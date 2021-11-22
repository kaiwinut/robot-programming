#!/usr/bin/env roseus
;;;
(ros::roseus "reach_checkerboard")
(load "package://pr2eus/robot-interface.l")
(load "package://dxl_armed_turtlebot/euslisp/dxl-armed-turtlebot.l")
;;;
(defclass armed-turtlebot-interface
  :super robot-interface
  :slots ())
;;;
(defmethod armed-turtlebot-interface
  (:init (&rest args)
    (send-super* :init :robot dxl-armed-turtlebot-robot args)
    (ros::advertise "/cmd_vel" geometry_msgs::Twist 1))
  (:default-controller
   ()
   (list
    (list
     (cons :controller-action "fullbody_controller/follow_joint_trajectory")
     (cons :controller-state "fullbody_controller/state")
     (cons :action-type control_msgs::FollowJointTrajectoryAction)
     (cons :joint-names '("arm_joint1" "arm_joint2" "arm_joint3"
                          "arm_joint4" "arm_joint5" "arm_joint6")))))
  (:go-velocity
   (x y d) ;; [m/sec] [m/sec] [deg/sec]
   (let ((lin (instance geometry_msgs::vector3 :init :x x :y y :z 0))
         (ang (instance geometry_msgs::vector3 :init :x 0 :y 0 :z (deg2rad d))))
     (ros::publish "/cmd_vel"
                   (instance geometry_msgs::Twist :init :linear lin :angular ang))))
  )
;;;
(setq *ri* (instance armed-turtlebot-interface :init))
;;
(setq *l* (instance ros::transform-listener :init))

(setq *target* (make-cube 50 50 50))
(setq *dxl-armed-turtlebot* (dxl-armed-turtlebot))
(objects (list *dxl-armed-turtlebot* *target*))

(ros::rate 10)
(do-until-key
 (setq tm (send *l* :get-latest-common-time "/camera_rgb_optical_frame" "/test_object"))
 (if tm
     (progn
       (ros::ros-info "get latest common time is ~A before"
                      (send (ros::time- (ros::time-now) tm) :to-sec))
       (when (< (send (ros::time- (ros::time-now) tm) :to-sec) 1.0)
         (setq target-local (send *l* :lookup-transform  "/camera_rgb_optical_frame"
                                                         "/test_object" tm))
         (ros::ros-info "lookup transform y = ~A" target-local)
         (setq target-world
               (send target-local :transform
                     (send *dxl-armed-turtlebot* :camera :camera_rgb_optical) :parent))
         (send *target* :move-to target-world :world)
         (orient-coords-to-axis *target* #f(0 0 1))
         (setq r
               (send *dxl-armed-turtlebot* :inverse-kinematics
                     (send *target* :copy-worldcoords)
                     :revert-if-fail t
                     :rotation-axis :z :debug-view nil :thre 100))
         (if r ;; ik solved!
             (progn
               (ros::ros-warn "send :angle-vector")
               (send *ri* :angle-vector (send *dxl-armed-turtlebot* :angle-vector) 200)
               )
           (progn ;; ik failed...
             (ros::ros-warn "send :go-velocity")
             (send *ri* :go-velocity
                   0.05 0 (if (> (elt (send target-local :worldpos) 1) 0) 2 -2)) ;; rotate and move forward slowly
             ))
         ))
   (progn
     (ros::ros-warn "could not get common time")
     (send *dxl-armed-turtlebot* :reset-pose2)
     (send *ri* :angle-vector (send *dxl-armed-turtlebot* :angle-vector) 1500)
     (send *ri* :go-velocity 0 0 4)
     ))
 (send *irtviewer* :draw-objects)
 (x::window-main-one)
 (ros::spin-once)
 (ros::sleep)
 ) ;; do-until-key

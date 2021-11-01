(load "models/room73b2-scene.l")
(load "models/h7-robot.l")
(setq *room* (room73b2))
(setq *robot* (h7))
(objects (list *robot* *room*))

(send *robot* :reset-pose)
(send *robot* :move-to (send *room* :spot "table-spot") :world)
(send *robot* :locate #f(0 -350 550))
(send *robot* :rotate (deg2rad 90) :z)

(send *irtviewer* :look-all
      (geo::make-bounding-box
       (flatten (send-all (send *robot* :bodies) :vertices))))

(setq *chair0* (send *room* :object "room73b2-chair0"))
(if (send *chair0* :parent) (send (send *chair0* :parent) :dissoc *chair0*))
(send *robot* :head :look-at (send *chair0* :worldpos))

(send *robot* :larm :inverse-kinematics
      (car (send *chair0* :handle))
      :link-list (send *robot* :link-list (send *robot* :larm :end-coords :parent))
      :move-target (send *robot* :larm :end-coords)
      :rotation-axis :z
      :debug-view t)

(send *robot* :larm :end-coords :assoc *chair0*)
(send *robot* :larm :move-end-pos #f(250 0 0) :world
      :debug-view t :look-at-target t)

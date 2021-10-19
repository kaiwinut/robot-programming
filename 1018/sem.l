(setq s3
      (make-gdome (make-gdome (make-gdome (make-icosahedron 20)))))
(send s3 :set-color :gray)
(send s3 :locate #f(550 550 0))

(setq s2
      (make-gdome (make-gdome (make-gdome (make-icosahedron 50)))))
(send s2 :set-color :blue)
(send s2 :locate #f(500 500 0))
(send s2 :assoc s3)

(setq s1
      (make-gdome (make-gdome (make-gdome (make-icosahedron 100)))))
(send s1 :set-color :yellow)
(send s1 :assoc s2)

(make-irtviewer)
(objects (list s1 s2 s3))

(dotimes (i 2572)
  (send s1 :rotate (deg2rad 0.14) :z)
  (send s2 :rotate (deg2rad 50) :z)
  (send *irtviewer* :draw-objects)
  (x::window-main-one))

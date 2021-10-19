(defclass rat
  :slots ((numer) (denom)))
(defmethod rat
  (:init
   (n d)
   (setq numer n)
   (setq denom d)
   self)
  (:numer () numer)
  (:denom () denom)
  (:add-rat
   (y)
   (setq ans (instance rat :init
		       (+ (* (send self :numer) (send y :denom))
			  (* (send self :denom) (send y :numer)))
		       (* (send self :denom) (send y :denom))))
   ans)

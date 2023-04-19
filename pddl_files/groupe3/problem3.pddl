(define (problem rubik2)
  (:domain rubik)
  (:objects r w b g o y - color)
  (:init
    (face1 o g w)
    (face2 o b w)
    (face3 r g w)
    (face4 r b w)
    (face5 b o y)
    (face6 b r y)
    (face7 g o y)
    (face8 g r y)
  )
  (:goal (and
    (face1 b o w)
    (face2 y o g)
    (face3 r g w)
    (face4 r y b)
    (face5 g r y)
    (face6 b w r)
    (face7 g w o)
    (face8 o y b)
  ))
)
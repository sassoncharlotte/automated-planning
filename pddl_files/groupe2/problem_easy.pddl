(define (problem military-race-0)
    (:domain military-race)
    (:objects
        pos11 - position
        pos12 - position
        pos13 - position
    )

    (:init
        (at pos13)
        (obstacle pos12)
        (munition)

        (adjacent pos11 pos12)
        (adjacent pos12 pos11)
        (adjacent pos12 pos13)
        (adjacent pos13 pos12)
    )

    (:goal
        (at pos11)
    )
)

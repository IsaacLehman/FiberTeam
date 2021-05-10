# FiberTeam

BY: Isaac Lehman
    An easy approach to multithreading in python.

    STEPS:
        1. Import
            from fiberTeam import FiberTeam
        2. Make some Fibers
            myFibers = FiberTeam(50)
        3. Run
            fiber_id = myFibers.add_fiber(function=make_pi, args=(arg1, arg2, ...))

            -or-

            @myFibers.Fiberize()
            def make_pi(thread_id, arg1, arg2, ...):
                ...

            make_pi(1,2,3...)
            make_pi(1,2,3...)
            ...
            make_pi(1,2,3...)
        4. Get result
            result = myFibers.join_fiber(fiber_id)

        def make_pi(thread_id, arg1, arg2, ...)

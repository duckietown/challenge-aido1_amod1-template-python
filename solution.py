#!/usr/bin/env python

from duckietown_challenges import wrap_solution, ChallengeSolution, ChallengeInterfaceSolution


class Solver(ChallengeSolution):
    def run(self, cis):
        assert isinstance(cis, ChallengeInterfaceSolution)

        from AidoGuest import AidoGuest
        hostname = "aido-host"
        aidoGuest = AidoGuest(hostname)
        aidoGuest.run()

        cis.set_solution_output_dict({})


if __name__ == '__main__':
    wrap_solution(Solver())

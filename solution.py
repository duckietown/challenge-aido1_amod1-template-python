import six

if six.PY2:
    msg = 'Only Python 3.6+ is supported.'
    raise Exception(msg)

from duckietown_challenges import wrap_solution, ChallengeSolution, ChallengeInterfaceSolution


class Solver(ChallengeSolution):
    def run(self, cis: ChallengeInterfaceSolution):
        from AidoGuest import AidoGuest
        hostname = "aido-host"
        cis.info('Starting AidoGuest with host = %s' % hostname)
        aidoGuest = AidoGuest(hostname)
        try:
            aidoGuest.run()
        except BaseException as e:
            msg = 'aidoGuest failed to run.'
            cis.error(msg)
            cis.error(e)
            raise e


        cis.set_solution_output_dict({})


if __name__ == '__main__':
    wrap_solution(Solver())

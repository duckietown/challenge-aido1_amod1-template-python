import logging
import time
import six

if six.PY2:
    msg = 'Only Python 3.6+ is supported.'
    raise Exception(msg)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
from DispatchingLogic import DispatchingLogic
from utils.StringSocket import StringSocket


class AidoGuest:
    """
    AidoGuest is a simple demo client that interacts with AidoHost.
    """

    # default values for demo

    SCENARIO = 'SanFrancisco.20080518'
    REQUEST_NUMBER_DESIRED = 500

    # decision variable
    NUMBER_OF_VEHICLES = 20
    PRINT_SCORE_PERIOD = 200

    def __init__(self, ip='localhost'):
        """
        :param ip: for instance "localhost"
        """
        self.ip = ip
        logger.info('AidoGuest using ip = %r' % ip)

    def run(self):
        """connect to AidoGuest"""
        logger.info('Guest waiting 10 s before connecting')
        time.sleep(10)
        logger.info('Guest connecting to %s' % self.ip)
        stringSocket = StringSocket(self.ip)
        # send initial command, e.g., {SanFrancisco.20080518}
        stringSocket.writeln('{%s}' % self.SCENARIO)  # scenario name

        # receive information on chosen scenario, i.e., bounding box and number of requests, the city grid is
        # inside the WGS: 84 coordinates bounded by the box bottomLeft, topRight,
        # {{longitude min, latitude min}, {longitude max, latitude max}}
        numReq, bbox, nominalFleetSize = stringSocket.readLine()
        bottomLeft, topRight = bbox

        # chose number of Requests and fleet size
        assert self.REQUEST_NUMBER_DESIRED <= numReq
        logger.info("Nominal fleet size:", nominalFleetSize)
        logger.info("Chosen fleet size: ", self.NUMBER_OF_VEHICLES)

        configSize = [self.REQUEST_NUMBER_DESIRED, self.NUMBER_OF_VEHICLES]
        stringSocket.writeln(configSize)

        dispatchingLogic = DispatchingLogic(bottomLeft, topRight)

        # receive dispatching status and send dispatching command
        count = 0
        while True:
            status = stringSocket.readLine()
            if status == '':  # when the server closed prematurely
                raise IOError("server terminated prematurely?")
            elif not status:  # server signal that simulation is finished
                break
            else:
                count += 1
                score = status[3]
                if count % self.PRINT_SCORE_PERIOD:
                    print("score = %s at %s" % (score, status[0]))

                command = dispatchingLogic.of(status)
                stringSocket.writeln(command)

        # receive final performance score/stats
        finalScores = stringSocket.readLine()
        logger.info("final service quality score:  ", finalScores[1])
        logger.info("final efficiency score:       ", finalScores[2])
        logger.info("final fleet size score:       ", finalScores[3])

        stringSocket.close()


def main():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default="localhost")

    parsed = parser.parse_args()

    host = parsed.host
    logger.info('Starting AidoGuest with host = %s' % host)
    aidoGuest = AidoGuest(host)
    aidoGuest.run()


if __name__ == '__main__':
    main()

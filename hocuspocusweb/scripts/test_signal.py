import os
import signal
import time


def handler(*args):
    print('Signal was recieved!')
    print('time: {}'.format(time.strftime('%x %X %z')))
    print('args: {}'.format(args))


if __name__ == '__main__':

    print('Process ID: {}'.format(os.getpid()))

    signal.signal(signal.SIGUSR1,
                  handler)

    while True:
        signal.pause()

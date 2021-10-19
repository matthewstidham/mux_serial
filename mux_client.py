#!/usr/bin/env python3

import sys
import socket
from pexpect import pty_spawn

_default_host = 'localhost'
_default_port = 23200


class MuxClient(object):

    def __init__(self, host=_default_host, port=_default_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.term = None

    def run(self, command):
        self.sock.connect_ex((self.host, self.port))
        self.term = pty_spawn.spawn(command=command)
        print('MUX > Connected to %s:%d' % (self.host, self.port), file=sys.stderr)
        return self.term

    def interact(self):
        print('MUX > Use ctrl+] to stop...\n', file=sys.stderr)
        self.term.interact()

    def close(self):
        print('\nMUX > Closing...', file=sys.stderr)

        if self.term is None:
            self.sock.close()
        else:
            self.term.close()  # Closes sock too

        print('MUX > Done! =)', file=sys.stderr)


if __name__ == '__main__':
    import optparse

    # Option parsing, duh
    parser = optparse.OptionParser()
    parser.add_option('-p', '--port',
                      help='Host port',
                      dest='port',
                      type='int',
                      default=_default_port)
    parser.add_option('--command', '-c',
                      help='command to run on device', default='echo hello world')
    (opts, args) = parser.parse_args()

    client = MuxClient(port=opts.port)
    client.run(command=opts.command)
    client.interact()

    if not sys.flags.interactive:
        client.close()

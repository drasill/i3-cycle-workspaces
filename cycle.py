#!/usr/bin/env python3
# vim: ts=4 sw=4 et

# NOTE : this is some quick and dirty code for my own needs.

import i3ipc
import re
import time
import argparse

class I3Cycler(object):

    def __init__(self, wsConfig):

        self.wsConfig = wsConfig

        self.conn                      = i3ipc.Connection()
        self.current_ws_name           = None
        self.current_ws_conf           = None
        self.currently_cycling_ws_name = None
        self.ws_change_ts              = time.time()
        self.current_cycle_num         = 1

        self.conn.on('workspace::focus', self.on_workspace_focus)
        self.conn.on('binding::run',     self.on_binding_run)


    def run(self):
        """ Run the script """
        try:
            self.conn.main()
        except KeyboardInterrupt:
            print('Exiting on keyboard interrupt')

    def on_workspace_focus(self, i3conn, e):
        """ When workspace is focused """
        self.current_ws_name = e.current.name
        self.ws_change_ts = time.time()

    def on_binding_run(self, i3conn, e):
        """ When a binding is ran """

        # Detect a "workspace" change command
        match = re.match(r"^workspace\s+(.*)$", e.binding.command)
        if not match:
            return

        ws_name = match.group(1)

        do_cycle = False

        if ws_name == self.currently_cycling_ws_name:
            # Currently cycling
            do_cycle = True
            self.current_cycle_num  = (self.current_cycle_num + 1) % self.current_ws_conf['cycle']

        elif ws_name == self.current_ws_name:
            # Already on the requested WS
            diff = time.time() - self.ws_change_ts
            # If too fast, this cannot be a second request.
            if diff > 0.01:

                # Which WS config do we match ?
                for key, ws in enumerate(self.wsConfig):
                    if re.match(ws['re'], ws_name):
                        self.current_ws_conf = ws
                        do_cycle = True
                        break

        if not do_cycle:
            self.currently_cycling_ws_name = None
            self.current_ws_conf = None
            self.current_cycle_num = 1
            return


        # Let's Cycle
        self.cycle()

    def cycle(self):
        """ Go to the "next" cycling workspace """

        if not self.currently_cycling_ws_name:
            self.currently_cycling_ws_name = self.current_ws_name

        # If it's a numeric, increment; otherwise, add some "+"
        m = re.match(r"^(\d+)(.*)$", self.currently_cycling_ws_name)
        if (m):
            next_num = int(m.group(1)) + self.current_cycle_num
            next_ws_name = "%d%s" % (next_num, m.group(2))
        else:
            next_ws_name = self.currently_cycling_ws_name
            for i in range(0, self.current_cycle_num):
                next_ws_name += "˖"

        self.conn.command('workspace ' + next_ws_name)


class WsAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(WsAction, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        if not namespace.ws:
            namespace.ws = []
        if self.dest == 'ws':
            namespace.ws.append({'re':values, 'cycle': 3})
        else:
            if len(namespace.ws) == 0:
                raise ValueError(("You must first specify a workspace with"
                    " 'ws' before an option like '"+self.dest+"'"))
            namespace.ws[len(namespace.ws) - 1][self.dest] = values

def main():
    parser = argparse.ArgumentParser(description='i3wm workspaces cycler')
    parser.add_argument('--ws', action=WsAction, dest='ws', required=True)
    parser.add_argument('--cycle', action=WsAction, dest='cycle', type=int)
    args = parser.parse_args()
    print(args.ws)
    cycler = I3Cycler(args.ws)
    cycler.run()

if __name__ == '__main__':
    main()

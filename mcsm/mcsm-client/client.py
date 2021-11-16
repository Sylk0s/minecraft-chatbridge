from mcsm.server.server import Server, MCServer
from mcsm.cli.cli_manager import Manager
import time
import argparse
import json
from threading import Thread

running = []

def argumentRunner():
    mcsm_parser = argparse.ArgumentParser(description='CLI Utility for managing servers')
    commands = mcsm_parser.add_subparsers()

    parser_status = commands.add_parser('status', help='Shows the status of the server(s) | Usage: mscm status [server] (no server arg will show info for all servers)')
    parser_status.add_argument('server',nargs='*',default='',help='[optional] Designate a server to get the status of')
    parser_status.set_defaults(func=get_status)

    parser_start = commands.add_parser('start', help='Starts the designated server | Usage: mcsm start [server]')
    parser_start.add_argument('server',help='Designate a server to start')
    # not quite sure how to make this work how I want
    # parser_start.add_argument('-a','--all',action='store_true')
    parser_start.set_defaults(func=start_server)

    parser_switch = commands.add_parser('switch', help='Switches CLI output to the given server | Usage: mcsm switch [server]')
    parser_switch.add_argument('server',help='Designate a server to switch to')
    parser_switch.set_defaults(func=switch_server)

    parser_stop = commands.add_parser('stop', help='Stops a server | Usage: mcsm stop [server]')
    parser_stop.add_argument('server',help='designate which server to stop')
    parser_stop.set_defaults(func=stop_server)

    parser_setup = commands.add_parser('setup', help='Sets up a server | Usage: mcsm setup [server]')
    parser_setup.add_argument('server',help='Name the server you want to setup')
    parser_stop.set_defaults(func=setup_server)

    parser_config = commands.add_parser('config', help='Use to config mcsm | Usage: mcsm config [option] [args]')
    parser_setup.add_argument('option',help='Select the option to change')
    parser_stop.set_defaults(func=config_mcsm)

    parser_list = commands.add_parser('list', help='List out all known servers | Usage: mcsm list')
    parser_list.set_defaults(func=list_servers)

    args = mcsm_parser.parse_args()
    args.func(args)

def get_status(args):
    if args.server:
        print('server specific status for',args.server)
    else:
        print('general status for all servers')
        print(running)

def start_server(args):

    print("Starting server",args.server)

    ctl = Controller()

    managerThread = Thread(target=ctl.runServer)
    managerThread.daemon = False
    managerThread.run()

    # ctl.runServer()

def switch_server(args):
    print('Switched to',args.server)

def stop_server(args):
    print('Stopped',args.server)

def setup_server(args):
    print('setting up',args.server)

def config_mcsm(args):
    print('configuring mcsm option',args.option)

def list_servers(args):
    print("\033[1m\033[96mServers:\n========")
    conf = json.load(open("server_configs.json"))
    # I like this, need to check if it works on windows or not (for online and offline)
    for e in conf:
        print("\033[92m"+e)

class Controller:
    def runServer(self):
        server = MCServer("server", self)
        server.run()

        running.append(server)

        print(running)
        #cli = Manager(server)
        #cli.startCLI()

        #while True:
        #   time.sleep(1)

    def getServerConfigFile(self):
        return "/home/sylkos/projects/minecraft-chatbridge/server_configs.json"

#ctl = Controller()
#ctl.runServer()

#time.sleep(20)

if __name__ == "__main__":
    argumentRunner()
import os
import sys
import time
import signal
import argparse

from config import config
import swarm

def arg_setup():
    arg_parser = argparse.ArgumentParser(description=config["description"])
    arg_parser.add_argument("action", type=unicode, \
        help="Start swarm or connect to swarm (start, stop, connect)")
    arg_parser.add_argument("--host", "-a", type=unicode, \
        help="Address of host swarm")
    arg_parser.add_argument("--port", type=int, \
        help="Port to host or connect to stratus swarm")
    arg_parser.add_argument("--key", type=unicode, \
        help="Key file to use")
    arg_parser.add_argument("--crt", type=unicode, \
        help="Cert file to use")
    arg_parser.add_argument("--name", "-n", type=unicode, \
        help="Name to identify client by other than hostname")
    arg_parser.add_argument("--username", "-u", type=unicode, \
        help="Username to connect to stratus swarm")
    arg_parser.add_argument("--password", "-p", type=unicode, \
        help="Password to connect to stratus swarm")
    arg_parser.add_argument("--ssl", action='store_true', default=False, \
        help="Connect to the swarm with ssl")
    arg_parser.add_argument("--recv", "-r", type=unicode, \
        default="print_recv", \
        help="Function to exicute on recive data (print_recv, shell)")
    arg_parser.add_argument('--daemon', action='store_true', \
        help="Start as a daemon")
    arg_parser.add_argument('--no-daemon', dest='daemon', action='store_false', \
        help="Start as a daemon")
    arg_parser.set_defaults(daemon=config["arg_defaults"]["daemon"])
    arg_parser.set_defaults(save_pid=True)
    arg_parser.add_argument("--version", "-v", action="version", \
        version=u"micropython version " + unicode(config["version"]) )
    initial = vars(arg_parser.parse_args())
    args = {}
    for arg in initial:
        if initial[arg]:
            args[arg] = initial[arg]
    return args

def start(options):
    swarm.launch("swarm", options)
    swarm.launch("proxy", options)
    return True

def connect(options):
    swarm.launch("swarm", options)
    return True

def stop(options):
    try:
        pid_file = open("daemon.pid", "rb")
        pid = int(pid_file.readline())
        pid_file.close()
        os.kill(pid, signal.SIGQUIT)
        os.unlink("daemon.pid")
    except:
        pass
    return False

def make_daemon(options={}):
    # Daemonize to run in background
    pid = os.fork()
    if pid > 0:
        # exit first parent
        sys.exit(0)
    pid = os.fork()
    if pid > 0:
        # exit second parent
        sys.exit(0)
    if "save_pid" in options:
        pid_file = open("daemon.pid", "wb")
        pid_file.write(str(os.getpid()))
        pid_file.close()
    if "output" in options:
        output = options["output"]
    elif os.name == "nt":
        output = "nul"
    else:
        output = "/dev/null"
    output = open(output, 'wb')
    sys.stdout = output
    sys.stderr = output

def main():
    options = arg_setup()
    # Get the action
    action = getattr(sys.modules[__name__], options["action"])
    del options["action"]
    if "daemon" in options:
        del options["daemon"]
        make_daemon(options)
    if action(options):
        while True:
            time.sleep(300)

if __name__ == '__main__':
    main()

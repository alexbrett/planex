#!/usr/bin/env python

# Some generic utils used by several other files

import subprocess
import os
import pipes
import urlparse

dump_cmds = True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def rewrite_url(url, destination=None):
    """
    Rewrite url to point to destination
    """
    (scheme, host, path, _, _, fragment) = urlparse.urlparse(url)
    if destination is None or scheme in ["git", "hg"]:
        return url

    else:
        basename = path.split("/")[-1]
        return destination + basename + fragment


def run(cmd, check=True, env=None, inputtext=None):
    """
    Run a command, dumping it cut-n-pasteably if required. Checks the return
    code unless check=False. Returns a dictionary of stdout, stderr and return
    code (rc)
    """
    if dump_cmds:
        print bcolors.WARNING, "CMD: ", (" ".join(map(pipes.quote,cmd))), bcolors.ENDC

    if env == None:
        env = os.environ.copy()

    proc = subprocess.Popen(cmd, env=env,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    [stdout,stderr] = proc.communicate(inputtext)

    if check and proc.returncode != 0:
        print bcolors.FAIL + "ERROR: command failed" + bcolors.ENDC
        print "Command was:\n\n  %s\n" % (" ".join(map(pipes.quote,cmd)))
        print "stdout"
        print "------"
        print stdout
        print "stderr"
        print "------"
        print stderr
        raise Exception
            
    return {"stdout":stdout, "stderr":stderr, "rc":proc.returncode}
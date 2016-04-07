#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# Copyright (C) 2016  Pan Jiabang
#
# This file is part of Tmux-Parallel.
#
# Tmux-Parallel is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Tmux-Parallel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tmux-Parallel. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Pan Jiabang"
__copyright__ = "Copyright 2016, Tmux-Parallel"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Pan Jiabang"
__email__ = "panjiabang@gmail.com"
__status__ = "Production"

import argparse
import subprocess
import sys


def call(shell_cmd):
    subprocess.call(shell_cmd, shell=True)


which_call = subprocess.Popen(['which', 'tmux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
which_call.wait()
if which_call.returncode != 0:
    print >> sys.stderr, """Tmux not installed, try to install tmux with following commands first.
Debian/Ubuntu: sudo apt-get install tmux
Fedora/CentOS: sudo yum install tmux
OS X: brew install tmux"""
    sys.exit(which_call.returncode)

parser = argparse.ArgumentParser(description="run commands in parallel using tmux")
parser.add_argument('-f', '--file', dest='file', default=[], action='append', required=True,
                    help='file of commands that can run in parallel')
parser.add_argument('-s', '--session', dest='session', default='ptmux',
                    help='specific a tmux session to run with')
args = parser.parse_args()

parallel_groups = []

for brew_file in args.file:
    with open(brew_file, 'r') as f:
        apps = f.readlines()
        apps = map(lambda x: x.replace('\n', '').strip(), apps)
        apps = filter(lambda x: len(x) > 0, apps)
        parallel_groups.append(apps)

command_wrapper = """
while true; do
    %s;
    if [ $? -eq 0 ]; then
        break;
    else
        read -p "mission fail, retry? (Y/N)[n]" retry;
        case $retry in
            [Yy]* ) continue;;
                * ) break;;
        esac
    fi;
done
"""

initial_sleep = 2
tmux_session = args.session

for group in parallel_groups:
    tmux_split_param = ['', '-h', '-v -t 0', '-v -t 1']
    progress = -1
    for command in group:
        progress += 1
        cmd = (command_wrapper % command).replace('\n', ' ')
        print cmd
        if progress > 0 and progress % 4 == 0:
            call("tmux new-window '%s'" % cmd)
            call("tmux select-window -t %s:%d" % (tmux_session, progress / 4))
        elif progress == 0:
            call("tmux new-session -d -s %s 'sleep %d && %s'" % (tmux_session, initial_sleep, cmd))
        else:
            param = tmux_split_param[progress % 4]
            call("tmux split-window %s '%s'" % (param, cmd))
    call("tmux -2 attach-session -t %s" % tmux_session)

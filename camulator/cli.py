# Camulator CLI scripts. 

import sys
import argparse
from .recorder import Recorder 
from .player import Player

def cli(args = sys.argv[0]):
    usage = "{} [options]".format(args)
    description = 'Record or replay Redis commands.'
    parser = argparse.ArgumentParser(prog = 'camulator', usage = usage, 
        description = description) 
    parser.add_argument('-r', '--record', action = 'store_true', 
        default = False, help = 'Record Redis commands.')
    parser.add_argument('-p', '--play', action = 'store_true', 
        default = False, help = 'Play Redis commands.')
    parser.add_argument('file_name', type = str, default = 'obs.txt.gz',
        help = 'Filename to record or play back.')
    parser.add_argument('-n', '--notiming', action = 'store_true', 
        default = False, help = 'Do not use original recorded timings.')
    parser.add_argument('-c', '--commands', type = str, default = 'set, publish',
        help = 'List of commands to record. Defaults to \'set, publish\'. Currently supports Redis commands with 2 arguments.')
    parser.add_argument('-ch', '--channels', type = str, default = 'all',
        help = 'List of channels to publish to from a recording, ignoring those not listed. Default = \'all\'.')
    if(len(sys.argv[1:])==0):
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    main(record = args.record, play = args.play, file_name = args.file_name, 
        no_timing = args.notiming, commands = args.commands, 
        channels = args.channels)

def main(record, play, file_name, no_timing, commands, channels):
    if(record & play):
        print('Ignoring record command.')
        rec = Recorder()
        rec.record(file_name, commands)
    elif(record):
        rec = Recorder()
        rec.record(file_name, commands)
    elif(play):
        player = Player()
        player.play(file_name, no_timing, channels)

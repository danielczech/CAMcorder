# Camulator CLI scripts. 

import sys
import argparse
from .recorder import Recorder 
from .player import Player

def cli(args = sys.argv[0]):
    usage = "{} [options]".format(args)
    description = 'Record or replay an observation\'s metadata Redis messages.'
    parser = argparse.ArgumentParser(prog = 'camulator', usage = usage, 
        description = description) 
    parser.add_argument('-r', '--record', action = 'store_true', 
        default = False, help = 'Record an observation\'s Redis messages.')
    parser.add_argument('-p', '--play', action = 'store_true', 
        default = False, help = 'Play an observation\'s Redis messages.')
    parser.add_argument('file_name', type = str, default = 'obs.txt.gz',
        help = 'Filename to record or play back.')
    parser.add_argument('-n', '--notiming', action = 'store_true', 
        default = 'False', help = 'Do not use recorded original timings.')
    parser.add_argument('-c', '--channels', type = str, default = 'all',
        help = 'Comma separated list of channels to publish to from a recording, ignoring those not listed. By default all channels are published to.')
    if(len(sys.argv[1:])==0):
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    main(record = args.record, play = args.play, file_name = args.file_name, 
        no_timing = args.notiming, channels = args.channels)

def main(record, play, file_name, no_timing, channels):
    if(record & play):
        print('Ignoring record command.')
        rec = Recorder()
        rec.record(file_name)
    elif(record):
        rec = Recorder()
        rec.record(file_name)
    elif(play):
        player = Player()
        player.play(file_name, no_timing, channels)

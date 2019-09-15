# Camulator CLI scripts. 

import sys
import argparse

def cli(args = sys.argv[0]):
    usage = "{} [options]".format(args)
    description = 'Record or replay an observation\'s metadata Redis messages.'
    parser = argparse.ArgumentParser(prog = 'camulator', usage = usage, 
        description = description) 
    parser.add_argument('-r', '--record', action = 'store_true', 
        default = False, help = 'Record an observation\'s Redis messages.')
    parser.add_argument('-p', '--play', action = 'store_true', 
        default = False, help = 'Play an observation\'s Redis messages.')
    parser.add_argument('-f', '--file', type = str, default = 'obs.yml', 
        help = 'Filename to record or play back (yml).') 
    if(len(sys.argv[1:])==0):
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    main(record = args.record, play = args.play, filename = args.file)

def main(record, play, filename):
    if(record & play):
        print('Ignoring record command.')
    elif(record):
        print('recording ' + filename)
    elif(play):
        print('playing ' + filename)







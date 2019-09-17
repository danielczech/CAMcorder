# Class to play recorded Redis activity.

import redis
import gzip
import time

class Player(object):
    """Play back a file containing a sequence of recorded Redis commands.
    """ 

    def __init__(self, host = '127.0.0.1', port = '6379'):
        self.host = host
        self.port = port
        self.redis_server = redis.StrictRedis(host, port)
        
    def play(self, file_name, no_timing, channels):
        """Play back redis commands recorded in a file. 
        """
        entries = self.read_file(file_name)
        for entry in entries:
            try:
                delay, cmd, arg0, arg1 = self.read_entry(entry)
            except:
                print('Could not read entry; skipping...') # Log in future
                continue
            if(no_timing): 
                # If timing is not to be used - constant delay of 0.25 between
                # commands.
                time.sleep(0.25)     
            else:
                # Precise delays currently not required, so processing time is 
                # ignored for now. In future, if needed, commands
                # will be processed at specific times.
                time.sleep(delay)
            try:
                self.redis_server.execute_command(cmd, arg0, arg1)
            except:
                print('Could not issue Redis command; skipping...')
        print('Playback of {} completed.'.format(file_name)) # Log in future 

    def read_entry(self, entry):
        """Process entry from recording. 
        """
        atts = entry.split(' ')
        delay = float(atts[0])
        cmd = atts[1]
        arg0 = atts[2]
        arg1 = atts[3].strip('\n')
        return delay, cmd, arg0, arg1

    def read_file(self, file_name):
        """Read entire file into memory first to avoid bottlenecks if
        playing back redis commands quickly.
        """
        entries = []
        try:
            with gzip.open(file_name, 'r') as f:
                entries = f.readlines()        
        except:
            # In future will log
            print('Could not open file: {}'.format(file_name))
        return entries

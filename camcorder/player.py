# Class to play recorded Redis activity.

import redis
import gzip
import time

class Player(object):
    """Play back a file containing a sequence of recorded Redis commands.
    """ 

    def __init__(self, host = '127.0.0.1', port = '6379'):
        """Initialise redis server.
        """
        self.host = host
        self.port = port
        self.redis_server = redis.StrictRedis(host, port)
        
    def play(self, file_name, no_timing, channels):
        """Play back redis commands recorded in a file.
                
        Args:
            file_name (str): Name and path of file to read.
            no_timing (bool): If true, ignore recorded timing of commands.
            channels (str): Channels to publish to (default = \'all\').

        Returns:
            None
        """
        entries = self.read_file(file_name)
        t0 = 0
        for entry in entries:
            try:
                t_entry, cmd, arg0, arg1 = self.read_entry(entry)
                delay = t_entry - t0
                t0 = t_entry
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
                self.redis_command(cmd, arg0, arg1, channels)
            except:
                print('Could not issue Redis command; skipping...')
        print('Playback of {} completed.'.format(file_name)) # Log in future 

    def redis_command(self, cmd, arg0, arg1, channels):
        """Execute Redis command, accounting for specified channels. Note that
        currently, only Redis commands with two arguments are supported. 

        Args:
            cmd (str): Redis command to be executed.
            arg0 (str): First argument of Redis command.
            arg1 (str): Second argument of Redis command.
            channels (str): List of channels that may be published to. 

        Returns:
            None
        """
        if('all' not in channels):
            if(('publish' in cmd.lower()) & (arg0 in channels)):
                self.redis_server.execute_command(cmd, arg0, arg1)
        else: 
            self.redis_server.execute_command(cmd, arg0, arg1)

    def read_entry(self, entry):
        """Process an entry from a recording. Note that currently, 
        only Redis commands with two arguments are supported. 

        Args:
            entry (str): Entry from a recording file.

        Returns:
            t_entry (float): Timestamp (in seconds since start of recording).
            cmd (str): Redis command to be executed.
            arg0 (str): First argument of Redis command.
            arg1 (str): Second argument of Redis command.
        """
        atts = entry.partition(' ')
        t_entry = float(atts[0])
        atts = atts[2].strip().partition(' ') 
        cmd = atts[0]
        atts = atts[2].strip().partition(' ')
        arg0 = atts[0]
        arg1 = atts[2].strip('\n')
        return t_entry, cmd, arg0, arg1

    def read_file(self, file_name):
        """Read entire recording file into memory first to avoid bottlenecks if
        playing back Redis commands quickly.
        
        Args: 
            file_name (str): Name and filepath of recording file.
   
        Returns:
            entries (list): List of entries (str) containing Redis commands.
        """
        entries = []
        try:
            with gzip.open(file_name, 'r') as f:
                entries = f.readlines()        
        except:
            # In future will log
            print('Could not open file: {}'.format(file_name))
        return entries

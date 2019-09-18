# Class to record all desired redis activity

import os.path
import redis
import time
import numpy as np
import gzip

class Recorder():
    """Class to record redis activity during an observation. This activity
    includes all published messages to any channel and all key-value pairs
    written to the database. Currently, only Redis commands which accept two
    arguments are recorded. 
    """ 
    def __init__(self, host = '127.0.0.1', port = '6379'):
        """Connect to Redis server.
        """
        self.host = host
        self.port = port
        self.redis_server = redis.StrictRedis(host, port)
        self.t_start = None

    def record(self, file_name, commands):
        """Listen to all desired Redis activity.

        Args:
            file_name (str): Name of file to write.
            commands (str): Commands to record (ignoring others).
        """
        commands = commands.replace(',', '').lower().split(' ')
        print('Recording; ^C to stop')
        self.t_start = time.time() # Relative start time of recording.
                                   # Note: not the time since first
                                   # recorded entry.
        # Check if file to record already exists:
        if(os.path.isfile(file_name)):
            print('File {} exists; overwriting'.format(file_name)) # log in future
            open(file_name, 'w').close()
        while True:
            try:
                result = self.redis_server.execute_command('monitor')
                # Only interested in the commands 'set' and 'publish'
                rec_entry = self.parse_result(result.lower(), commands)
                if rec_entry is not None:
                    self.write_entry(file_name, rec_entry)
            except KeyboardInterrupt:
                print '\nRecording to {} stopped'.format(file_name)
                return

    def parse_result(self, result, commands):
        """Decode Redis monitor results and return strings to 
        write to the current recording's file.

        Args:
            result (str): Redis monitor result. 
            commands (list): List of Redis command types (str) to record.
        
        Returns:
            entry (str): Redis command entry to save to recording file. 

        """
        entry = None
        for command in commands:
            # Enclose in \" to ensure only specific command obtained.
            command ='"{}"'.format(command)
            if command in result:
                t_offset = time.time() - self.t_start
                try:
                    result = result.split(command)[1]
                    args = result.split(' ')
                    entry = '{} {} {} {}\n'.format(t_offset, command, 
                            args[1], args[2])
                except:
                    # In future will log
                    print('Unexpected result. Skipping...')
                # Expecting one command per result, so can return
                return entry

    def write_entry(self, file_name, entry):
        """Append an entry to the recording file; creates the recording
        file if it does not exist.
 
        Args:
            file_name (str): Name of recording file.
            entry (str): Redis command entry to append to recording.
        """
        with gzip.open(file_name, 'a') as f:
            f.write(entry.replace('"', ''))               

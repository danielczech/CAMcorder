# camulator

Record or replay Redis commands. 

In the case of the `meerkat-backend-interface`, the `camulator` can be used to simulate an observation's metadata by recording and replaying the sequence of Redis messages containing CAM information. For example, the `camulator` could take the place of the `katcp_server` and `katportal_server` when simulating an observation. 

The `Recorder` class makes use of the Redis command [MONITOR](https://redis.io/commands/MONITOR), which impacts Redis throughput.  

### Usage:

Record occurrences of the Redis commands `SET` and `PUBLISH` to a file:
`camulator -r file_name.txt.gz -c 'set, publish'`

Play back Redis commands stored in a file, publishing only to the channels `alerts` and `sensor_alerts`:
`camulator -p file_name.txt.gz -ch 'alerts, sensor_alerts'`

<pre>
positional arguments:
  file_name             Filename to record or play back.

optional arguments:
  -h, --help            show this help message and exit
  -r, --record          Record Redis commands to file.
  -p, --play            Play Redis commands from file.
  -n, --notiming        Do not use original recorded timings.
  -c COMMANDS, --commands COMMANDS
                        List of commands to record. Defaults to 'set,
                        publish'. Currently supports Redis commands with 2
                        arguments.
  -ch CHANNELS, --channels CHANNELS
                        List of channels to publish to from a recording,
                        ignoring those not listed. Default = 'all'.
</pre>

### Installation

[Redis](https://redis.io/topics/quickstart) should already be installed.
You may wish to install the camulator in a virtual environment. 
 
```
python setup.py install
```

### To Do:

- Add a logger.
- Improve timing by specifying precise times at which commands should be executed.
- Add support for Redis commands which do not have two arguments.


# camulator

Record or replay Redis commands. 

In the case of the `meerkat-backend-interface` this will be useful to simulate an observation's metadata by recording and replaying the sequence of Redis messages containing CAM information. For example, the `camulator` could take the place of the `katcp_server` and `katportal_server` when simulating an observation. 

### Usage:

positional arguments:
  file_name             Filename to record or play back.

optional arguments:
  -h, --help            show this help message and exit
  -r, --record          Record Redis commands.
  -p, --play            Play Redis commands.
  -n, --notiming        Do not use original recorded timings.
  -c COMMANDS, --commands COMMANDS
                        List of commands to record. Defaults to 'set,
                        publish'. Currently supports Redis commands with 2
                        arguments.
  -ch CHANNELS, --channels CHANNELS
                        List of channels to publish to from a recording,
                        ignoring those not listed. Default = 'all'.


### To Do:

Add a logger.

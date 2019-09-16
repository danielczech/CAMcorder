# camulator
Simulate an observation's metadata by recording and replaying the sequence of Redis messages containing CAM information.
The `camulator` takes the place of the `katcp_server` and `katportal_server` when simulating an observation. 

The current file format for recordings is just a text file, the idea being that it can easily be opened and read by a human. 

### To Do:

Add a logger.

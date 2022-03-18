# psi-02 - Multi-threaded TCP socket server

## Usage

<code>python server.py 6006</code> or any other port.

## Description

Written in Python 3, tested with version 3.8. The only file is <code>server.py</code>, which takes one parameter - port number. The server is then run on <code>localhost:port</code>.
The server accepts only GET requests, to which it responds with OK 200 response and the same text in an HTML body, so that it can be easily tested in web browser.
  
## Technical details
  
The server uses built-in Python wrapper around C sockets. The only non-standard construction in the code is the function <code>recv_timeout</code>, which takes care of receiving the incoming data. This function deals with the problem of <code>recv</code> call being blocking, which means that the call can block after receiving the last byte of the incoming data. This is mitigated by setting the socket as non-blocking and then using timeouts to receive all the data without blocking on the last byte.

# cli-screenview
A remote screen viewer written in Python for your text-only console. Control any GUI application and play games like e.g. Minecraft in your console.

![](https://raw.githubusercontent.com/louis-e/cli-screenview/main/screenshot1.png)
<br>*Video Demonstration: https://www.youtube.com/watch?v=P1d04is-wQQ*

### Parameters
The following parameters are currently available:
```shell
python cli-screenview-server.py IP PORT CONTROLS AUTH_TOKEN
python cli-screenview-client.py IP PORT AUTH_TOKEN CNSL_WIDTH FPS UNICODE CONTROLS
```
Parameter  | Explanation | Default Value | Optional
------------- | ------------- | ------------- | -------------
IP | Server IP | 127.0.0.1 | No
Port | Server Port | 1860 | No
AUTH_TOKEN | Authentication token which the client has to provide in order to authenticate itself. If used on the server script, this will set an own token instead of generating a new random token | *RANDOM* | No (client) / Yes (server)
CNSL_WIDTH | Max characters width of the console | 100 | Yes
FPS | Framerate | 10 | Yes
UNICODE | Console Unicode Support (For Windows CMD set *False* or use Powershell workaround) | True | Yes
CONTROLS | Enable sending / receiving keyboard input | True | Yes

To exit the scripts, use ESC on the server script and CTRL-C on the client script.

-------------
### How to use
##### Example
```shell
$ pip3 install -r requirements.txt
$ python3 server.py 127.0.0.1 1860

$ python3 client.py 127.0.0.1 1860 AUTH_TOKEN 120 10 false
```

-------------
### To Do
##### Features 
- [ ] Better parameter system
- [ ] Mouse control
- [ ] Auto buffer size
- [ ] Sound

##### Known Bugs
- After exiting the client script, further commands are not displayed anymore in that specific console session. A fix is already in progress.
- Transmission delays when using the UNICODE parameter (Workaround: Set a target FPS value of 10 or lower)
- Buffer Overflow (Workaround: Increase the buffer size in the client script or decrease the CNSL_WIDTH value)

-------------
### Windows CMD Color Workaround
Use the following command in an administrator Powershell in order to activate the Unicode support which is used for the advanced color processing in the Windows command line.
```powershell
Set-ItemProperty HKCU:\Console VirtualTerminalLevel -Type DWORD 1
```
Otherwise set the UNICODE parameter to *False*. This might affect the render quality.

-------------
This project would not be possible without
- https://github.com/pnappa/CLImage
- https://github.com/ollipal/sshkeyboard

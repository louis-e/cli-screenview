import socket, sys, time, os, climage
from threading import Thread
from signal import signal, SIGINT
from sshkeyboard import listen_keyboard

serverAddressPort = (sys.argv[1], int(sys.argv[2]))
bufferSize = 32768
encoding = "utf-8"
connectionEstablished = False
consoleWidth = int(os.get_terminal_size().columns - os.get_terminal_size().columns / 5)
consoleUnicode = True
keyboardControls = True



UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(str.encode(sys.argv[3]), serverAddressPort)

if (len(sys.argv) > 4):
    consoleWidth = int(sys.argv[4])
if (len(sys.argv) > 6):
    consoleUnicode = sys.argv[6].lower() == "true"
if (len(sys.argv) > 7):
    keyboardControls = sys.argv[7].lower() == "true"



def clear():
    os.system('cls' if os.name=='nt' else 'clear')
clear()

def moveCursor(x, y):
    print("\033[" + str(x) + ";" + str(y) + "H")

def checkCon():
    global connectionEstablished

    time.sleep(3)
    if not (connectionEstablished):
        print("Timeout: Server did not respond")
        os._exit(0)
Thread(target=checkCon).start()

def signalHandler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting')
    os.remove("temp-screenview-img.jpeg")
    if (connectionEstablished): UDPClientSocket.sendto(str.encode("CMD:QUIT"), serverAddressPort)
    os._exit(0)
signal(SIGINT, signalHandler)

def keyListener():
    def keyPressed(key):
        UDPClientSocket.sendto(str.encode("KEY_P:" + key), serverAddressPort)
    def keyReleased(key):
        UDPClientSocket.sendto(str.encode("KEY_R:" + key), serverAddressPort)
    listen_keyboard(on_press=keyPressed, on_release=keyReleased, delay_second_char=0, delay_other_chars=0)



while(True):
    bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    try:
        if (message.decode(encoding)[0:4] == "CMD:"):
            if (message.decode(encoding)[4:len(message.decode(encoding))] == "EXIT"):
                break
            elif (message.decode(encoding)[4:len(message.decode(encoding))] == "TRUSTED"):
                connectionEstablished = True
                if (keyboardControls): Thread(target=keyListener, daemon=True).start()
                if (len(sys.argv) > 4):
                    UDPClientSocket.sendto(str.encode("RES:" + str(int(sys.argv[4]) + 165)), serverAddressPort)
                    if (len(sys.argv) > 5):
                        UDPClientSocket.sendto(str.encode("FPS:" + sys.argv[5]), serverAddressPort)
            elif (message.decode(encoding)[4:len(message.decode(encoding))] == "QUIT"):
                print("Server closed connection")
                os._exit(0)
        elif (message.decode(encoding)[0:4] == "MSG:"):
            print("Message from server: " + message.decode(encoding)[4:len(message.decode(encoding))])
    except UnicodeDecodeError:
        try:
            newFile = open("temp-screenview-img.jpeg", "wb")
            for byte in message:
                newFile.write(byte.to_bytes(1, byteorder='big'))
            newFile.close()
            moveCursor(0, 0)
            print(climage.convert('temp-screenview-img.jpeg', is_unicode=consoleUnicode, is_truecolor=True, is_256color=False, width=consoleWidth))
        except: pass
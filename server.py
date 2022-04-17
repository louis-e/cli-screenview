import socket, random, string, time, PIL.ImageGrab, io, os, sys
from threading import Thread
from PIL import Image
from pynput.keyboard import Controller
from pynput import keyboard

serverIP = "127.0.0.1"
serverPort = 1860
bufferSize = 1024
trustedAddress = ("", 0)
connectionEstablished = False
authToken = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
encoding = "utf-8"
fps = 10
resScaler = 200
keyboardController = Controller()
keyboardControls = True



if (len(sys.argv) > 1):
    serverIP = sys.argv[1]
if (len(sys.argv) > 2):
    serverPort = int(sys.argv[2])
if (len(sys.argv) > 3):
    keyboardControls = sys.argv[3].lower() == "true"
if (len(sys.argv) > 4):
    authToken = sys.argv[4]

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((serverIP, serverPort))

print("UDP server listening on " + str(serverIP) + ":" + str(serverPort) + ". Press ESC to exit")
print("Auth Token: " + authToken + "\n")



def imageToByteArray(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, "JPEG")
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def sendScreen():
    global trustedAddress, connectionEstablished, resScaler

    while(connectionEstablished):
        screen = PIL.ImageGrab.grab()
        screen = screen.resize((int(screen.width * (resScaler * 100 / screen.width) / 100), int(screen.height * (resScaler * 100 / screen.width) / 100)))
        if (trustedAddress != ("", 0)): UDPServerSocket.sendto(imageToByteArray(screen), trustedAddress)
        time.sleep(1 / fps)

def exitListener(key):
    if key == keyboard.Key.esc:
        print("Exit triggered")
        if (connectionEstablished): UDPServerSocket.sendto(str.encode("CMD:QUIT"), trustedAddress)
        os._exit(0)
listener = keyboard.Listener(on_press=exitListener)
listener.start()



def recv():
    global trustedAddress, connectionEstablished, fps, resScaler, keyboardController

    while(True):
        try: bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        except: print("Client unexpectedly disconnected"); os._exit(1)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        if (trustedAddress != address and len(trustedAddress[0]) == 0):
           if (message.decode(encoding) == authToken):
               print("Client " + address[0] + ":" + str(address[1]) + " accepted")
               trustedAddress = address
               UDPServerSocket.sendto(str.encode("CMD:TRUSTED"), trustedAddress)

               connectionEstablished = True
               Thread(target=sendScreen).start()
           else:
               print("Client " + address[0] + ":" + str(address[1]) + " rejected: auth token does not match")
               UDPServerSocket.sendto(str.encode("MSG:Auth token does not match"), address)
               UDPServerSocket.sendto(str.encode("CMD:EXIT"), address)
               continue
        elif (trustedAddress != address):
            print("Client " + address[0] + ":" + str(address[1]) + " rejected: limit of 1 connection reached")
            UDPServerSocket.sendto(str.encode("MSG:Maximum of 1 connection reached"), address)
            UDPServerSocket.sendto(str.encode("CMD:EXIT"), address)
            continue


        if (message.decode(encoding)[0:4] == "FPS:"):
            fps = int(message.decode(encoding)[4:len(message.decode(encoding))])
            print("Set FPS: " + str(fps))
        elif (message.decode(encoding)[0:4] == "RES:"):
            resScaler = int(message.decode(encoding)[4:len(message.decode(encoding))])
            print("Set RES: " + str(resScaler))
        elif (message.decode(encoding)[0:4] == "CMD:"):
            if (message.decode(encoding)[4:len(message.decode(encoding))] == "QUIT"):
                connectionEstablished = False
                trustedAddress = ("", 0)
                print("Client " + address[0] + ":" + str(address[1]) + " disconnected")
        elif (message.decode(encoding)[0:6] == "KEY_P:" and keyboardControls):
            #print("Key Pressed: " + message.decode(encoding)[6:len(message.decode(encoding))])
            if (len(message.decode(encoding)[6:len(message.decode(encoding))]) == 1):
                keyboardController.press(message.decode(encoding)[6:len(message.decode(encoding))])
            else:
                if (message.decode(encoding)[6:len(message.decode(encoding))] == "space"):
                    keyboardController.press(keyboard.Key.space)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "enter"):
                    keyboardController.press(keyboard.Key.enter)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "backspace"):
                    keyboardController.press(keyboard.Key.backspace)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "esc"):
                    keyboardController.press(keyboard.Key.esc)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "tab"):
                    keyboardController.press(keyboard.Key.tab)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "shift"):
                    keyboardController.press(keyboard.Key.shift)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "ctrl"):
                    keyboardController.press(keyboard.Key.ctrl)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "alt"):
                    keyboardController.press(keyboard.Key.alt)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "capslock"):
                    keyboardController.press(keyboard.Key.caps_lock)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "up"):
                    keyboardController.press(keyboard.Key.up)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "down"):
                    keyboardController.press(keyboard.Key.down)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "left"):
                    keyboardController.press(keyboard.Key.left)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "right"):
                    keyboardController.press(keyboard.Key.right)
        elif (message.decode(encoding)[0:6] == "KEY_R:" and keyboardControls):
            #print("Key Released: " + message.decode(encoding)[6:len(message.decode(encoding))])
            if (len(message.decode(encoding)[6:len(message.decode(encoding))]) == 1):
                keyboardController.release(message.decode(encoding)[6:len(message.decode(encoding))])
            else:
                if (message.decode(encoding)[6:len(message.decode(encoding))] == "space"):
                    keyboardController.release(keyboard.Key.space)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "enter"):
                    keyboardController.release(keyboard.Key.enter)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "backspace"):
                    keyboardController.release(keyboard.Key.backspace)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "esc"):
                    keyboardController.release(keyboard.Key.esc)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "tab"):
                    keyboardController.release(keyboard.Key.tab)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "shift"):
                    keyboardController.release(keyboard.Key.shift)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "ctrl"):
                    keyboardController.release(keyboard.Key.ctrl)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "alt"):
                    keyboardController.release(keyboard.Key.alt)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "capslock"):
                    keyboardController.release(keyboard.Key.caps_lock)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "up"):
                    keyboardController.release(keyboard.Key.up)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "down"):
                    keyboardController.release(keyboard.Key.down)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "left"):
                    keyboardController.release(keyboard.Key.left)
                elif (message.decode(encoding)[6:len(message.decode(encoding))] == "right"):
                    keyboardController.release(keyboard.Key.right)


Thread(target=recv).start()

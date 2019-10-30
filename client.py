import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import io
import numpy
from PIL import Image
import socket

cap=cv2.VideoCapture(0)

def receive(sock):

    totrec = 0
    msgArray = bytearray()
    c = sock.recv(8)
    c=c.decode()
    length=int(c)
    while totrec<length :
        chunk = sock.recv(length-totrec)
        msgArray.extend(chunk)
        totrec += len(chunk)
    show_frd(msgArray)

def send2(framestring,sock):

    length =len(framestring)
    lengthstr=str(length).zfill(8)
    sent = sock.send((lengthstr).encode())
    sock.sendall(framestring)


def show_me(im_b):

    p=io.BytesIO(im_b)
    pi=Image.open(p)
    img = cv2.cvtColor(numpy.array(pi), cv2.COLOR_RGB2BGR)
    cv2.imshow('Me',img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

def show_frd(im_b):

    p=io.BytesIO(im_b)
    pi=Image.open(p)
    img = cv2.cvtColor(numpy.array(pi),cv2.COLOR_RGB2BGR)
    cv2.imshow('Friend',img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

def send1(client):

    ret,img = cap.read()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    pimg = Image.fromarray(img)
    b = io.BytesIO()
    pimg.save(b,'jpeg')
    image_b = b.getvalue()
    show_me(image_b)
    send2(image_b,client)

def connectionEstablishment(ip,portno):

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,portno))
    print("Connection Established with :",ip,"at port number:",portno)
    print("Wait...")
    return s

portno = int(input("Enter the Port Number:"))
ip = '10.1.82.126'
s = connectionEstablishment(ip,portno)

while True:

    send1(s)
    receive(s)

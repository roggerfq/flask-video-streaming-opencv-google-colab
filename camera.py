import time
from base_camera import BaseCamera
import cv2
from multiprocessing.connection import Listener
import sys


class Camera(BaseCamera):
    @staticmethod
    def frames():

        address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
        str_key = '1234'
        listener = Listener(address, authkey=bytes(str_key, encoding= 'utf-8'))
        conn = listener.accept()
 

        while True:
           # read current frame
           data = conn.recv()
           img = data[0]
           flag = data[1]
           if(flag == False):
              print("close process")
              sys.exit()

           # encode as a jpeg image and return it
           yield cv2.imencode('.jpg', img)[1].tobytes()

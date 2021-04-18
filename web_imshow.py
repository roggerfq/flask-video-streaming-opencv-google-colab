from multiprocessing import Process
from app import app
import cv2

from multiprocessing.connection import Client

import time
def f(app):
    app.run()

class WebWindow():
  def __init__(self):

      p = Process(target=f, args=(app,))
      p.start()
      #p.join()

      address = ('localhost', 6000)
      str_key = '1234'
      self.conn = None
      connected = False
      while not connected:
          try:
             self.conn = Client(address, authkey=bytes(str_key, encoding= 'utf-8'))
             connected = True
          except Exception as e:
             print("wait for socket two seconds")
             time.sleep(2)

  def imshow(self, img):
      flag = True
      self.conn.send([img, flag])

  def close(self):
      flag = False
      self.conn.send([None, flag])
      self.conn.close()

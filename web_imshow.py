from app import app
from multiprocessing import Process
import cv2
from multiprocessing.connection import Client
import time


def f(app):
    app.run()

class WebWindow():
  def __init__(self):

    #__________Solution to "Address already in use"_________

      import os
      import subprocess
      from subprocess import check_output
      import re
      import signal

      port = 5000 #port flask

      def get_pid(name):
          return check_output(["pidof",name])

      try:
          data = subprocess.check_output(['lsof', '-i:{}'.format(port)]).decode().split('\n')[1]
          pid = re.match('^([a-zA-Z0-9]+)(\s+)([0-9]+)\s', data).groups()[2]
          print('flask: '+ str(pid))
          os.kill(int(pid), signal.SIGTERM) #or signal.SIGKILL 
      except:
          print('pass flask')
          pass

      try:
          str_pid_list = get_pid('ngrok').decode("utf-8").split(' ')
          for str_pid in str_pid_list:
              pid = int(str_pid)
              print('ngrok: '+ str(pid))
              os.kill(pid, signal.SIGTERM) #or signal.SIGKILL 
      except: 
          print('pass ngrok')
          pass

      #________________________________________________________


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

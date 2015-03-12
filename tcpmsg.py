#cs3130 Assignment 4
#Janelle Montgomery

# A TCP-based client and server that accesses a database. You will be able to modify
#the database using : search,add,remove, and display. To do this TCP based protcol
#will be used.


import random, socket, sys, argparse, ssl
import main
#what the server uses to check if all the information has been sent <term>
term = '.'
#host = '127.0.0.1'
#port = 2015
cafile = "ca.crt"
certfile = "localhost.pem"
#client for TCP
def client(host, port):
    h=host
    p=port
    while True:
        selection = main.display_menu()
        if selection == 1:
            db_add(h,p)
        elif selection == 2:
            db_search(h,p)
        elif selection == 3:
            db_remove(h,p)
        elif selection == 4:
            db_display(h,p)
        elif selection == 5:
            db_quit(h,p)
        else:
            print('Your choice is not valid, Try again :)')

#add a user to the database protocol +800
def db_add(host,port):
    
    
    print("Enter a 4 digit employee ID:")
    user_id = str(input())
    user_id = user_id + ':'
    
    
    print("Enter employees first name:")
    user_first = input()
    user_first = user_first + ':'
    

    print("Enter employees last name:")
    user_last = input()
    user_last = user_last + ':'
    

    print("Enter the employees department:")
    user_dep = input()
    user_dep = user_dep + term
    print('\n')

    #connecting to host and port and sending to the server
    user = user_id + user_first + user_last + user_dep
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile="ca.crt")
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    send = '+800:' + user
    ecmsg = send.encode('ascii')
    ssl_sock.sendall(ecmsg)
    reply = recv_all(ssl_sock)
    reply = reply.replace('.','')
    ssl_sock.close()
    print(str(reply))
    print('\nWould you like to add another employee? Y/N')
    choice = False
    while choice == False:
        answer = input()
        print("\n")
        if answer in['y','n','Y','N']:
            choice = True
        else:
            print("Invalid input.") 
            choice = False
                    
                   
    if answer in ['y','Y']:
        db_add()

#searching for a user in the database protocol +810
def db_search(host,port):
    
    print("Please enter an Employee ID:")
    user_id = str(input())
    print("\n")
    user_id = user_id + term

    #sending prompt to the server 
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile="ca.crt")
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    send = '+810:' + user_id
    ecmsg = send.encode('ascii')
    ssl_sock.sendall(ecmsg)
    reply = recv_all(ssl_sock)
    reply = reply.replace('.','')
    ssl_sock.close()
    print(str(reply))
    
    print('\nWould you like to search for another employee? Y/N')
    choice = False
    while choice == False:
        answer = input()
        print("\n")
          
        if answer in['y','n','Y','N']:
            choice = True
        else:
            print("Invalid input.") 
            choice = False
                    
                   
    if answer in ['y','Y']:
        db_search()

#remove a user from the database protocol +820
def db_remove(host,port):

    print("Enter Employee ID you would like to remove:")
    user_id = str(input())
    print("\n")
    user_id = user_id + term
    
    #connect to the server
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile="ca.crt")
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    send = '+820:' + user_id
    ecmsg = send.encode('ascii')
    ssl_sock.sendall(ecmsg)
    reply = recv_all(ssl_sock)
    reply = reply.replace('.','')
    print(str(reply))
    ssl_sock.close()

#display all user from the databases protocol +830    
def db_display(host,port):
    
    print('Employee FMS-Display Database')
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile="ca.crt")
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    send = '+830:' + term 
    ecmsg = send.encode('ascii')
    ssl_sock.sendall(ecmsg)
    reply = recv_all(ssl_sock)
    reply = reply.replace('.','')
    print (str(reply))
    #ssl_sock.close()

#quit the program protocol +840   
def db_quit(host,port):
    
    print('Client Signing off~~~')
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile="ca.crt")
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    send = '+840:' + term 
    ecmsg = send.encode('ascii')
    ssl_sock.sendall(ecmsg)
    reply = recv_all(ssl_sock)
    reply = reply.replace('.','')
    ssl_sock.close()
    print(str(reply))
    exit(0)

#used to handle the data being sent from the server to the client
def recv_all(ssl_sock):
    
    commsg = ''
    message = ''
    

    while term not in message:
        commsg = ssl_sock.recv(4096)
        commsg = commsg.decode('ascii')
        message += commsg
        
        
    
    return message


    
    
        
#creating the database in a dictionary and reading from the file       
def create_dictionary():
    d = {}
    f=open("database.txt","r")
    for rec in f:
        rec=rec.strip()
        ID,rest = rec.split(":",1)
        d[ID]=rest.split(":",2)
    return d        
        

#server to handle requests from the client and send information back    
def server(host,port):

    d=create_dictionary()
    user = []
    purpose = ssl.Purpose.CLIENT_AUTH
    context = ssl.create_default_context(purpose, cafile="ca.crt")
    context.load_cert_chain(certfile)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host,port))
    listener.listen(1)

    
    while True:
        print('Listening at interface {!r} and port {}'.format(host, port))
        raw_sock, address = listener.accept()
        print('Connection from host {!r} and port {}'.format(*address))
        ssl_sock = context.wrap_socket(raw_sock, server_side=True)
        message = recv_all(ssl_sock)
        print('\n')
        print('Message says: ', repr(message))
        print('\n')

        #add a user to the database good:+310 bad:-300
        if '+800' in message:
            print(message)
            protocol, user_id, user_first, user_last, user_dep = message.split(':')

            if user_id in d:
                ssl_sock.sendall(b'-300: This user already exists please try again.')
              

            else:
                user.append(user_first)
                user.append(user_last)
                user_dep = user_dep.replace('.','')
                user.append(user_dep)
                d[user_id] = user
                with open("database.txt", "w+")as f:
                    for k,v in d.items():
                        f.write(k + ":" + ":".join(v) + "\n")
                ssl_sock.sendall(b'+310: User successfully added.')
               
           
          
    
        #search for a user in the database good:+410 bad:-400
        elif '+810' in message:
            protocol, user_id = message.split(':')
            user_id = user_id.replace('.','')
            if user_id in d.keys():
                send = "+410: ID:" + user_id + " Name:" + d[user_id][0] +" "+d[user_id][1] + " 			Department:" + d[user_id][2]
                send = send + term
                send = send.encode('ascii')
                ssl_sock.sendall(send)
               
                    
            else:
                ssl_sock.sendall(b"-400: Not a valid Employee ID.")
          
     
        #remove a user from the database good:+510 bad:-500
        elif '+820' in message:
            protocol, user_id = message.split(':')
            user_id = user_id.replace('.','')
            if not user_id in d.keys():
                ssl_sock.sendall(b"-500: Not a valid Employee ID.")
            else:
                ssl_sock.sendall(b"+510: Remove Successful.")
                del d[user_id]
                with open("database.txt", "w+")as f:
                    for k,v in d.items():
                        f.write(k + ":" + ":".join(v) + "\n")
                f.close()
                
        #display the contents of the database good=+610     
        elif '+830' in message:
            ssl_sock.sendall(b'+610:')
            ssl_sock.sendall(b'\n')
            for k in d.keys():
                send = "ID:" + k + " Name:" + d[k][0] +" "+d[k][1] + " Department:" + d[k][2] 
                send = send 
                send = send.encode('ascii')
                ssl_sock.sendall(send)
                ssl_sock.sendall(b'\n')
            ssl_sock.sendall(term.encode('ascii'))
            
                
        elif '+840' in message:

            ssl_sock.sendall(b'Server Signing off~~~.')
            ssl_sock.close()
            print('Socket is now closed.')
            exit(0)

        ssl_sock.close()
        print('Socket is now closed.')




if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=2015,
    help='TCP port (default 2015)')
    parser.add_argument('host', help='hostname or IP address')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

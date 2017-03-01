def assmeble_packet(checksum , seqno , length , data ,l ):
    packet = checksum
    packet += " "
    packet += str(seqno)
    packet += " " 
    for line in data:
        length += len(line)+2
    length -= 2
    print str(length)
    length = length + len(packet)
    length_of_length = len(str(length))
    length = length + length_of_length + 1
    packet += str(length)
    packet += "~"
    packet += l
    return packet;
    


def packet_loss():
    probability = random.random()
    if probability < 0.9:
        return True;
    else:
        return False;


def checkingsum(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest();


def start(filename , ip,port , serversocket):
    print "\n  New Thread Started For "+ip+":"+str(port)
    address = (ip,port)
    f = open(filename,'rb')

    
    #sequence number
    seqno = 0
    l = f.read(BUFFER_SIZE)
    print l
    data = l.splitlines()
    length = 0
    #checksum1 = 0
    checksum = checkingsum(l)
    #checksum = "01110011 " #checksum
    checksum = str(checksum)
    packet = assmeble_packet(checksum , seqno , length , data,l)
    print "TOTAL LENGTH OF STRING" + str(len(packet))
    
    while (l):
        test_probability = packet_loss()
        print str(test_probability)
        if test_probability:
            serversocket.sendto(packet,address)
            print('Sent ',repr(packet))
            current_time = time.time()
            end_time = current_time + 5
            print str(end_time) + "  " + str(current_time)
            while current_time < end_time:
                data , address = serversocket.recvfrom(BUFFER_SIZE_ACK)
                rec = data.split()
                checkackno = rec[1]
                received_checksum = rec[0]
                checksum_ack = checkingsum(rec[1])
                if data and int(checkackno) == seqno and received_checksum == str(checksum_ack):
                    break
                else:
                    current_time = time.time()
                   
            current_time = time.time()
            print data
            
            splitted = packet.split()
            last_sent_seqno = splitted[1]
            print last_sent_seqno + "LAST_SENT_SEQNO"
            #sequence number
            if seqno == 0:
                seqno = 1
            else:
                seqno = seqno + 1
                seqno = seqno % 2 

            l = f.read(BUFFER_SIZE)
            length = 0
            checksum = checkingsum(l)
            #checksum = "01110011 " #checksum
            checksum = str(checksum)
            data = l.splitlines()
            packet = assmeble_packet(checksum , seqno , length , data,l)
            print "TOTAL LENGTH OF STRING" + str(len(packet))
        else:
            time.sleep(5)
    f.close() 
    print('Done sending')   


# server.py
import sys
from socket import *
import os
import random
import time
from threading import Thread
from SocketServer import ThreadingMixIn
from random import randrange
import hashlib


BUFFER_SIZE = 500
BUFFER_SIZE_ACK = 60
checkackno = -1
checksum = '0'
seqno = 0
length = 0
data = ''
packet = ''
l = ''
initial_file = open('server.in','rb')
data = initial_file.read()
data = data.splitlines()
IP_Address=str(data[0])
Port_No = int(data[1])
server_address = ('localhost',Port_No)
serversocket = socket(AF_INET,SOCK_DGRAM)
#serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((IP_Address, Port_No))
#serversocket.listen(5)
threads = []


print 'Server listening....'

while True:                       
    print 'Got connection from', server_address
    data , (ip,port) = serversocket.recvfrom(1024)
    print'Server received : ', repr(data)
    data = data.split()
    spaces = '\n   ***Client Request : '
    #printing out the Request.
    #lw el data feeha 4 kalemat .
    if len(data) == 4:
        req = data[0]
        filename = data[1]
        hostname = data[2]
        portnumber = data[3]
        print spaces,req,filename,hostname,portnumber

    #lw el data feeha 3 kalemat .
    elif len(data) == 3:
        req = data[0]
        filename = data[1]
        hostname = data[2]
        print spaces,req,filename,hostname
    #filename='mytext.txt'

    newthread = Thread(target=start, args=[filename,ip,port,serversocket])
    newthread.start()
    threads.append(newthread) 

    for t in threads:
        t.join()
input()
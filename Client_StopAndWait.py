# client.py

def checkingsum(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest();



from socket import *
import os
import hashlib


initial_file = open('client.in','rb')
data = initial_file.read()
data = data.splitlines()
IP = str(data[0])
port = int(data[1])

address = (IP,port)
socket = socket(AF_INET,SOCK_DGRAM)



#ackno = 0
total_BUUF_SIZE = 560
receivedseqno = 0
expectedseqno = 0
length = '0'
checksum = '01100110'


print '  ****The Commands Syntax should be as follows :'
print '             GET file-name source-host-name (source-port-number)'

request = raw_input("  Request :  ")
request_array = request.split()
req = request_array[0]
if  len(request_array) == 4 or len(request_array) == 3:
    #checks if the request method is only post or get nothing else.
    if req == 'GET' or req == 'get':
        filename_array = request_array[1]
        filename_array = filename_array.split('.')
        filename = filename_array[0] +'_received_from_server'
        filename = filename +'.' + filename_array[1]
        print filename
        socket.sendto(request,address)
    else:
        #if the Request Method isn't get or post
        print '\n  ***Invalid Request Method !!***\n'
else:
    print '\n  ***Invalid Request Method !!***\n'
    
with open(filename, 'wb') as f:
    print 'file opened'
    while True:
        print('receiving data...')
        data , server_address = socket.recvfrom(total_BUUF_SIZE)
        #input()
        #data = packet.split('~',1)[1]
        
        rec = data.split()
        receivedseqno = rec[1]
        packet = data.split('~',1)[1]
        #print('PACKKKEETT=%s', (packet))
            #input()
            #receivedseqno = receivedseqno.split()[1]
        
            #print str(expectedseqno) + " EXPECTED"
            #print str(receivedseqno) + " Received"
        if packet:
            print('data=%s', (packet))
            received_checksum = rec[0]
            checksum = checkingsum(packet)
            if expectedseqno == int(receivedseqno) and received_checksum == checksum:
                ackno = receivedseqno
                #checksum = '01100111'
                #ackpck = checksum + ' ' + str(ackno) + ' '
                #length = len(ackpck)
                #length = len(str(length)) + length

                checksum_ack = checkingsum(str(ackno))
                print str(checksum_ack) + "CHECK SUM OF ACK"
                ackpck = str(checksum_ack) + ' ' + str(ackno) + ' '
                length = len(ackpck)
                length = len(str(length)) + length
                ackpck = ackpck + str(length)
                socket.sendto(ackpck,server_address)
                print ackpck
                expectedseqno = expectedseqno + 1
                expectedseqno = expectedseqno % 2
                    #print str(expectedseqno) + " EXPECTED"


        
        if not data:
            break
            #  write data to a file
        f.write(packet)

f.close()
print('Successfully get the file')
input()
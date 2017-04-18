from xml.dom import minidom
import socket
import sys
import time
from collections import namedtuple
import struct

# read the xml file
xmldoc = minidom.parse('simpletest_v4.xml')
modules = xmldoc.getElementsByTagName('module')

for s in modules:
    moduleID = s.getAttribute('ID') #int
    TestID = s.getElementsByTagName('TestID') #float
    Datatype = s.getElementsByTagName('DataType') #string 
    HandleData = s.getElementsByTagName('HandleData') #varies #string
    IsData = s.getElementsByTagName('IsData') #int
    Log = s.getElementsByTagName('Log') #string
    #Filename = s.getElementsByTagName('Filename') #varies #string
    TimeOut = s.getElementsByTagName('TimeOut') #int
    DataPath = s.getElementsByTagName('DataPath') #varies #string
    LoopCount = s.getElementsByTagName('LoopCount') #int

# For the 2nd command calculate data size of handle command
handlesize=len(str(HandleData[0].firstChild.data))+1
print handlesize




#List of items to be sent
# "Struct" Return a new Struct object which writes and reads binary data according to the format string format

format='i f {}s i i i {}s i'.format(len(str(Datatype[0].firstChild.data))+1,len(str(DataPath[0].firstChild.data))+1)
f=struct.Struct(format)
#f=struct.Struct('i f 6s 37s i i 10s i')

format_status='i f {}s i i i {}s i'.format(len(str(Datatype[0].firstChild.data))+1,len(str(DataPath[0].firstChild.data))+1)
fs=struct.Struct(format_status)

header =(int(moduleID),float(TestID[0].firstChild.data),str(Datatype[0].firstChild.data),handlesize,int(IsData[0].firstChild.data),int(TimeOut[0].firstChild.data),str(DataPath[0].firstChild.data),int(LoopCount[0].firstChild.data))
fd ='{}s'.format(str(HandleData[0].firstChild.data))

data = (str(HandleData[0].firstChild.data))

status =(int(moduleID),float(TestID[0].firstChild.data),"Status",int(0),int(IsData[0].firstChild.data),int(TimeOut[0].firstChild.data),str(DataPath[0].firstChild.data),int(LoopCount[0].firstChild.data))

result =(int(moduleID),float(TestID[0].firstChild.data),"Result",int(0),int(IsData[0].firstChild.data),int(TimeOut[0].firstChild.data),str(DataPath[0].firstChild.data),int(LoopCount[0].firstChild.data))






#To prepare binary data values for transmission
packed_header = f.pack(*header)
#packed_data = fd.pack(*data)
packed_status =fs.pack(*status)
packed_result =fs.pack(*result)

#status=(int(moduleID),float(TestID[0].firstChild.data),)

   # TCP Connection
TCP_IP = '192.168.1.110'
TCP_PORT = 5467
BUFFER_SIZE = 4096
count=0

print data
#Test details sent via tcp connection

#cpickle works but have to deserialize .Check it out

MESSAGE =packed_header
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(MESSAGE)
time.sleep(1)
s.send(data)
recv_data = s.recv(BUFFER_SIZE)
s.close()
print "Daemon:", recv_data
status =1
#has to be recieved by an other thread
while status == 1 :
    STATUS =packed_status
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.sendall(STATUS)
    recv_data = s.recv(BUFFER_SIZE)
    s.close()
    print "Daemon:", recv_data
    time.sleep(1)
    if recv_data == "DONE EXECUT" :
       status =0

STATUS =packed_result
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(STATUS)
recv_data = s.recv(BUFFER_SIZE)
s.close()
print "Daemon: Read Value =", recv_data





from xml.dom import minidom
import socket
import sys
import cPickle
import time
from collections import namedtuple

# read the xml file
xmldoc = minidom.parse('simpletest_v2.xml')
modules = xmldoc.getElementsByTagName('module')

for s in modules:
    moduleID = s.getAttribute('ID')
    TestID = s.getElementsByTagName('TestID')
    Datatype = s.getElementsByTagName('DataType')
    HandleData = s.getElementsByTagName('HandleData')
    IsData = s.getElementsByTagName('IsData')
    DataPath = s.getElementsByTagName('DataPath')
    Log = s.getElementsByTagName('Log')
    Filename = s.getElementsByTagName('Filename')
    TimeOut = s.getElementsByTagName('TimeOut')
    LoopCount = s.getElementsByTagName('LoopCount')

#List of items to be sent
    
    Execution = [ moduleID,TestID[0].firstChild.data, Datatype[0].firstChild.data,
          HandleData[0].firstChild.data,
          IsData[0].firstChild.data, DataPath[0].firstChild.data, Log[0].firstChild.data, Filename[0].firstChild.data,
          TimeOut[0].firstChild.data, LoopCount[0].firstChild.data]
    size=sys.getsizeof( Execution)
#    print(size)
#    print(Execution) # printing unicode string

   # TCP Connection

    TCP_IP = '192.168.1.110'
    TCP_PORT = 5007
    BUFFER_SIZE = 4096
    count=0
    
#Test details sent via tcp connection

#cpickle works but have to deserialize .Check it out

    MESSAGE =HandleData[0].firstChild.data
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.sendall(MESSAGE)
    #s.sendall(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()
    print "Daemon:", data
    status =1
#has to be recieved by an other thread
    while status == 1 :
        STATUS ="Status"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.sendall(STATUS)
        data = s.recv(BUFFER_SIZE)
        s.close()
        print "Daemon:", data
        time.sleep(1)
        if data == "DONE EXECUT" :
           status =0

    STATUS ="Result"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.sendall(STATUS)
    data = s.recv(BUFFER_SIZE)
    s.close()
    print "Daemon: Read Value =", data




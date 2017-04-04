# xmlparsor.py
#
#
# Created by Sudheeshna Karri on 4/1/17.
#
#TODO:
#
#More effitient parsor
#Send the test details ,status requests ,result requests etc in command structure form
#


from xml.dom import minidom
import socket
import sys
import cPickle
import time
from collections import namedtuple

# Parse the xml file

xmldoc = minidom.parse('simpletest_P.xml')
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

   # TCP Commnication
    TCP_IP = '192.168.160.148'
    TCP_PORT = 54673
    BUFFER_SIZE = 4096
    count=0
    
#Test details sent via tcp connection
#cpickle works but have to deserializeat recieving end.Check it out ???

    MESSAGE =HandleData[0].firstChild.data
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.sendall(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()
    print "Daemon:", data
    status =1
    # request for test execution status. IF status is DONE EXECUTION, request for result and read value
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
#Request for result
    STATUS ="Result"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.sendall(STATUS)
    data = s.recv(BUFFER_SIZE)
    s.close()
    print "Daemon: Read Value =", data





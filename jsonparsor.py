
import json
import struct
import socket
import sys
import time
import string
import xlwt

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Results")
Row =1
sheet1.write(0,0,"TEST ID")
sheet1.write(0,1,"TEST RESULT")


from collections import namedtuple
Metro = namedtuple('module', 'ID, TestID, DataType, HandleData, IsData, DataPath, Log,ExpectedResult,TimeOut,LoopCount')

with open('json.json') as json_data:
 d = json.load(json_data)
 
 #Parsing into testcases
 module_tc = [Metro(**k) for k in d['module']]

#print "Number of test cases :" ,len(module_tc)
# testcases count
tc_count = len(module_tc)
handlesize=[]

# Comparing result to determain PASS or FAIL
def compare(s1, s2):
    remove = string.punctuation + string.whitespace + '\n' + '\x00'
    a=s1.translate(None, remove)
    b=s2.translate(None, remove)
    if s1.translate(None, remove) == s2.translate(None, remove):
        return "PASS"
    else:
        return "FAIL"
#return cmp(x,y)




#testcases loop
for mod in range(0,tc_count):
    handlesize.insert(mod,len(module_tc[mod].HandleData))
    header=[]
    #elements of testcases loop
    #for ele in range(0,9):
    #print module_tc[mod][ele]
    #format
    format='i f {}s i i i {}s i'.format(len(module_tc[mod].DataType)+1,len(module_tc[mod].DataPath)+1) # format for Header
    format_sr='i f {}s i i i i i'.format(len(module_tc[mod].DataType)+1) # format for Status & Result
    f=struct.Struct(format)
    fsr=struct.Struct(format_sr)

    # header ,status and result arrays
       

    header =(int(module_tc[mod].ID),float(module_tc[mod].TestID),str(module_tc[mod].DataType),handlesize[mod],int(module_tc[mod].IsData),int(module_tc[mod].TimeOut),str(module_tc[mod].DataPath),int(module_tc[mod].LoopCount))
    #print header
    status =(int(module_tc[mod].ID),float(module_tc[mod].TestID),"Status",int(0),int(0),int(0),int(0),int(0))
    result =(int(module_tc[mod].ID),float(module_tc[mod].TestID),"Result",int(0),int(0),int(0),int(0),int(0))

    # Second Coomand DATA will contain the COMMAND
    data = (str(module_tc[mod].HandleData))

    #To prepare binary data values for transmission
    packed_header = f.pack(*header)
    #packed_data = fd.pack(*data)
    packed_status =fsr.pack(*status)
    packed_result =fsr.pack(*result)

    #status=(int(moduleID),float(TestID[0].firstChild.data),)

    # TCP Connection
    TCP_IP = '192.168.1.107'
    TCP_PORT = 5467
    BUFFER_SIZE = 4096
    count=0

    print "=== TEST ID = ",float(module_tc[mod].TestID), "=========\n"
    print "User Command:", data
    
    
    
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

    expected_output = str(module_tc[mod].ExpectedResult)
    obtained_output = str(recv_data)
    test_Result= compare(expected_output,obtained_output)
    print " TEST RESULT = ",test_Result," \n"

    #Printing all results in excel
    sheet1.write(Row,0,float(module_tc[mod].TestID))
    sheet1.write(Row,1,test_Result)
    Row=Row+1


book.save("Results.xls")














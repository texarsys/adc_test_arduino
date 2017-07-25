import socket
import sys
from thread import *
import wiringpi

# ***********Set up socket *****************************************************
HOST = '192.168.1.155' # Raspberry Pi IP address
PORT = 7777            # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'


# ***********Set up SPI channel to talk to MCP4901*******************************
SPIchannel = 0 #SPI Channel (CE1)
SPIspeed = 5000 #Clock Speed in Hz
wiringpi.wiringPiSetupGpio()
wiringpi.wiringPiSPISetup(SPIchannel, SPIspeed)



def set_voltage_on_dac(volt_sp):
    volt_sp_spi = int(round(volt_sp * 255 / 5.0))
    spi_tx_raw = 0x3000 + (volt_sp_spi << 4)
    spi_tx = chr(spi_tx_raw / 0x100) + chr(spi_tx_raw % 0x100)
    recvData = wiringpi.wiringPiSPIDataRW(SPIchannel, spi_tx)


#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    #conn.send('Welcome to the server. Type bye to exit\n') #send only takes string
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        voltage_req = conn.recv(4096)

        # voltage_req is a string. Convert it to a float and call the set_voltage_on_dac function to set DAC output
        set_voltage_on_dac( float(voltage_req) )

        print voltage_req, type(voltage_req)

        conn.sendall(voltage_req) #send the received data back to the client (PC) so it can confirm.



#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()

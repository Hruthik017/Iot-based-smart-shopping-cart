
import RPi.GPIO as GPIO
from time import sleep  
import serial
from urllib.request import urlopen
import time


EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

def loadread():
    hx = HX711(29, 31)
    hx.set_reading_format("MSB", "MSB")
    #hx.set_reference_unit(92)

    hx.reset()
    
    hx.tare()

    print("Tare done! Add weight now...")

    try:
        val = hx.get_weight(5)
        print(val)
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
    return val

def fward():
    GPIO.output(m1,1)
    GPIO.output(m2,0)
    GPIO.output(m3,1)
    GPIO.output(m4,0)

def bward():
    GPIO.output(m1,0)
    GPIO.output(m2,1)
    GPIO.output(m3,0)
    GPIO.output(m4,1)
        
def stopm():
    GPIO.output(m1,0)
    GPIO.output(m2,0)
    GPIO.output(m3,0)
    GPIO.output(m4,0)
        
def rw():
    GPIO.output(m1,1)
    GPIO.output(m2,0)
    GPIO.output(m3,0)
    GPIO.output(m4,0)

def lw():
    GPIO.output(m1,0)
    GPIO.output(m2,0)
    GPIO.output(m3,1)
    GPIO.output(m4,0)
def revievezigbee():
    status1=0
    SerialPort = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)
    sdata=str(SerialPort.readline(13).decode('utf-8'))
    return(str(sdata))

pr1=0001.25
pr2='0002'
pr3='0003'
pr4='0004'
pr5='0005'
mr1=100
mr2=200
mr3=300
mr4=400
mr5=500
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
ib1=0
ib2=0
ib3=0
ib4=0
ib5=0
ib6=0

m1=40
m2=38
m3=36
m4=32
ir=7
ldrl=15
ldrm=13
ldrr=11
buzz=37
GPIO.setup(buzz,GPIO.OUT)
GPIO.setup(m1,GPIO.OUT)
GPIO.setup(m2,GPIO.OUT)
GPIO.setup(m3,GPIO.OUT)
GPIO.setup(m4,GPIO.OUT)
GPIO.setup(ir,GPIO.IN)
GPIO.setup(ldrl,GPIO.IN)
GPIO.setup(ldrm,GPIO.IN)
GPIO.setup(ldrr,GPIO.IN)


def sendard( tt):
    
    SerialPort = serial.Serial("/dev/ttyUSB1", baudrate=9600, timeout=1)
    SerialPort.write(str.encode('Tea Bag\r'))
    SerialPort.write(str.encode(' '+str(mr1)+'\r'))
    time.sleep(2)
    SerialPort.write(str.encode('Total is'+' '+str(tt)+'\r'))
    
def sendard2( tt):
    
    SerialPort = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
    SerialPort.write('Book \r')
    SerialPort.write(' '+str(mr2)+'\r')
    time.sleep(2)
    SerialPort.write('Total is'+' '+str(tt)+'\r')
    
def sendard3(tt):
    
    SerialPort = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
    SerialPort.write('Perfume \r')
    SerialPort.write(' '+str(mr3)+'\r')
    time.sleep(2)
    SerialPort.write('Total is'+' '+str(tt)+'\r')
    
def sendard4(tt):
    
    SerialPort = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
    SerialPort.write('LED Bulb\r')
    SerialPort.write(' '+str(mr4)+'\r')
    time.sleep(2)
    SerialPort.write('Total is'+' '+str(tt)+'\r')
    
def sendard5(tt):
    
    SerialPort = serial.Serial("/dev/ttyUSB1", baudrate=9600, timeout=1)
    SerialPort.write(str.encode('T Shirt \r'))
    time.sleep(1)
    SerialPort.write(str.encode((' '+str(mr5)+'\r\n')))
    time.sleep(1)
    SerialPort.write(str.encode(('Total is'+' '+str(tt)+'\r\n')))
    time.sleep(1)
    SerialPort.write(str.encode(('\r\n')))
    time.sleep(1)
    SerialPort.write(str.encode(('\r\n')))
    time.sleep(1)
    SerialPort.write(str.encode(('\r\n')))
# main() function
def main():
    # use sys.argv if needed
  
    t=0    
    p=''
    m=''
    t1=''
    #baseURL = 'https://api.thingspeak.com/update?api_key=690S3KXDC270S92Q' 
    WRITE_API = "O3M8H1DWOI6VUZTX" # Replace your ThingSpeak API key here
    BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)


    ThingSpeakPrevSec = 0
    ThingSpeakInterval = 20 # 20 seconds
    while True:
            stopm()
            print('Press 1 for Movement')
            print('Press 2 for Purchase')
            RH=str(input('Press Key 2 select action'))
            while(RH=='1'):
                if(GPIO.input(ldrl)==0):
                    print('Left')
                    lw()
                if(GPIO.input(ldrm)==0):
                    fward()
                    print('Forward')
                if(GPIO.input(ldrr)==0):
                    rw()
                    print('Right')
                if(GPIO.input(ir)==0):
                    stopm()
                    print('stop')
                    RH='0'
                    break;
            while(RH=='2'):
                print('Waiting for RFID Card')
                RH1=revievezigbee()
                print(RH1)
                if(RH1=='5500C91F0B88'):
                    p=pr1
                    m=str(mr1)
                    t=t+mr1+0.25
                    tot=t
                    t1=str(abs(loadread()))
                    print('Product Code is ',str(p))

                    print('Load value is '+str(t1))
                    print ('Price is ',str(tot))
                    #sendart()
                   
                    thingspeakHttp = BASE_URL + "&field1={:.2f}&field2={:.2f}&field3={:.2f}".format(float(pr1), float(t1),float(tot))
                    print(thingspeakHttp)
            
                    conn = urlopen(thingspeakHttp)
                    print("Response: {}".format(conn.read()))
                    conn.close()
                if(RH1=='5500E80A3F88'):
                   GPIO.output(buzz,1)
                   time.sleep(2)
                   GPIO.output(buzz,0)
                   print('Mal Practice is detected')
                if(RH1=='5500B70F52BF'):
                    RH1='aa'
                    sendard5(tot)
                    break
            
       # except:
        #    print 'exiting.'
         #   break

# call main
if __name__ == '__main__':
    main()



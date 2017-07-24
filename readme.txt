1. arduino.py  
   -> The device file for arduino communication
2. raspberry_pi.py
   -> The device file for the raspberry pi
3. sketch_analog_read
   -> the program written using Arduino IDE for reading the voltage at Pin A0
4. Photos folder
   -> The photos of the wiring between the DAC and the Raspberry Pi are put in this folder

The internal 5V ADC reference produced by the Arduino is off by several tens of millivolts compared to the 5V
supply of the Raspberry Pi. This was resulting in a voltage reading error at the arduino pin A0. To overcome 
this problem, the Arduino AREF pin was connected to the 5V supply of the Raspberry pi and the arduino software 
was configured to use the external reference voltage (Refer to the statement: analogReference(EXTERNAL) in the 
arduino code).
# Copyright (C) Texar Systems Private Limited, India - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

# Notes on Usage:
# 1. This device file is meant for communication with the arduino via USB.
#
# 2. The device configuration "Port" can be obtained from the Device manager. E.g, it can be COM2, COM3 etc
#


import math
import socket
import wx

class SocketDevice():
    def __init__(self):
        """
        The constructor of the class
        """

    def setDeviceConfig(self, device_config_dict):
        """
        This action is called by EZPy when 
        1. the device is created
        2. the device config is updated
        """
        ip_address = str(device_config_dict["IP Address"])
        port = int(device_config_dict["Port No"])
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # A single string is used for the AF_UNIX address family. A pair (host, port) is used for the
            # AF_INET address family, where host is a string representing either a hostname in Internet domain
            # notation like 'daring.cwi.nl' or an IPv4 address like '100.50.200.5', and port is an integer.
            #E.g., self.sock.connect(('192.168.1.155', 7777)) #raspberry ip = 192.168.1.155 and port = 7777
            self.sock.connect((ip_address, port))
        except socket.error,msg:
            dlg = wx.MessageDialog(None, str(msg), 'Info',wx.OK)
            dlg.ShowModal()
            raise

    def startOfTestcase(self):
        """
        This action is called at the start of the testcase. The device config parameters to be extracted here for later use.
        """
        pass  # nothing to do here. Hence pass statement is called.

    def endOfTestcase(self):
        """
        This action is called at the end of the testcase
        """
        pass  # nothing to do here. Hence pass statement is called.

    def sendSocket(self, input_dict):
        """
        This action is called from the scheduler window of the testcase. 
        """
        send_value  = float(input_dict["SendValue"])  #sree note the type conversion may need more explanation
        try:
            ret_value=self.sock.sendall(str(send_value))  # blocking until all the bytes are sent;returns none if success
        except socket.error,msg :
            dlg = wx.MessageDialog(None, str( msg),'Info', wx.OK)
            dlg.ShowModal()
            ret_value = 0 #send is a failure

        output_dict = {}
        #if return value is None, then send is success;otherwise failure
        if ret_value == None:
            output_dict["ReturnValue"]   = 1
        else:
            output_dict["ReturnValue"] = 0
        return output_dict

    def recvSocket(self, input_dict):
        """
        This action is called from the scheduler window of the testcase. 
        """
        try:
            recv_value = self.sock.recv(4096)  # by default its blocking,so it wil go to next line after receiving data
        except socket.error,msg:
            dlg = wx.MessageDialog(None, str( msg),'Info', wx.OK)
            dlg.ShowModal()
            recv_value = 0 #check what to do in case of connection error in between

        output_dict = {}
        output_dict["RecvValue"] = recv_value
        return output_dict

    @classmethod
    def getDeviceDict(cls):
        """
        This method defines the parameters for
        1. the device config window
        2. all the action config windows
        """
        tmp_device_dict = {}                 # initialise the device dictionary to an empty dictionary
        tmp_device_dict["Version"] = "1.0"   # version of the device file.

        # ******************** Device config window definition **********************************************************
        # This part of the code defines the "Device Config Window". The users need to modify only the first statement
        # below to include any configuration needed for the device. This first statement can also be an empty dictionary
        # in case no configuration is needed for the device
        tmp_device_config_dict={"IP Address" : " ", "Port No": " "} # users need to edit this statement to include all the configurations of this device
        tmp_device_dict["DeviceConfig"]=tmp_device_config_dict      # do not modify this statement.
        # ***************************************************************************************************************


        # ******************** Action config window definitions *********************************************************
        tmp_device_dict["Actions"] = {}                              # do not modify.

        # Add action configuration
        tmp_action_name = "sendSocket"
        tmp_action_inp_dict = {"SendValue"   : ""}
        tmp_action_out_dict = {"ReturnValue"   : ""}
        tmp_device_dict["Actions"][tmp_action_name] = [tmp_action_inp_dict, tmp_action_out_dict]  # do not modify


        tmp_action_name = "recvSocket"
        tmp_action_inp_dict = {}
        tmp_action_out_dict = {"RecvValue": "" }
        tmp_device_dict["Actions"][tmp_action_name] = [tmp_action_inp_dict, tmp_action_out_dict]  # do not modify
        # ***************************************************************************************************************

        return tmp_device_dict
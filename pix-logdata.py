#!/usr/bin/env python
""" Drone Pilot - Control of MRUAV """
""" pix-logdata.py -> Script that logs data from a vehicle and a MoCap system. DroneApi related. """

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2015 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__maintainer__ = "Kyle Brown"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

# Dependencies
# * This script assumes that the pixhawk is connected to the raspberry pi via the serial port (/dev/ttyAMA0)
# * In our setup, telemetry port 2 is configured at 115200 on the pixhawk

# Usage:
# * mavproxy.py --master=/dev/ttyAMA0 --baudrate 115200 --aircraft TestQuad
# * module load api
# * api start pix-logdata.py

import time, threading, csv, datetime

'''  To import own modules, you need to export the current path before importing the module.    '''
'''  This also means that mavproxy must be called inside the folder of the script to be called. ''' 
import os, sys
sys.path.append(os.getcwd())
import modules.UDPserver as udp
import modules.utils as utils
import modules.pixVehicle

# Vehicle initialization
api = local_connect()
vehicle = api.get_vehicles()[0]

# Function to manage data, print it and save it in a log 
def logit():
    try:
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%m_%d_%H-%M-%S')+".csv"
        f = open("logs/"+st, "w")
        logger = csv.writer(f)
        logger.writerow(('timestamp','roll','pitch','yaw','vx','vy','vz','rc1','rc2','rc3','rc4','x','y','z'))
        while True:
            # Print message
            print "Roll = %0.4f Pitch = %0.4f Yaw= %0.4f" % (vehicle.attitude.roll, vehicle.attitude.pitch, vehicle.attitude.yaw)
            print "Vx = %0.4f Vy = %0.4f Vz= %0.4f" % (vehicle.velocity[0], vehicle.velocity[1], vehicle.velocity[2])
            print "RC1 = %d RC2 = %d RC3 = %d  RC4 = %d " % (vehicle.channel_readback['1'], vehicle.channel_readback['2'], vehicle.channel_readback['3'], vehicle.channel_readback['4'])
            print "X = %0.2f Y = %0.2f Z = %0.2f" % (udp.message[5], udp.message[4], udp.message[6])
            # Save log
            if udp.active:
                logger.writerow((time.time(), \
                                 vehicle.attitude.roll, vehicle.attitude.pitch, vehicle.attitude.yaw, \
                                 vehicle.velocity[0], vehicle.velocity[1], vehicle.velocity[2], \
                                 vehicle.channel_readback['1'], vehicle.channel_readback['2'], vehicle.channel_readback['3'], vehicle.channel_readback['4'], \
                                 udp.message[5], udp.message[4], udp.message[6] ))
            time.sleep(0.01) # To record data at 100hz exactly
    except Exception,error:
        print "Error in logit thread: "+str(error)
        f.close()


""" Section that starts the script """

udp.startTwisted()

while True:
	if vehicle.armed and modules.UDPserver.active:
		logit()
	else:
		print "Waiting for vehicle to be armed and/or UDP server to be active..."
		time.sleep(0.5)






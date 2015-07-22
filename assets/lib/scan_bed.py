# bed scan tool
import time
import sys, os
import serial
from subprocess import call
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np


#Args
try:
        resultfile=str(sys.argv[1]) 	# resulting image
        log_trace=str(sys.argv[2])      # UI text

except:
        print "Missing parameters"

#No Args
cycle=True
s_warning=s_error=s_skipped=0

#points to probe
probed_points=np.array([[22,66.5,0],[22,84.44,0],[22,102.38,0],[22,120.31,0],[22,138.25,0],[22,156.19,0],[22,174.13,0],[22,192.06,0],[22,210,0],[42.25,66.5,0],[42.25,84.44,0],[42.25,102.38,0],[42.25,120.31,0],[42.25,138.25,0],[42.25,156.19,0],[42.25,174.13,0],[42.25,192.06,0],[42.25,210,0],[62.5,66.5,0],[62.5,84.44,0],[62.5,102.38,0],[62.5,120.31,0],[62.5,138.25,0],[62.5,156.19,0],[62.5,174.13,0],[62.5,192.06,0],[62.5,210,0],[82.75,66.5,0],[82.75,84.44,0],[82.75,102.38,0],[82.75,120.31,0],[82.75,138.25,0],[82.75,156.19,0],[82.75,174.13,0],[82.75,192.06,0],[82.75,210,0],[103,66.5,0],[103,84.44,0],[103,102.38,0],[103,120.31,0],[103,138.25,0],[103,156.19,0],[103,174.13,0],[103,192.06,0],[103,210,0],[123.25,66.5,0],[123.25,84.44,0],[123.25,102.38,0],[123.25,120.31,0],[123.25,138.25,0],[123.25,156.19,0],[123.25,174.13,0],[123.25,192.06,0],[123.25,210,0],[143.5,66.5,0],[143.5,84.44,0],[143.5,102.38,0],[143.5,120.31,0],[143.5,138.25,0],[143.5,156.19,0],[143.5,174.13,0],[143.5,192.06,0],[143.5,210,0],[163.75,66.5,0],
[163.75,84.44,0],[163.75,102.38,0],[163.75,120.31,0],[163.75,138.25,0],[163.75,156.19,0],[163.75,174.13,0],[163.75,192.06,0],[163.75,210,0],[184,66.5,0],[184,84.44,0],[184,102.38,0],[184,120.31,0],[184,138.25,0],[184,156.19,0],[184,174.13,0],[184,192.06,0],[184,210,0]])

#probed_points=np.array([[5+17,5+61.5,0],[5+17,148.5+61.5,0],[178+17,148.5+61.5,0],[178+17,5+61.5,0]])

serial_reply=""

#num of probes each point
num_probes=4

from geometry import Point, Line, Plane

def trace(string):
        global log_trace
        out_file = open(log_trace,"a+")
        out_file.write(str(string) + "\n")
        out_file.close()
        #headless
        print string
        return
     
def read_serial(gcode):
	serial.flushInput()
	serial.write(gcode + "\r\n")
	time.sleep(0.1)
	
	#return serial.readline().rstrip()
	response=serial.readline().rstrip()
	
	if response=="":
		return "NONE"
	else:
		return response
		
def macro(code,expected_reply,timeout,error_msg,delay_after,warning=False,verbose=True):
	global s_error
	global s_warning
	global s_skipped
	serial.flushInput()
	if s_error==0:
		serial_reply=""
		macro_start_time = time.time()
		serial.write(code+"\r\n")
		time.sleep(0.3) #give it some tome to start
		while not (serial_reply==expected_reply or serial_reply[:4]==expected_reply):
			#Expected reply
			#no reply:
			if (time.time()>=macro_start_time+timeout+5):
				if serial_reply=="":
					serial_reply="<nothing>"
				if not warning:
					s_error+=1
				else:
					s_warning+=1
				return False #leave the function
			serial_reply=serial.readline().rstrip()
			#add safety timeout
			time.sleep(0.2) #no hammering
			pass
		time.sleep(delay_after) #wait the desired amount
	else:
		s_skipped+=1
		return False
	return serial_reply

#trace(resultfile)
#trace(log_trace)

#heated_bed=[[22.0,66.5,37.5825],[22.0,84.44,37.525],[22.0,102.38,37.4975],[22.0,120.31,37.5075],[22.0,138.25,37.5225],[22.0,156.19,37.5225],[22.0,174.13,37.56],[22.0,192.06,37.5975],[22.0,210.0,37.5775],[42.25,66.5,37.56],[42.25,84.44,37.5025],[42.25,102.38,37.5175],[42.25,120.31,37.4975],[42.25,138.25,37.51],[42.25,156.19,37.53],[42.25,174.13,37.5725],[42.25,192.06,37.595],[42.25,210.0,37.57],[62.5,66.5,37.545],[62.5,84.44,37.495],[62.5,102.38,37.48],[62.5,120.31,37.4775],[62.5,138.25,37.52],[62.5,156.19,37.5225],[62.5,174.13,37.55],[62.5,192.06,37.5725],[62.5,210.0,37.58],[82.75,66.5,37.525],[82.75,84.44,37.4775],[82.75,102.38,37.47],[82.75,120.31,37.495],[82.75,138.25,37.5175],[82.75,156.19,37.5425],[82.75,174.13,37.5425],[82.75,192.06,37.58],[82.75,210.0,37.55],[103.0,66.5,37.5275],[103.0,84.44,37.495],[103.0,102.38,37.47],[103.0,120.31,37.485],[103.0,138.25,37.515],[103.0,156.19,37.55],[103.0,174.13,37.535],[103.0,192.06,37.5675],[103.0,210.0,37.56],[123.25,66.5,37.5225],[123.25,84.44,37.475],[123.25,102.38,37.495],[123.25,120.31,37.5125],[123.25,138.25,37.54],[123.25,156.19,37.555],[123.25,174.13,37.55],[123.25,192.06,37.58],[123.25,210.0,37.5675],[143.5,66.5,37.525],[143.5,84.44,37.5125],[143.5,102.38,37.5025],[143.5,120.31,37.5275],[143.5,138.25,37.555],[143.5,156.19,37.5575],[143.5,174.13,37.5725],[143.5,192.06,37.605],[143.5,210.0,37.5925],[163.75,66.5,37.5325],[163.75,84.44,37.5075],[163.75,102.38,37.5025],[163.75,120.31,37.525],[163.75,138.25,37.55],[163.75,156.19,37.59],[163.75,174.13,37.5775],[163.75,192.06,37.5875],[163.75,210.0,37.5825],[184.0,66.5,37.565],[184.0,84.44,37.5175],[184.0,102.38,37.54],[184.0,120.31,37.54],[184.0,138.25,37.555],[184.0,156.19,37.58],[184.0,174.13,37.6],[184.0,192.06,37.6025],[184.0,210.0,37.6]]

heated_bed = np.empty(probed_points.shape)

trace("Bed scan wizard Initiated")
port = '/dev/ttyAMA0'
baud = 115200

#initialize serial
serial = serial.Serial(port, baud, timeout=0.6)
serial.flushInput()

#macro("M741","TRIGGERED",2,"Front panel door control",1, verbose=False)	
macro("M402","ok",2,"Retracting Probe (safety)",1, warning=True, verbose=False)	
macro("G27","ok",100,"Homing Z - Fast",0.1)	

macro("G90","ok",5,"Setting abs mode",0.1, verbose=False)
macro("G92 Z241.2","ok",5,"Setting correct Z",0.1, verbose=False)
#M402 #DOUBLE SAFETY!
macro("M402","ok",2,"Retracting Probe (safety)",1, verbose=False)	
macro("G0 Z60 F5000","ok",5,"Moving to start Z height",10) #mandatory!


for (p,point) in enumerate(probed_points):

	#real carriage position
	x=point[0]-17
	y=point[1]-61.5
	macro("G0 X"+str(x)+" Y"+str(y)+" Z45 F10000","ok",15,"Moving to Pos",3, warning=True,verbose=False)		
	#msg="Measuring point " +str(p+1)+ "/"+ str(len(probed_points)) + " (" +str(num_probes) + " times)"
	#trace(msg)
	#Touches 4 times the bed in the same position
	probes=num_probes #temp

	temp=np.zeros(4);
	for i in range(0,num_probes):
		
		#M401
		macro("M401","ok",2,"Lowering Probe",1, warning=True, verbose=False)	
		
		serial.flushInput()
		#G30	
		serial.write("G30\r\n")
		#time.sleep(0.5)			#give it some to to start  
		probe_start_time = time.time()
		while not serial_reply[:22]=="echo:endstops hit:  Z:":
			serial_reply=serial.readline().rstrip()	
			#issue G30 Xnn Ynn and waits reply.
			if (time.time() - probe_start_time>20):  #timeout management
#				trace("Probe failed on this point")
				probes-=1 #failed, update counter
				break	
			pass
		
		#print serial_reply
		#get the z position
		if serial_reply!="":
			z=float(serial_reply.split("Z:")[1].strip())
			#trace("probe no. "+str(i+1)+" = "+str(z) )
			probed_points[p,2]+=z # store Z
			temp[i]=z;
			
		serial_reply=""
		serial.flushInput()
		
		#G0 Z40 F5000
		macro("G0 Z50 F5000","ok",10,"Rising Bed",1, warning=True, verbose=False)
		
	#mean of the num of measurements
	probed_points[p,0]=probed_points[p,0]
	probed_points[p,1]=probed_points[p,1]
	probed_points[p,2]=probed_points[p,2]/probes; #mean of the Z value on point "p"
	
	#trace("Mean ="+ str(probed_points[p,2]))
	
	#msg="Point " +str(p+1)+ "/"+ str(len(probed_points)) + " , Z= " +str(probed_points[p,2])
	#trace(msg)
	#print point[0], point[1], probed_points[p,2], temp[0], temp[1], temp[2], temp[3]  
	msg="Point "+str(p+1)+"(X,Y,avg(Z),Z1,Z2,Z3,Z4):"+str(point[0]) +","+ str(point[1])+","+str(probed_points[p,2])+","+str(temp[0])+","+str(temp[1])+","+str(temp[2])+","+str(temp[3])  
	trace(msg)
	macro("M402","ok",2,"Raising Probe",1, warning=True, verbose=False)	

	heated_bed[p,0]= point[0]
	heated_bed[p,1]= point[1]
	heated_bed[p,2]= probed_points[p,2]

	#G0 Z40 F5000
	macro("G0 Z50 F5000","ok",2,"Rising Bed",0.5, warning=True, verbose=False)
	
#now we have all the 4 points.
macro("G0 X5 Y5 Z50 F10000","ok",2,"Idle Position",0.5, warning=True, verbose=False)

macro("M18","ok",2,"Motors off",0.5, warning=True, verbose=False)

#sys.setrecursionlimit(10000)
#heated_matrix=matrix(heated_bed);
heated_matrix=np.asmatrix(heated_bed);

#print heated_bed
#print heated_matrix

fig = plt.figure()
ax111 = fig.gca()

X = np.reshape(heated_matrix[:,0], (9, 9))
Y = np.reshape(heated_matrix[:,1], (9, 9))

#print X
#print Y

#X = heated_matrix[::9,0]
#Y = heated_matrix[0:9,1]
#X, Y = np.meshgrid(X, Y)

Z = np.reshape(heated_matrix[:,2], (9, 9))

#print Z

X=np.array(X,dtype=object)
Y=np.array(Y,dtype=object)
Z=np.array(Z,dtype=object)

l1 = ax111.contourf(X, Y, Z, interpolation='nearest')
ax111.figure.colorbar(l1) # axes: 
ax111.axis('equal') # labels: 
ax111.set_xlabel(ur"$x$ axis (mm)") 
ax111.set_ylabel(ur"$y$ axis (mm)") 
ax111.set_title("Probed value along the heated bed") 
ax111.set_xlim(0,223)
ax111.set_ylim(0,235)

#fig.tight_layout()

plt.savefig(resultfile)
#html("<img src='cell://test2.png' />")


#end
trace("Done!")
sys.exit()

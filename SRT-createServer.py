
## OneView Automation
##https://github.com/dderichswei/synergy/blob/master/Synergy%20Roundtable.ipynb


# import python-OneView Library
from hpOneView.oneview_client import OneViewClient

import sys
import os
import paramiko
import datetime
import time


import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")


# login to OneView Appliance
config = {
    "api_version": "500",
    "ip": "10.0.20.50",
    "credentials": {
        "userName": "python",
        "authLoginDomain": "local",
        "password": "python123!"
    }
}
oneview_client = OneViewClient(config)


# create an network
options = {
    "name": "Roundtable - Test Ethernet Network",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None
}

try: 
	ethernet_network = oneview_client.ethernet_networks.create(options)
	print("Created ethernet-network " + ethernet_network['name'] + "   URI: " + ethernet_network['uri'] + "successfully.")

	
except:
	print (" Network already there" )

###name = input("network created !? ")   # Python 3

# create an server by deploying an Server Profile w I3S

# define variables for power state of server
powerOn = {
    "powerState": "On",
    "powerControl": "MomentaryPress"
}

powerOff = {
    "powerState": "Off",
    "powerControl": "PressAndHold"
}


#template_name = "Roundtable - API Demo Template (DirkD)"
template_name = "Roundtable - Python (DirkD)"
server_name = "Roundtable - API Demo Server (DirkD)"

# server_hardware_uri = '/rest/server-hardware/39313738-3133-5A43-4A37-343030373931' # SY660 G10
server_hardware_uri = '/rest/server-hardware/39313738-3134-5A43-4A37-343030373536' # SY480
server_template_uri = oneview_client.server_profile_templates.get_by_name(template_name)

# power off Server, just to be sure it is off
server_power = oneview_client.server_hardware.update_power_state(powerOff, server_hardware_uri) 

#create Server Profile from template, change some os deployment parameters
try:
    print ("create server profile at " + str(datetime.datetime.now()))
    roundtable_server = oneview_client.server_profile_templates.get_new_profile(server_template_uri['uri'])
    roundtable_server["name"] = server_name
    roundtable_server["serverHardwareUri"] = server_hardware_uri

    for name in roundtable_server["osDeploymentSettings"]["osCustomAttributes"]:
        if (name['name'] == "NewUser"):
            name['value']= "dirk"
        if (name['name'] == "NewUserPassword"):
            name['value']= "HalloRoundtable!"   
    profile = oneview_client.server_profiles.create(roundtable_server)

    
except:
    print(server_name + " Server already exists")

#power on Server and boot ....	
print ("Power on server " + str(datetime.datetime.now()))
server_power = oneview_client.server_hardware.update_power_state(powerOn, server_hardware_uri) # turn on server



# configure nxinx in the newly created server

deployed_server = oneview_client.server_profiles.get_by_name(server_name)

for name in deployed_server["osDeploymentSettings"]["osCustomAttributes"]:
    if (name['name'] == "Team0NIC1.ipaddress"):
        ip_address = name['value']

# wait until Server is up .....
waiting=True
while waiting:
	counter=0
	t = os.system('ping '+ip_address)
	if not t:
		time.sleep(10)
		waiting=False
	else:
		counter +=1
		if counter == 100:
			waiting = False 
		print("waiting to finish boot")

#####name = input("server booted !? ")  

ssh = paramiko.SSHClient()

server_name = "Roundtable - API Demo Server (DirkD)"
username = 'root'
password = 'Compaq1!'


        
print("Login with user: " + username + " Server:" + ip_address)        
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())         # add unknown Host-Keys
ssh.connect(ip_address, username=username, password=password)     # login
ssh.exec_command('docker run -d --name nginx -p 80:80 nginx')
time.sleep(10)
stdin, stdout, stderr = ssh.exec_command("docker exec -it nginx sed -i '\''s/nginx/the Synergy Roundtable/g'\'' /usr/share/nginx/html/index.html", get_pty=True)
time.sleep(10)
stdin, stdout, stderr = ssh.exec_command("docker exec -it nginx sed -i '\''s/nginx/the Synergy Roundtable/g'\'' /usr/share/nginx/html/index.html", get_pty=True)

print(" ")
print("http://" + ip_address)

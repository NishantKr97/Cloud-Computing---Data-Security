import netifaces as ni
import socket
import os

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_subnet_mask(myIpAddress):
	subnet = myIpAddress[:-3]
	subnet = subnet + "000"
	return subnet

def inputIPAddress():
	ipAddress = input("Enter the IP address to access Login Page : ")
	return ipAddress

def inputPortAddress():
	inputPort = input("Enter the Port No. to access Login Page : ")
	return inputPort

def checkSubnetAccess(myIpAddress, subnet, inputIP, inputPort):
	myIpSubnet = inputIP[:-3]
	mySubnet = subnet[:-3]
	flag = 1
	if mySubnet != myIpSubnet:
		flag = 0

	return flag

def checkPublicNetworkAccess(myIpAddress, subnet, inputIP, inputPort):
	myIpClass = inputIP[0:1]
	mySubnet = subnet[:-3]
	flag = 1
	if myIpClass == 0:
		flag = 0
	
	return flag


def checkPortAccess(myIpAddress, subnet, inputIP, inputPort):
	myIpSubnet = inputIP[:-3]
	mySubnet = subnet[:-3]
	flag = 1
	if int(inputPort) <= 1024 or int(inputPort) > 65535:
		flag = 0

	return flag	

def checkSMTPAccess(myIpAddress, subnet, inputIP, inputPort):
	myIpSubnet = inputIP[:-3]
	mySubnet = subnet[:-3]
	flag = 0
	if inputPort == 25:
		flag = 1

	return flag 

def checkICMPAccess(myIpAddress, subnet, inputIP, inputPort):
	myIpSubnet = inputIP[:-3]
	mySubnet = subnet[:-3]
	flag = 0
	if inputPort == 7:
		flag = 1

	return flag 	

def checkTelnetAccess(myIpAddress, subnet, inputIP, inputPort):
	myIpSubnet = inputIP[:-3]
	mySubnet = subnet[:-3]
	flag = 0
	if inputPort == 23:
		flag = 1

	return flag 

def checkHTTPAccess(myIpAddress, subnet, inputIP, inputPort):
	myIpSubnet = inputIP[:-3]
	mySubnet = subnet[:-3]
	flag = 0
	if inputPort == 80:
		flag = 1

	return flag 

def main():
	myIpAddress = get_ip_address() 
	print("IP Address : " + myIpAddress)
	subnet = get_subnet_mask(myIpAddress)
	inputIP = inputIPAddress()
	inputPort = inputPortAddress()
	accessRule1 = checkSubnetAccess(myIpAddress, subnet, inputIP, inputPort)
	accessRule2 = checkPublicNetworkAccess(myIpAddress, subnet, inputIP, inputPort)
	accessRule3 = checkPortAccess(myIpAddress, subnet, inputIP, inputPort)
	accessRule4 = checkSMTPAccess(myIpAddress, subnet, inputIP, inputPort)
	accessRule5 = checkICMPAccess(myIpAddress, subnet, inputIP, inputPort)
	accessRule6 = checkTelnetAccess(myIpAddress, subnet, inputIP, inputPort)
	accessRule7 = checkHTTPAccess(myIpAddress, subnet, inputIP, inputPort)

	if (accessRule1 and accessRule2 and accessRule3) or accessRule4 or accessRule5 or accessRule6 or accessRule7:
		print("Loading...")
		for i in range(0, 100000000):
			pass
		# os.system("firefox https://ieeexplore.ieee.org/abstract/document/7299312")
		os.system("firefox http://0.0.0.0:8080/")
	else:
		print("Error signing in!!!")




if __name__ == '__main__':
	main()


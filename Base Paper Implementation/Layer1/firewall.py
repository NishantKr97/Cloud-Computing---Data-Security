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

def checkAccess(myIpAddress, subnet, inputIP, inputPort):
	myIpSubnet = inputIP[:-3]
	mySubnet = subnet[:-3]
	flag = 1
	if mySubnet != myIpSubnet:
		flag = 0
	if int(inputPort) <= 1024 or int(inputPort) > 65535:
		flag = 0

	if flag == 1:
		return True
	else:
		return False


def main():
	myIpAddress = get_ip_address() 
	print("IP Address : " + myIpAddress)
	subnet = get_subnet_mask(myIpAddress)
	inputIP = inputIPAddress()
	inputPort = inputPortAddress()
	access = checkAccess(myIpAddress, subnet, inputIP, inputPort)
	if access:
		print("Loading...")
		for i in range(0, 100000000):
			pass
		os.system("firefox https://ieeexplore.ieee.org/abstract/document/7299312")
	else:
		print("Error signing in!!!")



if __name__ == '__main__':
	main()


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
	print("Your Subnet is : " + subnet)

def inputIPAddress(myIpAddress):
	ipAdress = input("Enter the IP address to access Login Page : ")
	
	print("Your IP Address is : " + myIpAddress)
	get_subnet_mask(myIpAddress)
	print("Loading...")
	for i in range(0, 100000000):
		pass
	# os.system("firefox https://ieeexplore.ieee.org/abstract/document/7299312")



def main():
	myIpAddress = get_ip_address() 
	inputIPAddress(myIpAddress)

if __name__ == '__main__':
	main()
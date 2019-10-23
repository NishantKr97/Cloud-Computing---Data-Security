import netifaces as ni
import socket
import os

# FIREWALL AUTHENTICATION


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_subnet_mask(myIpAddress):
	# subnet = myIpAddress[:-3]
	# subnet = subnet + "000"
	# return subnet
	return myIpAddress

def inputIPAddress():
	ipAddress = input("Enter the IP address to access Login Page : ")
	return ipAddress

def inputPortAddress():
	inputPort = input("Enter the Port No. to access Login Page : ")
	print("\n        ||\n        ||\n        ||\n        ||\n        ||\n        ||\n       \  /\n        \/\n")
	return inputPort

def checkAccess(myIpAddress, subnet, inputIP, inputPort):
	l1 = len(subnet)
	l2 = len(inputIP)

	# print (subnet, inputIP, l1, l2)

	x = l1 - 1
	j = 0
	# print (l2)

	while subnet[x] != '.':
		x -= 1
	# print (x)
	# for x in range(l1 - 1, 0, -1):
	# 	if subnet[x] == '.':
	# 		print (x)
	# 		break
	for j in range(l2 - 1, 0, -1):
		if inputIP[j] == '.':
			# print (j)
			break
	myIpSubnet = inputIP[:j]
	mySubnet = subnet[:x]


	# myIpSubnet = inputIP[:-3]
	# mySubnet = subnet[:-3]

	# print(mySubnet, myIpSubnet)
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

	rsa_key = input("Enter the RSA key : ")
	print("\n        ||\n        ||\n        ||\n        ||\n        ||\n        ||\n       \  /\n        \/\n")
	if(rsa_key == "8037427191231280"):
		print(".......................................................................\n| Authorized Key -> Welcome to the Firewall Authentication Step!!!    |\n....................................................................... ")
		myIpAddress = get_ip_address() 
		for i in range(0, 100000000):
			pass
		print("\n_______________________________________________________________________\nValid IP Address : " + myIpAddress + "\n_______________________________________________________________________\n")
		subnet = get_subnet_mask(myIpAddress)
		inputIP = inputIPAddress()
		inputPort = inputPortAddress()
		access = checkAccess(myIpAddress, subnet, inputIP, inputPort)
		if access:
			print("\n.......................................................................\n| Authorized Login -> This may take some time.                        |\n| Loading...                                                          |")
			for i in range(0, 100000000):
				pass
			print(".......................................................................")
			for i in range(0, 10000000):
				pass
			# os.system("firefox file:///home/nishantkr97/Documents/Projects/Cloud-Computing---Data-Security/Base%20Paper%20Implementation/Layer2/home.html")
			os.system("python intrusion_test.py")			
		else:
			print("\n.......................................................................\n|                        Error signing in!!!                          |\n....................................................................... ")
	else:
		print("Invalid RSA Key!!!")
	





if __name__ == '__main__':
	main()


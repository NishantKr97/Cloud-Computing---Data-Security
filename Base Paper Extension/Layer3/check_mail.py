


def main():
	username = input("Enter username:")
	password = input("Enter password:")

	dict = {"admin1" : "pass1", "admin2" : "pass2", "admin3" : "pass3", "admin4" : "pass4", "admin5" : "pass5"}

	if username in dict and password == dict[username]:
		print ("Login Successful")

	else:
		print ("Login Unsuccessful")

	# senderEmail = input("Enter sender email")
	# receiverEmail = 

	print ("WELCOME TO GOOGLE GROUP")

	for i in range(0, 100000000):
		pass

	print ("Checking Inbox for any new Mail....")

	for i in range(0, 100000000):
		pass

	print ("You have a new mail!!!\n\n")

	file1 = open("myfile.txt","r+")
	print (file1.read())
	file1.close()

if __name__ == '__main__':
	main()
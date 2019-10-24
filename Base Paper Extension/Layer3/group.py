import hashlib 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import imageio

quantization_table = [[16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [68, 56, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]]


def convert(char):
    return format(ord(char), '09b')


# In[17]:


def dct(image, data):
    image_data = image.astype(float)
    m, n = image_data.shape
    image_dct = np.zeros(image.shape)
    x_division = int(m/8)
    y_division = int(n/8)
#     print ('m = ', m)
#     print ('n = ', n)
#     print (x_division)
#     print (y_division)
    
    lis_dct = []
    x = 0
    F = 0
    lis_F = []
    TF = 0.1
    lis_selected = []
    
    T = 0.2
    TL = 0.2
    TH = 0.3
    
    pointer = 0
    
    avg = 0
    
    eof = 0
    
    a = 0
    
#     f = open("Data.txt","r")
#     string = f.read()
#     print (string)
    
#     data = ''
#     for i in string:
#         data += convert(i)
#     print (string)
#     print (data)
    

    for i in range(0, x_division):
        for j in range(0, y_division):
            x_s = i * 8
            x_e = (i+1) * 8
            y_s = j * 8
            y_e = (j+1) * 8
            image_dct[x_s:x_e, y_s:y_e] = cv2.dct(image_data[x_s:x_e,y_s:y_e]) / quantization_table
            lis_dct = cv2.dct(image_data[x_s:x_e,y_s:y_e]) / quantization_table
            y = 0
            sum_coeff = 0
            avg = 0
            
            if eof == 0:
            
                for l in lis_dct:
                    for k in l:
                        if y == 0:
                            y += 1
                            continue
                        else:
                            y += 1
                            sum_coeff += (k * k)
                            avg += k
    #             print ('sum_coeff = ', sum_coeff)
                F = sum_coeff/64
                avg /= 64
                # Indexes of selected blocks inserted in a list, useful while traversing later
                if F < TF:
                    lis_selected.append((i, j))

                    """ Embedding Code Start """
                    for l in range(0, 8):
                        for m in range(0, 8):
                            k = lis_dct[l][m]
#                             print (k)
    #                         x = k
                            if T >= 0:
            #                     print ("IN1")
            #                     print (abs(x - T))
                                if abs(k - T) <= 0.1 and k < TH and k > TL:
                                    current = 0
#                                     print ("IN2")

                                    if pointer == len(data):
#                                         print ("End of file")
                                        eof = 1
                                        break    

                                    c = data[pointer]
                                    pointer += 1
#                                     print ("Read a character:", c)
#                                     print ("Old K: ", k)
                                    if c == '0':
                                        k += 2
                                        lis_dct[l][m] += 2
                                        image_dct[x_s:x_e, y_s:y_e] = lis_dct
#                                         print (l, m)
                                    elif c == '1':
                                        k += 3
                                        lis_dct[l][m] += 3
                                        image_dct[x_s:x_e, y_s:y_e] = lis_dct
#                                         print (l, m)
#                                     print ("New K: ", k)

                                elif (k - T) > 0.1:
                                    k += 1
                                    lis_dct[l][m] += 1
                                    image_dct[x_s:x_e, y_s:y_e] = lis_dct
    #                                 print (k)

                            else:
                                print ("OUT1")
                                if abs(k - T) <= 0.1 and k < TH and k > TL:
                                    current = 0
                                    print ("OUT2")

                                    if pointer == len(data):
                                        print ("End of file")
                                        eof = 1
                                        break

                                    c = data[pointer]
                                    print ("Read a character:", c)
                                    pointer += 1
#                                     print ("Old K: ", k)
                                    if c == '0':
                                        k = -2 - k
                                        lis_dct[l][m] = -2 - lis_dct[l][m]
                                        image_dct[x_s:x_e, y_s:y_e] = lis_dct
                                        print (l, m)
                                    elif c == '1':
                                        k = -3 - k
                                        lis_dct[l][m] = -3 - lis_dct[l][m]
                                        image_dct[x_s:x_e, y_s:y_e] = lis_dct
                                        print (l, m)
#                                     print ("New K: ", k)

                                elif (k - T) < 0.1:
                                    k = -1 - k
                                    lis_dct[l][m] = -1 - lis_dct[l][m]
                                    image_dct[x_s:x_e, y_s:y_e] = lis_dct
                    """ Embedding Code Finish """


                lis_F.append(F)
    #             if x < 5:
    #                 print (F)
    #                 print (lis_dct)
    #                 print (avg)
    #                 x += 1
    #                 print ('y = ', y)

#     print ("Avg is ", sum(lis_F) / len(lis_F))
#     print (lis_F)
#     print (data)
#     print ("Length of lis_F = ", len(lis_F))
#     print ("Length of lis_selected = ", len(lis_selected))
#     print (lis_selected)
    return image_dct


def sha256(message):
	result = hashlib.sha256(message.encode()) 
	return result.hexdigest() 


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

	message = input("Type email to be sent:")
	encrypted = sha256(message)
	print(encrypted)

	data = ''
	for i in encrypted:
	    data += convert(i)
	# print (data)
	image = cv2.imread('airplane.jpeg', 0)
	image_dct = dct(image, data)

	# import scipy.misc
	# scipy.misc.imsave('airplane2.jpeg', image_dct)
	imageio.imwrite('filename.jpeg', image_dct)

	sfile1 = open("myfile.txt","w")
	file1.write(message) 
	file1.close()	 


if __name__ == '__main__':
	main()
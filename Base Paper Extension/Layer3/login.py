import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc


# In[14]:





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
message = message.encode()



quantization_table = [[16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [68, 56, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]]


# In[15]:


def decrypt(image_dct, image):
    data = ''
    image_data = image.astype(float)
    image_data_dct = image_dct.astype(float)
    m, n = image_data.shape
#     image_dct = np.zeros(image.shape)
    x_division = int(m/8)
    y_division = int(n/8)
    
    a = 0
    
    for i in range(0, x_division):
        for j in range(0, y_division):
            x_s = i * 8
            x_e = (i+1) * 8
            y_s = j * 8
            y_e = (j+1) * 8
            lis_dct = cv2.dct(image_data[x_s:x_e,y_s:y_e]) / quantization_table
            lis_dct_new = image_data_dct[x_s:x_e,y_s:y_e]
            
#             if a < 1:
#                 print (lis_dct)
#                 print (lis_dct_new)
#                 a += 1
#             ******************
            for k, l in zip(lis_dct, lis_dct_new):
                for m, n in zip(k, l):
                    if m == n:
#                         print ("Equal")
                        continue
                    elif abs(n - m) >= 1.9 and abs(n - m) <= 2.1:
                        data += '0'
#                         print ("0")
#                         print (data)
                    elif abs(n - m) >= 2.9 and abs(n - m) <= 3.1:
                        data += '1'
#                         print ("1")
#                         print (data)
#             ******************
#             for k in lis_dct_new:
#                 for m in k:
#                     if m > 2 and m < 3:
#                         data += '0'
# #                         print (data)
#                     elif m > 3:
#                         data += '1'
# #                         print(data)
                    
    
    to_return = ''
    for i in range(0, int(len(data) / 9)):
        substr = data[i * 9 : (i + 1) * 9]
#         print (substr)
        num = int(substr, 2)
#         print (num)
        to_return += chr(num)
        
#     print (to_return)
    return to_return


# In[16]:


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


# In[18]:


def getmsg():
    #s1 = 'Android devices boot to the homescreen, the primary navigation and information "hub" on Android devices, analogous to the desktop found on personal computers. Android homescreens are typically made up of app icons and widgets; app icons launch the associated app, whereas widgets display live, auto-updating content, such as a weather forecast, the users email inbox, or a news ticker directly on the homescreen. A homescreen may be made up of several pages, between which the user can swipe back and forth.[78] Third-party apps available on Google Play and other app stores can extensively re-theme the homescreen, and even mimic the look of other operating systems, such as Windows Phone. Most manufacturers customize the look and features of their Android devices to differentiate themselves from their competitors.'
    s1 = "Before you can begin to determine what the composition of a particular paragraph will be, you must first decide on an argument and a working thesis statement for your paper. What is the most important idea that you are trying to convey to your reader? The information in each paragraph must be related to that idea. In other words, your paragraphs should remind your reader that there is a recurrent relationship between your thesis and the information in each paragraph. A working thesis functions like a seed from which your paper, and your ideas, will grow. The whole process is an organic one—a natural progression from a seed to a full-blown paper where there are direct, familial relationships between all of the ideas in the paper."
    return s1


# In[20]:


from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii

def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()

curve = registry.get_curve('brainpoolP256r1')

def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    print ("ciphertextPrivKey:", ciphertextPrivKey)
    sharedECCKey = ciphertextPrivKey * pubKey
    print ("sharedECCKey:", sharedECCKey)
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    print ("secretKey:", secretKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    print ("ciphertextPubKey:", ciphertextPubKey)
    return (ciphertext, nonce, authTag, ciphertextPubKey)

def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext

# msg = b'The existing approaches studied do not apply compression on data before encryption. The data if compressed before encryption will encrypt faster due to reduced size. In [3] AES algorithm is used. The size of file after AES encryption is more and lags behind Blow fish algorithm. The security approaches studied so far does not consider parameters like time to encrypt and storage space into consideration. This proposed approach takes into account the parameters like time and space required into account. '       b'decrypted by its corresponding ECC private key'
msg = message
print("original msg:", msg)
privKey = secrets.randbelow(curve.field.n)
# print ("Privkey:", privKey)
pubKey = privKey * curve.g
# print ("Public:", pubKey)

cipher = ''

encryptedMsg = encrypt_ECC(msg, pubKey)
encryptedMsgObj = {
    'ciphertext': binascii.hexlify(encryptedMsg[0]),
    'nonce': binascii.hexlify(encryptedMsg[1]),
    'authTag': binascii.hexlify(encryptedMsg[2]),
    'ciphertextPubKey': hex(encryptedMsg[3].x) + hex(encryptedMsg[3].y % 2)[2:]
}
print("encrypted msg:", encryptedMsgObj)
# print (type(binascii.hexlify(encryptedMsg[0])))
cipher = binascii.hexlify(encryptedMsg[0]).decode("utf-8")
# print (cipher)
# print (type(cipher))

data = ''
for i in cipher:
    data += convert(i)
# print (data)
image = cv2.imread('github.jpeg', 0)
image_dct = dct(image, data)

import scipy.misc
scipy.misc.imsave('github2.jpeg', image_dct)

def final_decrypt(image_dct, image, encryptedMsg, privKey):
	bindata = decrypt(image_dct, image)
	bindata = str.encode(bindata)
	bindata = binascii.unhexlify(bindata)

	ecm = encryptedMsg
	l1 = list(encryptedMsg)
	l1[0] = bindata
	# print (l1)
	encryptedMsg = tuple(l1)
	# print (encryptedMsg)
	# print (ecm)

	# if ecm != encryptedMsg:
	#     print ("Y")

	decryptedMsg = decrypt_ECC(encryptedMsg, privKey)
	print("decrypted msg:", decryptedMsg)

final_decrypt(image_dct, image, encryptedMsg, privKey)
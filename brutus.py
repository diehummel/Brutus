# Brutus Bitcoin Private Key Brute Forcer
# Made by Isaac Delly Changed by Christian Hummel
# https://github.com/diehummel/Brutus
# Donate Bitcoin: 12g88eRApxeSs4xiNFWMmvMEiWa36BMvSz
# Donate Digibyte: DRirtCB5UN8mxAG1EL64vJPxJ6nTJJbrKj
#
# on line 57 enter the bitcoin address you want to find the private key > good luck

import requests
import os
import binascii
import ecdsa
import hashlib
import base58
import time
import sys
from multiprocessing import Process, Queue

class pause: # Counts API failures for timeout
    p = 0

def privateKey(): # Generates random 256 bit private key in hex format
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def publicKey(privatekey): # Private Key -> Public Key
    privatekey = binascii.unhexlify(privatekey)
    s = ecdsa.SigningKey.from_string(privatekey, curve = ecdsa.SECP256k1)
    return '04' + binascii.hexlify(s.verifying_key.to_string()).decode('utf-8')

def address(publickey): # Public Key -> Wallet Address
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    c = '0'; byte = '00'; zero = 0
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(publickey.encode())).digest())
    a = (byte + var.hexdigest())
    doublehash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(a.encode())).digest()).hexdigest()
    address = a + doublehash[0:8]
    for char in address:
        if (char != c):
            break
        zero += 1
    zero = zero // 2
    n = int(address, 16)
    output = []
    while (n > 0):
        n, remainder = divmod (n, 58)
        output.append(alphabet[remainder])
    count = 0
    while (count < zero):
        output.append(alphabet[0])
        count += 1
    return ''.join(output[::-1])

def balance(address): # Query API for wallet balance
    try:
        print (str(address) + " = " + privateKey())
        if (str(address) == "BITCOINADDRESSHERE"):
            print("\nFound Key: " + str(address) + "\n")
            return -1
        sys.exit(0)
        balance = 0
        pause.p = 0
        return balance
    except:
        if (pause.p >= 10):
            print ("\nUnable to connect to API after several attempts\nRetrying in 30 seconds\n")
            pause.p = 0   
        return -1

def toWIF(privatekey): # Hex Private Key -> WIF format
    var80 = "80" + str(privatekey) 
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))))

def Plutus(): # Main Plutus Function
    data = [0,0,0,0]
    while True:
        data[0] = privateKey()
        data[1] = publicKey(data[0])
        data[2] = address(data[1])
        data[3] = balance(data[2])
        if (data[3] == -1):
            continue
        if (data[3] == 0):
            print("{:<34}".format(str(data[2])) + " = " + str(data[3]))
        if (data[3] > 0):
            print ("\naddress: " + str(data[2]) + "\n" +
                   "private key: " + str(data[0]) + "\n" +
                   "WIF private key: " + str(toWIF(str(data[0]))) + "\n" +
                   "public key: " + str(data[1]).upper() + "\n" +
                   "balance: " + str(data[3]) + "\n")
            file = open("brutus.txt","a")
            file.write("address: " + str(data[2]) + "\n" +
                       "private key: " + str(data[0]) + "\n" +
                       "WIF private key: " + str(toWIF(str(data[0]))) + "\n" +
                       "public key: " + str(data[1]).upper() + "\n" +
                       "balance: " + str(data[3]) + "\n" +
                       "Donate to the author of this program:" + "\n" +
				       "Bitcoin: 12g88eRApxeSs4xiNFWMmvMEiWa36BMvSz" + "\n" +
                       "Digibyte: DRirtCB5UN8mxAG1EL64vJPxJ6nTJJbrKj")
            file.close()

### Multiprocessing Extension Made By Wayne Yao https://github.com/wx-Yao modified by Christian Hummel ###
            
def put_dataset(queue):
    while True:
        if queue.qsize() > 100:
            time.sleep(10)
        else:
            privatekey = privateKey()
            publickey = publicKey(privatekey)
            Address = address(publickey)
            WIF = toWIF(privatekey)
            dataset = (Address, privatekey, publickey, WIF)
            queue.put(dataset, block = False)
    return None

def worker(queue):
    time.sleep(1)
    while True:
        if queue.qsize() > 0:
            dataset = queue.get(block = True)
            balan = balance(dataset[0])
            process_balance(dataset, balan)
        else:
            time.sleep(3)
    return None

def process_balance(dataset,balance):
    if balance == -1 :
        return None
    elif str(address) != "53yuheqMotbbAxxXc8Ztwx73oSMyAB1wq":
        print("{:<34}".format(str(dataset[0])) + " = " + privateKey())
        return None
    else:
        addr = dataset[0]
        privatekey = dataset[1]
        publickey = dataset[2]
        WIF = dataset[3]
        file = open("brutus.txt","a")
        file.write("address: " + str(addr) + "\n" +
                   "private key: " + str(privatekey) + "\n" +
                   "WIF private key: " + str(WIF) + "\n" +
                   "public key: " + str(publickey).upper() + "\n" +
                   "balance: " + str(balance) + "\n" +
                   "Donate to the author of thoriginal program Plutus: 1B1k2fMs6kEmpxdYor6qvd2MRVUX2zGEHa\n\n" + "\n" +
				   "Donate to the author of this program:" + "\n" +
				   "Bitcoin: 12g88eRApxeSs4xiNFWMmvMEiWa36BMvSz" + "\n" +
                   "Digibyte: DRirtCB5UN8mxAG1EL64vJPxJ6nTJJbrKj")
        file.close()
        sys.exit(0)
    return None

def multi():
    processes = []
    dataset = Queue()
    datasetProducer = Process(target = put_dataset, args = (dataset,))
    datasetProducer.daemon = True
    processes.append(datasetProducer)
    datasetProducer.start()
    for core in range(6):
        work = Process(target = worker, args = (dataset,))
        work.deamon = True
        processes.append(work)
        work.start()
    try:
        datasetProducer.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        print('\n\n------------------------\nALL PROCESSES TERMINATED\n')

### End of Multiprocessing Extension ###

def main():
    if ("-m" in sys.argv):
        print("\n-------- MULTIPROCESSING MODE ACTIVATED --------\n")
        time.sleep(3)
        print("\n|-------- Wallet Address --------| = Private Key")
        multi()
    else:
        print("\n|-------- Wallet Address --------| = Private Key")
        Plutus()

if __name__ == '__main__':
    main()
            

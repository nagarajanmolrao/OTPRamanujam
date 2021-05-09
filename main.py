import time
import pyotp
import os
import json
from cryptography.fernet import Fernet
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP as security
import stdiomask


def clrscr():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


workingDirPath = ""
keyPassword = None
AES_Key = ""


def check_for_files():
    global workingDirPath
    dirConfigured = False
    if not os.path.isfile("dataPath.txt"):
        choice = input("Work with current Directory? Y/N: ")
        if choice == "y":
            workingDirPath = os.path.dirname(os.path.realpath(__file__))
        elif choice == "n":
            while not dirConfigured:
                workingDirPath = str(input("\nEnter the complete directory path: "))
                if os.path.exists(workingDirPath):
                    dirConfigured = True
                else:
                    print("\nGiven path doesn't exist!\n")
        else:
            print("Invalid Input!\n")
            exit(-1)
    else:
        with open(os.path.join(workingDirPath, "dataPath.txt"), 'r')as dataPath:
            workingDirPath = dataPath.read()
        if not os.path.exists(workingDirPath):
            print("Configured Path does not exist!\n")
            exit(-1)

    file_list = ["accounts.enc", "encryptedAES.key", "PrivateKey.pem", "PublicKey.pem"]
    for file in file_list:
        if not os.path.isfile(os.path.join(workingDirPath, file)):
            if file == file_list[2] or file == file_list[3]:
                print("Please use the key generator to generate a Key pair and copy both the files to \"", workingDirPath, "\"")
                exit(-1)
            elif file == file_list[1]:
                print("\nFile: ", file, "not in the Directory\n")
                choice = input("Generate a new Key?")
                if choice == "y" or choice == "Y":
                    encrypt_key()
                exit(-1)
            elif file == file_list[0]:
                print("\nFile: ", file, "not in current Directory\n")
                update_accounts()
                exit(-1)
            else:
                print("\nFile Check Passed!\n")
                with open("dataPath.txt", 'w')as dataPath:
                    dataPath.write(workingDirPath)


# noinspection PyBroadException
def encrypt_key():
    global AES_Key
    en_key = None
    AES_Key = Fernet.generate_key()
    try:
        with open(os.path.join(workingDirPath, 'PublicKey.pem'), 'rb') as pubkey:
            importedPubKey = RSA.import_key(pubkey.read())
    except:
        print("\nAn error occurred while accessing Public Key!\n")
        return -1

    try:
        encObj = security.new(importedPubKey)
    except Exception as e:
        print(e)
        exit(-1)
    else:
        en_key = encObj.encrypt(AES_Key)

    try:
        with open(os.path.join(workingDirPath, "encryptedAES.key"), 'wb') as efn:
            efn.write(en_key)
    except:
        print("An error occurred while encrypting the file!\n")
        return -1
    else:
        return 0


# noinspection PyBroadException
def decrypt_key():
    global AES_Key
    global keyPassword
    if keyPassword is None:
        keyPassword = stdiomask.getpass(prompt="Password to decrypt PrivateKeyFile: ")
    try:
        with open(os.path.join(workingDirPath, 'PrivateKey.pem'), 'rb') as privkey:
            try:
                importedPrivKey = RSA.import_key(privkey.read(), passphrase=keyPassword)
            except Exception as e:
                print("Error Decrypting Private Key!\n", e)
                keyPassword = None
                return -1
    except:
        print("\nAn error occurred while accessing Private Key!\n")
        return -1

    try:
        with open(os.path.join(workingDirPath, "encryptedAES.key"), 'rb') as fn:
            data = fn.read()
        decObj = security.new(importedPrivKey)
        AES_Key = decObj.decrypt(data)
    except Exception as e:
        print("\nAn error occurred while accessing and decrypting the file!\n", e)
        return -1
    else:
        return 0


# noinspection PyBroadException
def encrypt_accounts():
    global AES_Key
    try:
        with open(os.path.join(workingDirPath, "accounts.json"), 'rb') as data:
            OGData = data.read()
    except:
        print("Error reading Encrypted file")
    a = Fernet(bytes(AES_Key))
    encData = a.encrypt(OGData)
    try:
        with open(os.path.join(workingDirPath, "accounts.enc"), 'wb')as encFile:
            encFile.write(encData)
    except:
        print("An Error occurred while encrypting accounts file\nPlease restart the program and try again\n")
        exit(-1)
    else:
        remove_unencrypted_file()


# noinspection PyBroadException
def remove_unencrypted_file():
    if os.path.exists(os.path.join(workingDirPath, "accounts.json")):
        removeFlag = input("\nRemove the unencrypted file? Y/N :")
        if removeFlag == "y" or removeFlag == "Y":
            try:
                os.remove(os.path.join(workingDirPath, "accounts.json"))
            except:
                print("Error while deleting the unencrypted accounts file\n")
                exit(-1)
            else:
                print("\"accounts.json\" file deleted successfully\n")
            return 0
        elif removeFlag == "n" or removeFlag == "N":
            return 1
        else:
            print("Invalid Input!\n")
            return -1


# noinspection PyBroadException
def decrypt_accounts():
    with open(os.path.join(workingDirPath, "accounts.enc"), 'rb')as encFile:
        encData = encFile.read()
    b = Fernet(bytes(AES_Key))
    decrypted_data = b.decrypt(encData)
    return json.loads(decrypted_data)


def generate_otp(name, secret):
    if secret is None:
        print("Invalid Secret!")
        return -1
    totp = pyotp.TOTP(secret)
    CurrentOTP = totp.now()
    print("Name: ", name, end="\n")
    print("Current OTP: ", CurrentOTP)


# noinspection PyBroadException
def update_accounts():
    b = Fernet(bytes(AES_Key))
    try:
        with open(os.path.join(workingDirPath, "accounts.enc"), 'rb')as encFile:
            encData = encFile.read()
    except:
        print("Copy the \"accounts_template.json\" as \"accounts.json\" to \"", workingDirPath, "\"")
    else:
        decrypted_data = b.decrypt(encData)
        decrypted_data = json.loads(decrypted_data)
        with open(os.path.join(workingDirPath, "accounts.json"), 'w') as jFile:
            json.dump(decrypted_data, jFile)
        print("The Decrypted File has been stored as \"accounts.json\".\n")
    print("Add the entries through a text editor, save the file and Press any key to continue.\n")
    input("")
    encrypt_accounts()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    op = "0"
    if decrypt_key() == -1:
        exit(-1)
    check_for_files()
    accounts = decrypt_accounts()
    if accounts == -1:
        print("\nUnable to decrypt accounts!\n")
        exit(-1)
    while op != "q":
        j = 1
        for i in accounts:
            print("\n", j, ":\t", accounts[i]["name"])
            j += 1
        print("\nu :\tUpdate Accounts")
        print("\nq :\tQuit")
        op = input("Enter your choice: ")
        if op == "q":
            exit(0)
        elif op == "u":
            update_accounts()
            print("Closing the program, Re-open to load the new File\n")
            time.sleep(10)
            exit(-1)
        # noinspection PyBroadException
        try:
            generate_otp(accounts[op]["name"], accounts[op]["secret"])
            time.sleep(3)
        except:
            print("Invalid option!")

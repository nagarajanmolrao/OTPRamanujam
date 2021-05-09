from Cryptodome.PublicKey import RSA
import stdiomask

# Generation
key = RSA.generate(2048)

# Exporting the Keys
password = stdiomask.getpass(prompt="Password: ")
fPriv = open('PriKey.pem','wb')
fPriv.write(key.export_key('PEM', passphrase=password))
fPriv.close()

fPub = open('PubKey.pem', 'wb')
fPub.write(key.public_key().exportKey())
fPub.close()

# Importing the keys
password = stdiomask.getpass(prompt="Password: ")
with open('PriKey.pem', 'rb') as pkey:
    try:
        importedPrivKey = RSA.import_key(pkey.read(), passphrase=password)
    except Exception as e:
        print(e)
        print("Error Decrypting Private Key!\n")
        exit(-1)
    else:
        print("Done")
        exit(1)

with open('Pub.pem', 'rb') as pubkey:
    importedPubKey = RSA.import_key(pubkey.read())

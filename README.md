# OTPRamanujam
A CLI application to generate 2FA TOTP codes

### DESCRIPTION

This python application was built to generate 2FA TOTP codes for my personal accounts on Desktop.
Initially, I used "Authy" as the to-go application to get cross-platform to the OTP codes.
However, the downside of "Authy" for me was the need of previously authenticated device for new device registration.
I am nerd who frequently hop around various devices, so I decided to create this application to overcome this securely.

### HOW IT WORKS

- Accounts with their respective secret key are initially provided to the application through a json file
         *(refer "accounts-template.json" file in the repository)*

- Initially, a key is generated for the encryption of the json file.
        This key is later encrypted using a Key-Pair and stored in a file.
        **(The pair of keys must be provided)**
  
- Every time the program checks for four files in the working directory path provided:
    * accounts.enc : Encrypted file containing the accounts details
    * encryptedAES.key : Encrypted key used to encrypt the file containing the account details
    * PrivateKey.pem & PublicKey.pem : The pair of keys
    
    ***THESE FOUR FILES MUST HAVE THE EXACT FILE NAMES AS ABOVE***
- Every time the PrivateKey is decrypted using the password given at the time of key generation,
then this key is used to decrypt the actual decryption key stored in "encryptedAES.key",
  then the encrypted accounts file is decrypted and loaded as a dictionary, read and printed as a menu,
  from where one can select the account, and the OTP is generated.
  
### INSTALLATION

* In order for some dependencies to install on Windows, Installation of "Build Tools for Visual Studio 2019"
is necessary.
  - Visit the link below to download the same
    
    https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019
	
* Please Refer to link below if there are errors while installing pycryptodome package
	
	https://pycryptodome.readthedocs.io/en/latest/src/installation.html

* You can clone this repository and install all the python dependencies from pip.

    `pip install -r requirements.txt`

* Run the application

    `python main.py`

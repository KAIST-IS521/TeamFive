import gnupg
import base64
import json
import os

HOST = ''
PORT = 42 
TEAM_KEY_FOLDER = "teamkeys"
TEAM_SECRET_KEY = TEAM_KEY_FOLDER+"/teamsecret.key"
TA_KEY_FOLDER = "takeys"
SIG_TEMP_FILE = "/tmp/IS521GovKeySig"
FLAG_OUT_FILE = "/tmp/IS521GovFlag"

PASSPHRASE = ""

class UpdateKey():
    # init
    def __init__(self, team_key_path, ta_key_folder_path):
        self.gpg = gnupg.GPG()
        #import our keys
        self.teamgpg = self.gpg.import_keys(team_key_path) 
        self.tagpgList = []
        #import TA keys
        files = os.walk(ta_key_folder_path).next()[2]
        for filename in files: 
            with open(ta_key_folder_path+"/"+filename, 'r') as f:
                self.tagpgList.append( self.gpg.import_keys(f.read()) )
        
        
    # Decrypt Data with Team Private Key
    def DecryptData(self, enc):
        dec_data = self.gpg.decrypt(enc, passphrase = PASSPHRASE,  always_trust=True)
        return str(dec_data)

    #Save Signature Temporary
    def SaveSigToFile(self, sig):
        data = base64.b64decode(sig)
        f = open(SIG_TEMP_FILE, "wb")
        f.write(data)
        f.close()
        
    # Verify Signature
    def VerifySig(self, data):
        result = self.gpg.verify_data(SIG_TEMP_FILE, data)
        return result.valid

    # Save Flag & Delete Signature file
    def SaveFlag(self, flag):
        f = open(FLAG_OUT_FILE, "w")
        f.write(flag)
        f.close()

    # Process Key Update
    def UpdateKey(self, data):
        #Step1. Decrypt Data
        dec_data = self.DecryptData(data)
        if dec_data == '':
            return False

        #Step2. Parsing With Json
        try:
            json_data = json.load(dec_data)
        except:
            return False

        #Step3. Save Signature to File
        self.SaveSigToFile(json_data['signature'])

        #Step4. Verifying Signature
        valid = self.VerifySig(json_data['signer'] +":"+ json_data['newflag'])

        if not valid:
            return False 
        
        #Step5. Save Flag to File
        self.SaveFlag(json_data['newflag'])



    

if __name__ == '__main__':
    uk = UpdateKey("./teamkeys/teamsecret.key", "./takeys/")
    """
    f = open("/home/vagrant/test.sh.gpg", "rb")
    print uk.DecryptData(f.read())
    """
    f = open("/home/vagrant/test.sh.sig", "rb")

    hh = uk.gpg.verify_file(f, "/home/vagrant/test.sh")
    print hh.valid


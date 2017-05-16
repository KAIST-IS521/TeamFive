import gnupg
import base64
import json
import os

SIG_TEMP_FILE = "/tmp/IS521GovKeySig"
FLAG_OUT_FILE = "/tmp/IS521GovFlag"
PASSPHRASE = None 

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii')
    return dict(map(ascii_encode, pair) for pair in data.items())

class UpdateKey():
    # init
    def __init__(self, team_key_path, ta_key_folder_path):
        self.gpg = gnupg.GPG()
        #import our keys
        with open(team_key_path, "r") as f:
            self.gpg.import_keys(f.read()) 
        self.tagpgList = {}
        #import TA keys
        files = os.walk(ta_key_folder_path).next()[2]
        for filename in files: 
            with open(ta_key_folder_path+"/"+filename, 'r') as f:
                pub_key = self.gpg.import_keys(f.read())
                if len(pub_key.fingerprints) != 0:
                    self.tagpgList[os.path.splitext(filename)[0]] = pub_key.fingerprints[0]
        
        
    # Decrypt Data with Team Private Key
    def DecryptData(self, enc):
        if PASSPHRASE == None:
            dec_data = self.gpg.decrypt(enc,  always_trust=True)
        else:
            dec_data = self.gpg.decrypt(enc, passphrase = PASSPHRASE,  always_trust=True)

        return str(dec_data)

    #Save Signature Temporary
    def SaveSigToFile(self, sig):
        data = base64.b64decode(sig)
        f = open(SIG_TEMP_FILE, "wb")
        f.write(data)
        f.close()
        
    # Verify Signature
    def VerifySig(self, signer, newflag):
        result = self.gpg.verify_data(SIG_TEMP_FILE, signer+":"+newflag)
        # Check Singer's fingerprint
        if result.fingerprint == self.tagpgList[signer]:
            return result.valid
        return False 

    # Save Flag & Delete Signature file
    def SaveFlag(self, flag):
        f = open(FLAG_OUT_FILE, "w")
        f.write(flag)
        f.close()
        os.unlink(SIG_TEMP_FILE)


    # Process Key Update
    def UpdateKey(self, data):
        result = {'result':False, 'signer':'', 'newflag':''}
        try:
            #Step1. Decrypt Data
            dec_data = self.DecryptData(data)
            if dec_data == '':
                return result 
            #Step2. Parsing With Json
            json_data = json.loads(dec_data, object_hook=ascii_encode_dict)

            #Step3. Save Signature to File
            self.SaveSigToFile(json_data['signature'])

            #Step4. Verifying Signature
            valid = self.VerifySig(json_data['signer'],  json_data['newflag'])

            if not valid:
                return result 
            
            #Step5. Save Flag to File
            self.SaveFlag(json_data['newflag'])
            result['signer'] = json_data['signer']
            result['newflag'] = json_data['newflag']
        except:
            return result 

        result['result'] = True
        return result 

    

if __name__ == '__main__':
    uk = UpdateKey("./teamkeys/teamsecret.key", "./takeys/")
    """
    f = open("/home/vagrant/test.sh.gpg", "rb")
    print uk.DecryptData(f.read())
    """
    f = open("/home/vagrant/test.sh.sig", "rb")

    hh = uk.gpg.verify_file(f, "/home/vagrant/test.sh")
    print hh.valid


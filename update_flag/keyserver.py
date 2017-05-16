from socket import *
import update_key
import sys
import threading
import os


PORT = 42 
TEAM_KEY_FOLDER = "teamkeys"
TEAM_SECRET_KEY = TEAM_KEY_FOLDER+"/teamsecret.key"
TA_KEY_FOLDER = "takeys"


def ClinetHandle(conn, ku):
    data = conn.recv(8192)
    result = ku.UpdateKey(data)
    if result['result']:
        print "Key Update OK [ singer : %s, newflag: %s ]" % (result['signer'], result['newflag'])
    else:
        print "Key Update Failed"

    conn.close()
    return


# Print Usage
if len(sys.argv) < 3:
    print "Usage : %s %s %s" % (sys.argv[0], "[Private_Key_File]", "[TA's Key Folder]")
    sys.exit()

# Key existence check
TEAM_SECRET_KEY = sys.argv[1]
TA_KEY_FOLDER = sys.argv[2]

if os.access(TEAM_SECRET_KEY, 0) == False:
    print "[ERROR] There is no private key"
    sys.exit()

if os.access(TA_KEY_FOLDER, 0) == False:
    print "[ERROR] There is no public key folder"
    sys.exit()

# Create Key Update Class
try:
    ku = update_key.UpdateKey(TEAM_SECRET_KEY, TA_KEY_FOLDER)
except:
    print "[ERROR] Key import Error"
    sys.exit()


# Create socket
serverSocket = socket()

try:
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', PORT))
except error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

serverSocket.listen(5)


# Accept connection
while 1:
    try:
        conn, addr = serverSocket.accept()
    except socket.error:
        break
    t = threading.Thread(target = ClinetHandle, args=(conn,ku))
    t.start()

serverSocket.close()


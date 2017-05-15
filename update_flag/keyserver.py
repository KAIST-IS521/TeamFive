from socket import *
import update_key
import sys
import threading


PORT = 42 
TEAM_KEY_FOLDER = "teamkeys"
TEAM_SECRET_KEY = TEAM_KEY_FOLDER+"/teamsecret.key"
TA_KEY_FOLDER = "takeys"


def ClinetHandle(conn):
    ku = update_key.UpdateKey(TEAM_SECRET_KEY, TA_KEY_FOLDER)
    data = conn.recv(8192)
    result = ku.UpdateKey(data)
    if result:
        print "Key Update OK"
    else:
        print "Key Update Failed"

    conn.close()
    return


serverSocket = socket()

try:
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', PORT))
except error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

serverSocket.listen(5)

while 1:
    try:
        conn, addr = serverSocket.accept()
    except socket.error:
        break
    t = threading.Thread(target = ClinetHandle, args=(conn,))
    t.start()

serverSocket.close()


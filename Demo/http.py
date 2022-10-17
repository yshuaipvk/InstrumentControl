from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('ys','12345','E:/share',perm='elr')  #elradfmwMT,adfmw
    authorizer.add_user('ys2','12345','E:/share',perm='elr')
    authorizer.add_anonymous(os.getcwd())

    handler = FTPHandler
    handler.authorizer = authorizer

    address = ("0.0.0.0",2121)
    server = FTPServer(address,handler)
    server.serve_forever()
    # server.max_cons = 256
    # server.max_cons_per_ip =5
    #
    # server.serve_forever()
    #、

if __name__ == '__main__':
    main()
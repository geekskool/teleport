import socket
from sys import argv
import ftplib
from ftplib import FTP
import smtplib
import getpass



sys, HOST, PORT = argv


# The Sock Class which can traverse the FTP directory and copy files
class Sock(object):

    def __init__(self):
        self.s = socket.socket()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = PORT
        self.HOST = HOST


    def Server_type(self):
        if self.PORT == '80' or self.PORT == '443':
            self.Telnet()
        elif self.PORT == '21':
            self.FTP()
        elif self.PORT == '25':
            self.SMTP()
        else:
            HOST, PORT = raw_input("Invalid entry, please enter again >>").split()
            Server_type()
        

    def Telnet(self):
        self.s.connect((self.HOST,int(self.PORT)))
        get_request = raw_input("Please enter your GET Request >>")
        self.s.sendall("%s HTTP/1.0 \r\nContent-Type: text/html%s" % (get_request, "\r\n\r\n"))
        data = (self.s.recv(10000000))
        print "printing data ", data


    #Displays the directory list  
    def FTP(self):
        self.ftp = FTP(HOST)
        try:
            self.s.connect((HOST,int(PORT)))
            print "PORT",PORT,"is open"
            
            try:
                print HOST
                self.ftp.login()
                print "File List:"
                files = self.ftp.retrlines('LIST')
                self.Choice()

            #asks for password if its a secured ftp  
            except ftplib.error_perm:
                username = raw_input("Please enter the username >>")
                password = raw_input("Please enter the password >>")
                self.ftp.login(username,password)
                print "File List:"
                files = self.ftp.retrlines('LIST')
                self.Choice()
        
        except ftplib.error_perm:
            print "PORT",PORT,"is closed, program will exit"
            exit(0)
 

    #choice to copy files or move to a new dir
    def Choice(self):
        file_dir = raw_input("Enter 'y' to move into a directory \n"
                            "'n' to copy a file from the current directory \n"
                            "'enter' to exit>>")
        if file_dir == 'y':
            self.Move_to()
        elif file_dir == 'n':
            self.Copy_to()
        elif file_dir == '\r':
            exit(0)
        else:
            print "Please give a valid entry"
            self.Choice()


    #move to new dir
    def Move_to(self):
        directory = raw_input("Please enter the dir name to move to>>")
        try:
            self.ftp.cwd(directory)
            files = self.ftp.retrlines('LIST')
            self.Choice()
        except ftplib.error_perm:
            print "The given directory does not exist. Please enter a new directory"
            self.Choice()


    def Copy_to(self):
        name = raw_input("Please enter the file name >>")
        try:
            self.ftp.retrbinary('RETR '+name, open(name, 'wb').write)
            print "You file %s has been copied" % name
        except ftplib.error_perm:
            print "The given file cannot be copied."
        self.Choice()
        exit(0)
        self.s.shutdown(1)
        self.s.close()


    def SMTP(self):
      self.s.connect((HOST,int(PORT)))
      
      #fetch userid password and to address
      userid = raw_input("Username: ")
      password = getpass.getpass()
      toaddrs  = raw_input("To: ").split()
      print "Enter message, end with ^D (Unix) or ^Z (Windows):"
      msg = ("From: %s\r\nTo: %s\r\n\r\n"
             % (userid, ", ".join(toaddrs)))
      
      #entering msg untill user types control+D
      while 1:
          try:
              line = raw_input()
          except EOFError:
              break
          if not line:
              break
          msg = msg + line

      print "Message length is " + repr(len(msg))
      print "Message was sent to %s " %(toaddrs)

      #Connecting to SMPT of Google
      server = smtplib.SMTP(HOST+":587")
      
      #Authentication
      server.ehlo()
      
      #SSH enabling
      server.starttls()
      
      #Print debug outoput to log
      server.set_debuglevel(1)
      server.login(userid,password)
      server.sendmail(userid, toaddrs, msg)
      server.quit()



s = Sock()
s.Server_type()
    






    



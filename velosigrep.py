import subprocess
import os
import pty
from services import *
import pexpect

HOST="localhost"
line_number = 20

connection = pexpect.spawn('ssh ' + services[HOST][0] + '@' + HOST + ' cat ' + filename)
authentication = connection.expect(['Are you sure you want to continue connecting','password:', pexpect.EOF])
if authentication == 0:
    connection.sendline('yes')
    authentication = connection.expect(['Are you sure you want to continue connecting', 'password:', pexpect.EOF])
if authentication == 1:
    connection.sendline(password)
    connection.expect(pexpect.EOF)
elif authentication == 2:
    pass

output = connection.before.decode(encoding='UTF-8')

for i, line in enumerate(output.split(os.linesep)):
    if (line_number-100) <= i <= (line_number+100):
        print(i, line)
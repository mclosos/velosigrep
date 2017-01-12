import os
import pexpect
import argparse
from auth_data import auth_data


# create a parser of arguments
parser = argparse.ArgumentParser()
parser.add_argument('--ip', help='ip-address of remote host, example:127.0.0.1')
parser.add_argument('--file', help='path and name of log file, example: /var/log/syslog')
parser.add_argument('--line', help='number of target line')
args = parser.parse_args()
# create a connection with ssh, open log with cat
connection = pexpect.spawn('ssh ' + auth_data(args.ip)[0] + '@' + args.ip + ' cat ' + args.file)
authentication = connection.expect(['Are you sure you want to continue connecting','password:', pexpect.EOF])
if authentication == 0:
    connection.sendline('yes')
    authentication = connection.expect(['Are you sure you want to continue connecting', 'password:', pexpect.EOF])
if authentication == 1:
    connection.sendline(auth_data(args.ip)[1])
    connection.expect(pexpect.EOF)
elif authentication == 2:
    pass

output = connection.before.decode(encoding='UTF-8')
# print -100 and +100 lines from which was sent
for i, line in enumerate(output.split(os.linesep)):
    if (int(args.line)-100) <= i <= (int(args.line)+100):
        print(i, line)
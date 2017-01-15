import io
import paramiko
import argparse
from auth_data import auth_data


# create a parser of arguments
parser = argparse.ArgumentParser()
parser.add_argument('--ip', help='ip-address of remote host, example:127.0.0.1')
parser.add_argument('--path', help='path to the log file, example: /var/log/', default='/var/log/')
parser.add_argument('--file', help='name of log file, example: syslog')
parser.add_argument('--line', help='number of target line', default='0')
parser.add_argument('--index', help='index of log')
args = parser.parse_args()
# create a connection with ssh, open log with cat
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=args.ip, username=auth_data(args.ip)[0], password=auth_data(args.ip)[1], port=22)
stdin, stdout, stderr = client.exec_command('find ' + args.path + ' -name ' + args.file)
found = stdout.read().decode("utf-8").split('\n')
log_file_path = found[0]
print(log_file_path)
client.close()
# get the file
t = paramiko.Transport((args.ip, 22))
t.connect(username=auth_data(args.ip)[0], password=auth_data(args.ip)[1])
sftp_client = paramiko.SFTPClient.from_transport(t)
try:
    output = sftp_client.get(log_file_path, './logfile')
finally:
    sftp_client.close()

with io.open('./logfile', encoding='utf-8') as file:
    for l in file:
        if args.index in l:
            print(l, end="\n\n")
            print('#########################')
"""
# print -100 and +100 lines from which was sent
for i, line in enumerate(output.split(os.linesep)):
    if (int(args.line)-100) <= i <= (int(args.line)+100):
        print(i, line)
"""


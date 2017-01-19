#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import paramiko
import argparse
import traceback

from auth_data import auth_data

# create a parser of arguments
# зы http://docopt.org/ как альтернативу
parser = argparse.ArgumentParser()
parser.add_argument('--ip', help='ip-address of remote host, example:127.0.0.1')
# разве там не три параметра в задании? " ip-адрес, маску названия лога и числовой идентификатор"
# если так, то для find всё равно хватит args.file. А потом под словом "маска" могли иметь ввиду паттерн регулярных выражений
# то есть можно просто запулить grep'ом.
# в любом случае - log_file_path = found[0] - не обязательно нужный файл, если строк больше одной (log_file_path = found[0])
# т.е. то плохая маска => sys.exit(0)
parser.add_argument('--path', help='path to the log file, example: /var/log/', default='/var/log/')
parser.add_argument('--file', help='name of log file, example: syslog')
parser.add_argument('--index', help='index of log')
args = parser.parse_args()

# нужна ещё проверка наверно входных данных типа индекса (а вдруг не число!?)

# create a connection with ssh, open log with cat
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(hostname=args.ip, username=auth_data(args.ip)[0], password=auth_data(args.ip)[1], port=22)
except:
    print("Error: can't connect to {}".format(args.ip))
    print(traceback.format_exc())
    sys.exit(1)

try:
    cmd = 'find ' + args.path + ' -name ' + args.file
    stdin, stdout, stderr = client.exec_command(cmd)
except:
    print("Error: can't execute command {}".format(cmd))
    print(traceback.format_exc())
    sys.exit(1)

# а вдруг там другая кодировка? сложный вопрос на самом деле.
found = stdout.read().decode('utf-8').split(os.linesep)
log_file_path = found[0]
client.close()

# get the file
t = paramiko.Transport((args.ip, 22))
t.connect(userame=auth_data(args.ip)[0], password=auth_data(args.ip)[1])
sftp_client = paramiko.SFTPClient.from_transport(t)

try:
    output = sftp_client.get(log_file_path, './logfile')
except:
    print("Error: can't get file")
    print(traceback.format_exc())
    sftp_client.close()
    sys.exit(1)

# Find and print line with specified index
with open("./logfile") as file:
    lines = file.readlines()

target_index = int(args.index)

# печать слайса
print(lines[(target_index-100):(target_index+100+1)])

target_line = lines[target_index]

os.remove("./logfile")

# по exception'ам. Вообще говорят желательно отлавливать конкретные экспешены, а не все  и обрабатывать соответсвенно
# нужно смотреть какие рейзятся в parmiko

# разбивать на модули конкретно эту задачу наверно смысла нет
# разве что только сделать функции и
if __name__ == "__main__":
    pass
    # main()

# ну и протестить всё это было бы здорово конечно

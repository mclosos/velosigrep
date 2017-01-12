import subprocess
import os
import pty
from services import *

HOST="localhost"
line_number = 1

connection = subprocess.Popen(['ssh', services[HOST][0] + '@' + HOST, 'cat', filename],
                              stdout=subprocess.PIPE)

output, error = connection.communicate()

for i, line in enumerate(output.split(os.linesep)):
    if (line_number-100) <= i <= (line_number+100):
        print(i, line)
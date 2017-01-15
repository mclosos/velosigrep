# velosigrep

Script connects to remote host, find and read (first which found) specified file, print line with specified index (first which found), print -100 and +100 lines from it.

Be sure you have port 22 opened on target host.

<pre>
python == 3.4.3
paramiko==2.1.1
</pre>

importing authentication data from auth_data.py

Usage: python3 velosigrep.py --ip=183.15.19.4 --path=/logs/ --index=8440 --file=logfile

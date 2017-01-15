# velosigrep

Script connects to remote host, read specified file, print -100 and +100 lines from specified line.

Be sure you have port 22 opened on target host.

<pre>
python == 3.4.3
pexpect==4.2.1
</pre>

importing authentication data from auth_data.py

Usage: python3 velosigrep.py --ip=localhost --path=/logs/ --file=logfile --line=150

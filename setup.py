import curses
import socket
import sys
import configparser  # https://docs.python.org/3/library/configparser.html
import aiosmtpd.smtp
from smtp import startsmtp
from editor import editor
from udp import runudp
from tcp import runtcp
from multiprocessing import Process
from ftp import ftpserver


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


IP = get_ip_address()
# Found socket at https://docs.python.org/3/library/socket.html mostly just their code.

config = configparser.ConfigParser()
config.read('icarus.config')
if config['ADDRESSES']['IP'] == "auto":
    IP = get_ip_address()
else:
    IP = config['ADDRESSES']['IP']
smtpport = config['ADDRESSES']['SMTPPort']
abuseip = config['IPDBAPI']['AbuseIPDB']
abuseapikey = config['IPDBAPI']['IPDBAPI']
vtapikey = config['APIKEY']['apikey']
virustotal = config['APIKEY']['Virustotal']
syslogenable = config['SYSLOG']['Syslog']
syslogip = config['SYSLOG']['IP']
syslogport = config['SYSLOG']['PORT']
largfeedon = config['LARGFEED']['Largfeed']
largfeedserver = config['LARGFEED']['Server']
largfeedport = config['LARGFEED']['Port']


aiosmtpd.smtp.__ident__ = "Microsoft ESMTP MAIL Service"


def main(window):

    # Starting SMTP Service
    startsmtp()
    # Starting FTP Service
    p1 = Process(name='Ftp', target=ftpserver, daemon=True)
    p1.start()

    # Dynamic low interaction port services.

    tcpports = 3389, 143, 110, 111, 135, 139, 1723, 3306, 445, 1433, 5900, 22, 23
    udpports = 161, 5600

    for tcpport in tcpports:
        p = Process(name='DynamicTCP ' + str(tcpport), target=runtcp, daemon=True, args=(tcpport,))
        p.start()

    for udpport in udpports:
        p = Process(name='DynamicUDP ' + str(udpport), target=runudp, daemon=True, args=(udpport,))
        p.start()

    createattacker = open("/dev/shm/attacker", "a")
    createattacker.close()

    while True:
        # Opening the Last Attacker record from memory.
        lastattacker = open("/dev/shm/attacker", 'r')
        s = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.napms(3000)
        # Pretty standard configs. I have the curses refresh set to 3 seconds.
        # https://docs.python.org/3.5/library/curses.html#module-curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        sh, sw = s.getmaxyx()
        w = curses.newwin(sh, sw, 0, 0)
        w.nodelay(True)
        # No delay fixes a problem of the screen not updating properly.

        # the above 5 are just standard curses commands.
        # First number is vertical, 51 is horizontal
        w.addstr(0, 51, "Icarus.config")
        w.addstr(1, 51, "Virustotal:")
        w.addstr(2, 51, "Enabled: " + virustotal)
        w.addstr(3, 51, "APIKEY: " + vtapikey)
        w.addstr(5, 51, "AbuseIPDB:")
        w.addstr(6, 51, "Enabled: " + abuseip)
        w.addstr(7, 51, "APIKEY: " + abuseapikey)
        w.addstr(9, 51, "Syslog:")
        w.addstr(10, 51, "Enabled: " + syslogenable)
        w.addstr(11, 51, "Syslog Server: " + syslogip + ":" + syslogport)
        w.addstr(13, 51, "LARGfeed:")
        w.addstr(14, 51, "Enabled: " + largfeedon)
        w.addstr(15, 51, "LARGfeed Server: " + largfeedserver + ":" + largfeedport)
        w.addstr(17, 51, "Press P to change values.", curses.color_pair(2))
        w.addstr(18, 51, "Press R to restart.", curses.color_pair(3))
        w.addstr(19, 51, "Press Q to quit.", curses.color_pair(1))

        w.addstr(0, 0, "ICARUS HONEYPOT", curses.color_pair(1))

        w.addstr(10, 0, "Last Attacker: " + lastattacker.read())
        lastattacker.close()
        # Pretty standard menu above.

        w.refresh()

        key = w.getch()
        if key == ord('q'):
            break
        elif key == ord('r'):
            import os
            os.execv(sys.executable, ['python'] + sys.argv)
            # Nice little thing that restarts a python script.
        elif key == ord('p'):
            editor()  # from editor.py, opens your system editor.
            w.erase()
            w.refresh()


if __name__ == '__main__':
    curses.wrapper(main)

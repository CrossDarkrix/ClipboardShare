#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import subprocess
import sys
import time

PortNum = 50618

def ClipServer():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(('8.8.8.8', 80))
        print('Server iP Adress: {}'.format(sock.getsockname()[0]))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('0.0.0.0', PortNum))
            s.listen(255)
            while True:
                full_data = b''
                Loop = True
                (insock, _) = s.accept()
                while Loop:
                    try:
                        data = insock.recv(1073741824)
                        if len(data) <= 0:
                            Loop = False
                        else:
                            full_data += data
                    except:
                        pass
                try:
                    text = full_data.decode('utf-8')
                    if text != '':
                        if text != '\u200B':
                            try:
                                p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, close_fds=True)
                                p.communicate(input=text.encode('utf-8'))
                            except:
                                pass
                except:
                    pass
                time.sleep(0.89)
        except:
            time.sleep(0.89)


if __name__ == '__main__':
    ClipServer()
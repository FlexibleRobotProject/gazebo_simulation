#! /usr/bin/env python
import sys
import select
import termios
import tty

settings = termios.tcgetattr(sys.stdin)

def getKey():
    tty.setraw(sys.stdin.fileno())

    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)

    if rlist:
        key = sys.stdin.read(1)  # 读取终端上的交互输入
    else:
        key = 'a'

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    return key



if __name__ == '__main__':

    while 1:
        key = getKey()
        print(key)



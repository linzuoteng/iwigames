import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import queue
from loading import Loading
from select_game import Select
from title import Title
from shotIwai import Fight
from Server_game import Server
from race import Race

from hockey1 import Hockey
from hockey2 import Hockey2

from shot1 import Shot1
from shot2 import Shot2

p1_address = "133.20.66.46"
p2_address = "133.20.66.198"

p1_address = "localhost"
p2_address = "localhost"

Server_port = 50001
Client_port = 50000
Server_address = p1_address
Client_address = p2_address

Server_port = 50000
Client_port = 50001
Server_address = p2_address
Client_address = p1_address

def main():
    counter = 0
    q = queue.Queue()
    server = Server(q, Server_address, Server_port)
    while True:
        if counter == 0:
            t = Title()
            t.start()
            counter = t.getCount()
        elif counter == 1:
            l = Loading(q, Client_address, Client_port)
            l.load()
            counter = l.getCount()
            player = l.getPlayer()
        elif counter == 2:
            s = Select(q, Client_address, Client_port, player)
            s.select()
            counter = s.getCount()
        elif counter == 3:
            f = Fight(q, Client_address, Client_port, player)
            f.draw()
            counter = f.getCount()
        elif counter  == 4:
            if player == 1:
                h = Hockey(q, Client_address, Client_port)
                h.draw()
                counter = h.getCount()
            elif player == 2:
                h = Hockey2(q, Client_address, Client_port)
                h.draw()
                counter = h.getCount()
        elif counter  == 5:
            if player == 1:
                s = Shot1(q, Client_address, Client_port)
                s.draw()
                counter = s.getCount()
            elif player == 2:
                s = Shot2(q, Client_address, Client_port)
                s.draw()
                counter = s.getCount()
        elif counter  == 6:
            r = Race(q,Client_address, Client_port,player)
            r.draw()
            counter = r.getCount()
        elif counter == -1:
            break

if __name__=="__main__":
    main()
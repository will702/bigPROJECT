'p4a example service using oscpy to communicate with main application.'

from time import localtime, asctime, sleep

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from kvdroid.audio  import player

from kivy.utils import platform



class Service(object):
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)

    CLIENT = OSCClient('localhost', 3002)
    if platform == 'android':

        filename = ''
    else:
        filename = ''


    def __init__(self):

        self.SERVER.bind(b'/ping', self.ping)
        while True:
            sleep(1)
            self.send_date()


    def ping(self,*_):
        'answer to ping messages'
        filename = _[0].decode('utf-8')
        self.filename = filename

    def send_date(self):
        'send date to the application'


        self.CLIENT.send_message(
            b'/date',
            [asctime(localtime()).encode('utf8'), ],
        )

        if platform == 'android':
            if self.filename != '':

                player.play(self.filename)





if __name__ == '__main__':
    service = Service()




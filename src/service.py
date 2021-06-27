'p4a example service using oscpy to communicate with main application.'

from time import localtime, asctime, sleep

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

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
                from jnius import autoclass

                MediaPlayer = autoclass('android.media.MediaPlayer')
                AudioManager = autoclass('android.media.AudioManager')
                mPlayer = MediaPlayer()
                import audioread
                with audioread.audio_open(self.filename) as f:
                    totalsec = f.duration
                    min, sec = divmod(totalsec, 60)
                    sec = min * 60 + sec
                mPlayer.setDataSource(self.filename)
                mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
                mPlayer.prepare()
                mPlayer.start()
                sleep(sec)
                mPlayer.release()

if __name__ == '__main__':
    service = Service()




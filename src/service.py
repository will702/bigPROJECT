'p4a example service using oscpy to communicate with main application.'

from time import localtime, asctime, sleep

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

from kivy.utils import platform
CLIENT = OSCClient('localhost', 3002)


def ping(*_):

    'answer to ping messages'
    filename = _[0].decode('utf-8')
    print(filename)

    if platform == 'android':
        from jnius import autoclass

        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioManager = autoclass('android.media.AudioManager')
        mPlayer = MediaPlayer()
        import audioread
        with audioread.audio_open(filename) as f:
            totalsec = f.duration
            min, sec = divmod(totalsec, 60)
            sec = min*60+sec
        mPlayer.setDataSource(filename)
        mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
        mPlayer.prepare()
        mPlayer.start()
        sleep(sec)
        mPlayer.release()

def send_date():
    
    'send date to the application'
    CLIENT.send_message(
        b'/date',
        [asctime(localtime()).encode('utf8'),],
    )


if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    SERVER.bind(b'/ping', ping)
    while True:
        sleep(1)
        send_date()


'p4a example service using oscpy to communicate with main application.'

from time import localtime, asctime, sleep

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

from kivy.utils import platform

CLIENT = OSCClient('localhost', 3002,encoding='utf-8')


def ping(*_):
    'answer to ping messages'
    filename = _[0]
    print(filename)



def send_date():
    'send date to the application'
    CLIENT.send_message(
        b'/date',
        [asctime(localtime()), ],
    )

    # if platform == 'android':
    #     from jnius import autoclass
    #
    #     MediaPlayer = autoclass('android.media.MediaPlayer')
    #     AudioManager = autoclass('android.media.AudioManager')
    #     mPlayer = MediaPlayer()
    #     import audioread
    #     with audioread.audio_open('/sdcard/beep1.wav') as f:
    #         totalsec = f.duration
    #         min, sec = divmod(totalsec, 60)
    #         sec = min * 60 + sec
    #     mPlayer.setDataSource('/sdcard/beep1.wav')
    #     mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
    #     mPlayer.prepare()
    #     mPlayer.start()
    #     sleep(sec)
    #     mPlayer.release()
    #
    #


def my_function(*args):
    print('triggered')
    if platform == 'android':
        from jnius import autoclass

        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioManager = autoclass('android.media.AudioManager')
        mPlayer = MediaPlayer()
        import audioread
        with audioread.audio_open(args[0]) as f:
            totalsec = f.duration
            min, sec = divmod(totalsec, 60)
            sec = min * 60 + sec
        mPlayer.setDataSource(args[0])
        mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
        mPlayer.prepare()
        mPlayer.start()
        sleep(sec)
        mPlayer.release()



SERVER = OSCThreadServer(encoding='utf-8')
SERVER.listen('localhost', port=3000, default=True)
SERVER.bind(b'/ping', ping)
SERVER.bind(b'/my_function',my_function)

while True:
    sleep(1)
    send_date()

# coding: utf8
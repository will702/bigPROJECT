
'p4a example service using oscpy to communicate with main application.'

from time import sleep

from oscpy.server import OSCThreadServer


from kivy.utils import platform

from oscpy.client import OSCClient


CLIENT = OSCClient('localhost', 3002,encoding='utf-8')

if __name__ == '__main__':
    SERVER = OSCThreadServer(encoding='utf-8')
    SERVER.listen('localhost', port=3000, default=True)
    @SERVER.address('/my_function')
    def my_function(*args):

        CLIENT.send_message('/message',[args[0]])
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


    # coding: utf8
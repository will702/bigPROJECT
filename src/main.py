
from kivy.app import App
from kivy.lang import Builder
__version__ = '2.0'
from kivy.utils import platform

from jnius import autoclass

from oscpy.client import OSCClient
from oscpy.server import  OSCThreadServer
import certifi
import os


os.environ['SSL_CERT_FILE'] = certifi.where()

SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.oscservice',
    servicename=u'Pong'

)
KV = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: '30sp'
        Button:
            text: 'Turn On'
            on_press: app.start_service()
        Button:
            text: 'Turn Off'
            on_press: app.stop_service()

    ScrollView:
        Label:
            id: label
            size_hint_y: None
            height: self.texture_size[1]
            text_size: self.size[0], None

    BoxLayout:
        size_hint_y: None
        height: '30sp'
        Button:
            text: 'Play'
            on_press: app.trying()
        Button:
            text: 'Clear'
            on_press: label.text = ''
        Label:
            id: date

'''


class ClientServerApp(App):
    def build(self):
        self.service = None
        # self.start_service()




        self.client = OSCClient('localhost', 3000,encoding='utf-8')
        self.server = server = OSCThreadServer(encoding='utf-8')


        server.listen(
            address='localhost',
            port=3002,
            default=True,
        )
        server.bind('/message', self.display_message)


        self.root = Builder.load_string(KV)
        return self.root
    def display_message(self,message):
        if self.root:
            self.root.ids.label.text += '{}\n'.format(message)
    def start_service(self):

        if platform == 'android':
            service = autoclass(SERVICE_NAME)
            self.mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            argument = ''
            service.start(self.mActivity, argument)
            self.service = service



        elif platform in ('linux', 'linux2', 'macosx', 'win'):
            from runpy import run_path
            from threading import Thread
            self.service = Thread(
                target=run_path,
                args=['src/service.py'],
                kwargs={'run_name': '__main__'},
                daemon=True
            )
            self.service.start()
        else:
            raise NotImplementedError(
                "service start not implemented on this platform"
            )

    def stop_service(self):
        if self.service:
            if platform == "android":
                self.service.stop(self.mActivity)
            elif platform in ('linux', 'linux2', 'macos', 'win'):
                # The below method will not work.
                # Need to develop a method like
                # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s03.html
                self.service.stop()
            else:
                raise NotImplementedError(
                    "service start not implemented on this platform"
                )
            self.service = None





    def trying(self,*args):
        self.client.send_message('/my_function',['/sdcard/beep1.wav'])







if __name__ == '__main__':
    ClientServerApp().run()


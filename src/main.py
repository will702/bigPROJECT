# coding: utf8
__version__ = '0.2'

from kivy.app import App
from kivy.lang import Builder

from kivy.utils import platform

from jnius import autoclass

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer

SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.oscservice',
    servicename=u'Pong'
)

KV = '''
#:import platform kivy.utils.platform
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: '30sp'


    ScrollView:
        FileChooserListView:
            id: filechooser
            on_submit: app.selected(*args)
            filters:['*.wav']
            path:'/sdcard' if platform == 'android' else '/Users/willson/downloads'


    BoxLayout:
        size_hint_y: None
        height: '30sp'



        Label:
            id: date

'''


class ClientServerApp(App):
    def build(self):
        self.service = None
        # self.start_service()

        self.server = server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=3002,
            default=True,
        )

        server.bind(b'/message', self.display_message)
        server.bind(b'/date', self.date)

        self.client = OSCClient(b'localhost', 3000)
        self.root = Builder.load_string(KV)
        self.start_service()
        self.asw = ''
        return self.root

    def selected(self, filename, asw, budi):

        if self.asw == '':
            self.send(argumen=f'{asw[0]}')
            self.asw = asw[0]
        if self.asw != '':
            # print(self.asw)
            if self.asw == asw[0]:
                self.send(argumen=f'{asw[0]}')
            if self.asw != asw[0]:
                self.asw = asw[0]

                self.stop_service()

                self.start_service()

                self.send(argumen=f'{asw[0]}')

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

    def send(self, *args, argumen):
        self.client.send_message(b'/ping', [f'{argumen}'.encode('utf-8')])

    def display_message(self, message):

        if self.root:
            self.root.ids.label.text += '{}\n'.format("Worked")

    def date(self, message):

        if self.root:
            self.root.ids.date.text = message.decode('utf8')


if __name__ == '__main__':
    ClientServerApp().run()
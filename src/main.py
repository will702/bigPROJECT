# coding: utf8
__version__ = '0.2'


from kivy.lang import Builder
from kivymd.toast import toast
from kivy.utils import platform
from kivymd.app import MDApp
from jnius import autoclass

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from kivymd.uix.filemanager import  MDFileManager
from kivy.core.window import Window
from kivymd.theming import  ThemeManager

if platform == 'macosx':

    Window.size = (450, 750)
    #if you use macosx you will be resized like this

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.oscservice',
    servicename=u'Pong'
)




class ClientServerApp(MDApp):
    def build(self):
        self.service = None
        # self.start_service()

        self.server = server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=3002,
            default=True,
        )
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = 'Orange'

        self.theme_cls.primary_style = 'Light'
        self.manager_open = False

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )

        self.client = OSCClient(b'localhost', 3000)
        self.root = Builder.load_file('main.kv')

        self.start_service()
        self.asw = ''
        return self.root

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        toast(path)
        if self.asw == '':
            self.send(argumen=f'{path}')
            self.asw = path
        if self.asw != '':
            # print(self.asw)

            if self.asw == path:
                self.send(argumen=f'{path}')
            if self.asw != path:
                self.asw = path

                self.stop_service()

                self.start_service()

                self.send(argumen=f'{path}')


    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()




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







if __name__ == '__main__':
    ClientServerApp().run()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import threading
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager

KV = '''
MDBoxLayout:
    orientation: "vertical"
    MDTopAppBar:
        title: "EasyFileShare"
        elevation: 3
    MDFloatLayout:
        MDLabel:
            color: '#D45D00'
            id: user_id
            font_size: 20
            pos_hint: {"center_x": .6, "center_y": .7}
        MDRoundFlatIconButton:
            id: open
            text: "select Directory"
            icon: "folder"
            pos_hint: {"center_x": .3, "center_y": .5}
            on_release: app.file_manager_open()
        MDRoundFlatIconButton:
            id: start
            text: "start FTP Server"
            icon: "arrow-right-bold"
            pos_hint: {"center_x": .7, "center_y": .5}
            on_release: app.on_start_webdav()
        MDLabel:
            color: '#D45D00'
            id: user_pass
            font_size: 20
            pos_hint: {"center_x": 1., "center_y": .7}
'''


class EasyFileShare(MDApp):
    dialog = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        try:
            from android.permissions import request_permissions, Permission
            request_permissions(
                [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.MANAGE_EXTERNAL_STORAGE]
            )
            import android
            android.start_service(title='EasyFileShare', description='Monitoring EasyFileShare', arg='running')
        except:
            pass
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path, search='dirs'
        )
        self.check = False
        self.authorizer = pyftpdlib.authorizers.DummyAuthorizer()


    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.Screen = Builder.load_string(KV)
        self.Screen.ids['start'].disabled = True
        return self.Screen

    def on_start_webdav(self):
        if not self.check:
            self.check = True
            self.Screen.ids['start'].icon = 'stop'
            self.Screen.ids['start'].text = 'Stop FTP Server'
            try:
                self.server.start()
            except:
                pass
        else:
            self.check = False
            self.Screen.ids['start'].icon = 'arrow-right-bold'
            self.Screen.ids['start'].text = 'start FTP Server'
            try:
                self.server.join(timeout=0)
            except:
                pass
            self.dialog = MDDialog(text="please Restart App", buttons=[MDFlatButton(text="Close App", theme_text_color="Custom", text_color='#FF0C0C', on_release=self.close_alert)])
            self.dialog.open()

    def file_manager_open(self):
        self.file_manager.show(self.home_dir())
        self.manager_open = True

    def select_path(self, path: str):
        self.exit_manager()
        if os.path.isdir(path):
            self.Screen.ids['start'].disabled = False
            self.Screen.ids['user_id'].text = 'User Name: user'
            self.Screen.ids['user_pass'].text = 'Password: password'
            self.authorizer.add_user('user', 'password', path, perm='elradfmw')
            handler = pyftpdlib.handlers.FTPHandler
            handler.authorizer = self.authorizer
            _server = pyftpdlib.servers.FTPServer(("0.0.0.0", 21), handler)
            self.server = threading.Thread(target=_server.serve_forever, daemon=True)
            self.Screen.ids['open'].disabled = True

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def home_dir(self):
        if os.getenv('EXTERNAL_STORAGE') is not None:
            return os.getenv('EXTERNAL_STORAGE')
        else:
            return os.path.expanduser('~')

    def events(self, _0, keyboard, _2, _3, _4):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def close_alert(self, o):
        self.dialog.dismiss()
        self.stop()


if __name__ == '__main__':
    EasyFileShare().run()
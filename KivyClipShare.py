#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Version 3.0b

import asyncio
import os
import socket
import time
import threading
from kivy.core import clipboard
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import mainthread
from kivy.utils import platform
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.list import OneLineListItem
from kivymd.font_definitions import theme_font_styles

WillClosed = [False]
Threads = [None]
Threads2 = [None]
Threads3 = [None]
_was_get_list = []
PortNum = 50618
clipText = [clipboard.Clipboard.paste()]


class _StringProperty(StringProperty):
    def __init__(self, **kwargs):
        super(_StringProperty, self).__init__(**kwargs)


class _MDScrollView(MDScrollView):
    def __init__(self, *args, **kwargs):
        super(_MDScrollView, self).__init__(*args, **kwargs)


class _MDListsWidget(OneLineListItem):
    text = _StringProperty()

    def __init__(self, **kwargs):
        super(_MDListsWidget, self).__init__(**kwargs)
        self.theme_cls.font_styles['_ja-JP'] = ['_ja-JP', 100, False, 0.15]
        self.font_style = '_ja-JP'


class _MDFlatButton(MDFlatButton):
    def __init__(self, **kwargs):
        super(_MDFlatButton, self).__init__(**kwargs)
        self.font_name = '_ja-JP'
        self.md_bg_color = (61, 61, 61, 0)


class _MDLabel(MDLabel):
    def __init__(self, **kwargs):
        super(_MDLabel, self).__init__(**kwargs)
        self.font_name = '_ja-JP'


class _MDListWidget(MDList):
    def __init__(self, **kwargs):
        super(_MDListWidget, self).__init__(**kwargs)
        self.widget_list = []

    def set_widget(self, widget):
        self.widget_list.append(widget)
        self.add_widget(widget)

    def get_text(self, widget):
        for _widget in self.widget_list:
            if _widget == widget:
                return _widget.text

    def delete_all(self):
        for widget in self.widget_list:
            self.remove_widget(widget=widget)
        self.widget_list.clear()


class DetectClipboardText(EventDispatcher):
    def __init__(self, **kwargs):
        super(DetectClipboardText, self).__init__(**kwargs)
        self.register_event_type('on_detection')
        _thread = threading.Thread(target=self.detect, daemon=True)
        Threads2[0] = _thread
        _thread.start()

    def on_detection(self):
        pass

    def detect(self):
        while not WillClosed[0]:
            if clipboard.Clipboard.paste() != '': # クリップボードの中が空白か
                if clipboard.Clipboard.paste() != '\uFEFF': # クリップボードの中が空白文字か
                    if clipboard.Clipboard.paste() != clipText[0]: # クリップボードの中が前回登録した文字列か
                        if self.string_detect(clipboard.Clipboard.paste()): # クリップボードの中が過去に保存されていたか
                            clipText[0] = clipboard.Clipboard.paste() # コピーした内容の外部保存
                            _was_get_list.append(clipboard.Clipboard.paste()) # すでに登録した文字列のリスト
                            try:
                                self.dispatch('on_detection')
                            except:
                                pass
                        else:
                            for _ in range(2):
                                try:
                                    _was_get_list.remove(clipboard.Clipboard.paste())
                                except IndexError:
                                    pass
                                except ValueError:
                                    pass
                                except KeyError:
                                    pass
            if WillClosed[0]:
                break
            else:
                time.sleep(0.01)

    def string_detect(self, string_text: str) -> bool: # ２個以上の重複された文字列がないかチェック
        len_text = 0
        for strings in _was_get_list:
            if strings == string_text:
                len_text += 1
        if 3 <= len_text:
            return False
        else:
            return True


class DetectChange_iP(EventDispatcher):
    def __init__(self, **kwargs):
        super(DetectChange_iP, self).__init__(**kwargs)
        self.register_event_type('on_change_ip')
        self.ip = ''
        _thread = threading.Thread(target=self.check, daemon=True)
        Threads3[0] = _thread
        _thread.start()

    def on_change_ip(self):
        pass

    def check(self):
        while not WillClosed[0]:
            if self.ip != self.check_ip():
                try:
                    self.dispatch('on_change_ip')
                except:
                    pass
                self.ip = self.check_ip()
            if WillClosed[0]:
                break
            else:
                time.sleep(5)

    def check_ip(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(('8.8.8.8', 80))
                return '{}'.format(sock.getsockname()[0])
        except:
            return ''


class ReceiveClipboardText(EventDispatcher):
    def __init__(self, **kwargs):
        super(ReceiveClipboardText, self).__init__(**kwargs)
        self.register_event_type('on_receive')
        _thread = threading.Thread(target=self.setClip, daemon=True)
        _thread.start()
        Threads[0] = _thread

    def on_receive(self):
        pass

    def setClip(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(('0.0.0.0', PortNum))
            self.s.listen(100)
            while not WillClosed[0]:
                full_data = b''
                Loop = True
                (insock, _) = self.s.accept()
                while Loop:
                    try:
                        data = insock.recv(1073741824)
                        if len(data) <= 0:
                            Loop = False
                        else:
                            full_data += data
                    except:
                        pass
                text = full_data.decode('utf-8')
                if text != '':
                    clipboard.Clipboard.copy('{}'.format(text))
                    try:
                        self.dispatch('on_receive')
                    except:
                        pass
                time.sleep(0.89)
        except:
            pass


class SendText(object):
    def __init__(self, host, text):
        self.host = host
        if not self.host == '':
            try:
                try:
                    asyncio.run(self.send(text))
                except:
                    pass
            except:
                pass

    async def send(self, text):
        _, writer = await asyncio.open_connection(self.host, PortNum) # reader, writer = await asyncio.open_connection(self.host, PortNum)
        writer.write(text.encode('utf-8'))
        await writer.drain()
        writer.close()
        await writer.wait_closed()


class ClipboardShare(MDApp):
    def build(self):
        self.font_name = '_ja-JP'
        if platform == 'android':
            import android
            android.start_service(title='ClipShare Service', description='Monitoring Clipboard Service', arg='running')
        self.ReceiveClip = ReceiveClipboardText()
        self.Detection_clipboard = DetectClipboardText()
        self.CheckiP = DetectChange_iP()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        self.title = 'ClipShare'
        self.icon = os.path.join(os.getcwd(), 'images', 'MemoSyncIcon.png')
        self.Layout = BoxLayout(orientation='vertical')
        self.TextFiled = MDTextField()
        self.TextFiled.size = (50, 20)
        self.TextFiled.background_color = '#3d3d3d'
        self.TextFiled.foreground_color = '#FFFFFF'
        self.TextFiled.theme_height = 'Custom'
        self.TextFiled.theme_width = 'Custom'
        self.TextFiled.width = 200
        self.TextFiled.height = 80
        self.Layout.add_widget(self.TextFiled)
        self.Btn = _MDFlatButton(text='送信する')
        self.Btn.theme_width = 'Custom'
        self.Btn.theme_height = 'Custom'
        self.Btn.theme_font_size = 'Custom'
        self.Btn.theme_line_height = 'Custom'
        self.Btn.pos = (0, 100)
        self.Btn.color = '#FF0808'
        self.Btn.width = 200
        self.Btn.height = 400
        self.Btn.font_size = 200
        self.Btn.outline_color = '#FF0808'
        self.Btn.outline_width = 3
        self.Btn.line_width = 2
        self.Btn.line_color = '#FF0808'
        self.Btn.bind(on_press=lambda _: self.send())
        self.Layout.add_widget(self.Btn)
        self.ViewList = _MDListWidget()
        self.ViewList.specific_text_color = [0, 0, 0, 0]
        self.ViewList.size = (50, 100)
        self.ViewList.font_name = '_ja-JP'
        self.ListView = _MDScrollView(self.ViewList)
        self.ListView.font_name = '_ja-JP'
        self.ListView.size = (50, 500)
        self.ListView.pos = (0, 500)
        self.Layout.add_widget(self.ListView)
        self.Btn2 = _MDFlatButton(text='内容を削除する')
        self.Btn2.theme_width = 'Custom'
        self.Btn2.theme_height = 'Custom'
        self.Btn2.theme_font_size = 'Custom'
        self.Btn2.color = '#FF0808'
        self.Btn2.width = 200
        self.Btn2.height = 400
        self.Btn2.font_size = 130
        self.Btn2.outline_color = '#FF0808'
        self.Btn2.outline_width = 3
        self.Btn2.line_width = 2
        self.Btn2.line_color = '#FF0808'
        self.Btn2.bind(on_press=lambda _: self.clear())
        self.Layout.add_widget(self.Btn2)
        self.LabelIP = _MDLabel(text='iP: {}'.format(self.get_ip()))
        self.LabelIP.font_size = 130
        self.Layout.add_widget(self.LabelIP)
        self.Layout.size = (241, 412)
        self.Screen = MDScreen(self.Layout)
        self.Screen.size = (241, 412)
        self.bind(on_stop=lambda _: self.closed())
        self.ReceiveClip.bind(on_receive=lambda _: self.add_list())
        self.Detection_clipboard.bind(on_detection=lambda _: self.auto_get_and_send_clipboard())
        self.CheckiP.bind(on_change_ip=lambda _: self.change_ip_label())
        self.ClipText = ''
        return self.Screen

    @mainthread
    def change_ip_label(self):
        self.LabelIP.text = 'iP: {}'.format(self.get_ip())

    @mainthread
    def auto_get_and_send_clipboard(self):
        SendText(host='127.0.0.1', text=clipboard.Clipboard.paste())
        SendText(host=self.TextFiled.text, text=clipboard.Clipboard.paste())

    @mainthread
    def add_list(self):
        clip = clipboard.Clipboard.paste()
        if clip != '' or clip != '\uFEFF':
            if clip != self.ClipText:
                self.ClipText = clip
                SendText(host=self.TextFiled.text, text=clip)
                text = _MDListsWidget(text=clip)
                text.text_color = '#FFFFFF'
                text.font_size = 500
                text.width = 500
                text.height = 200
                text.bind(on_press=lambda click: self.copy_text(text))
                self.ViewList.set_widget(widget=text)
                _was_get_list.append(clip)

    @mainthread
    def copy_text(self, widget):
        clipboard.Clipboard.copy(self.ViewList.get_text(widget=widget))

    @mainthread
    def closed(self):
        WillClosed[0] = True
        try:
            Threads2[0].join(0)
        except:
            pass
        try:
            Threads3[0].join(0)
        except:
            pass
        try:
            Threads[0].join(0)
        except:
            pass

    def get_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(('8.8.8.8', 80))
            return sock.getsockname()[0]

    def send(self):
        SendText(host=self.TextFiled.text, text=clipboard.Clipboard.paste())

    @mainthread
    def clear(self):
        self.ViewList.delete_all()
        clipboard.Clipboard.copy('\uFEFF')
        _was_get_list.clear()


if __name__ == '__main__':
    ClipboardShare().run()
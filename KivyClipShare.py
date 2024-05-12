#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Version 3.0b

import asyncio
import os
import socket
import time
import threading
from kivy.core import clipboard
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
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.list.list import IconLeftWidget
from kivymd.uix.widget import MDWidget
from kivymd.uix.selectioncontrol.selectioncontrol import MDCheckbox

WillClosed = [False]
Threads = [None]
Threads2 = [None]
Threads3 = [None]
_was_get_list = []
PortNum = 50618
clipText = [clipboard.Clipboard.paste()]


class _MDLabelCheckBox(MDWidget):
    def __init__(self, **kwargs):
        super(_MDLabelCheckBox, self).__init__(**kwargs)
        self.layout = BoxLayout()
        self.layout.size = (1300, 80)
        self.label = _MDLabel()
        self.checkbox = MDCheckbox()
        self.checkbox.active = True
        self.label.font_size = 90
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.checkbox)
        self.add_widget(self.layout)


class _StringProperty(StringProperty):
    def __init__(self, **kwargs):
        super(_StringProperty, self).__init__(**kwargs)


class _MDScrollView(MDScrollView):
    def __init__(self, *args, **kwargs):
        super(_MDScrollView, self).__init__(*args, **kwargs)


class _MDListsWidget(OneLineIconListItem):
    text = _StringProperty()

    def __init__(self, *args, **kwargs):
        super(_MDListsWidget, self).__init__(*args, **kwargs)
        self.theme_cls.font_styles['_ja-JP'] = ['_ja-JP', 100, False, 1.5]
        self.font_style = '_ja-JP'
        self.raw_text = ''
        self.text = '[size=100]{}[/size]'.format(self.text)


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
                return _widget.raw_text

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
                            time.sleep(0.89)
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
        if os.path.exists(os.path.join(os.getcwd(), 'previous_ip.txt')):
            text = open(os.path.join(os.getcwd(), 'previous_ip.txt'), 'r', encoding='utf-8').read()
        else:
            text = ''
        self.TextFiled = MDTextField()
        self.TextFiled.size = (50, 20)
        self.TextFiled.font_size = 50
        self.TextFiled.background_color = '#3d3d3d'
        self.TextFiled.foreground_color = '#FFFFFF'
        self.TextFiled.theme_height = 'Custom'
        self.TextFiled.theme_width = 'Custom'
        self.TextFiled.width = 200
        self.TextFiled.height = 80
        self.TextFiled.hint_text = '対象のiPを入力してください...'
        self.TextFiled.font_name_hint_text = '_ja-JP'
        self.TextFiled.text = text
        self.TextFiled.helper_text_mode = 'on_focus'
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
        self.Check_fxtwitter = _MDLabelCheckBox()
        self.Check_fxtwitter.label.text = 'fxtwitter Mode'
        self.Layout.add_widget(MDScrollView(self.Check_fxtwitter))
        if os.path.exists(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt')):
            _fx = open(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt'), 'r', encoding='utf-8').read()
            if _fx == 'True':
                self.Check_fxtwitter.checkbox.active = True
            if _fx == 'False':
                self.Check_fxtwitter.checkbox.active = False
        if not os.path.exists(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt')):
            with open(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt'), 'w', encoding='utf-8') as fx:
                fx.write('True')
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
        self.Clip_t = ''
        self.Threads4 = threading.Thread(target=asyncio.run, daemon=True, args=(self._on_checkbox(), ))
        self.Threads4.start()
        return self.Screen

    def _on_checkbox(self):
        while True:
            if self.Check_fxtwitter.checkbox.active:
                with open(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt'), 'w', encoding='utf-8') as fx:
                    fx.write('True')    
            else:
                with open(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt'), 'w', encoding='utf-8') as fx:
                    fx.write('False')
            time.sleep(0.89)

    @mainthread
    def change_ip_label(self):
        self.LabelIP.text = 'iP: {}'.format(self.get_ip())

    @mainthread
    def auto_get_and_send_clipboard(self):
        if clipboard.Clipboard.paste() != '':
            if clipboard.Clipboard.paste() != '\uFEFF':
                SendText(host='127.0.0.1', text=clipboard.Clipboard.paste())
                if self.TextFiled.text != '':
                    SendText(host=self.TextFiled.text, text=clipboard.Clipboard.paste())

    @mainthread
    def add_list(self):
        clip = clipboard.Clipboard.paste()
        if clipboard.Clipboard.paste() != '':
            if clip != '\uFEFF':
                if clip != self.ClipText:
                    if self.Check_fxtwitter.checkbox.active:
                        text = '{}'.format(clipboard.Clipboard.paste())
                        try:
                            if text.split('/')[2] == 'x.com':
                                text = 'fxtwitter.com'.join(text.split('x.com'))
                            else:
                                text = 'fxtwitter.com'.join(text.split('twitter.com'))
                            if text.split('/')[2][0:4] == 'fxfx':
                                text = text.replace(text.split('/')[2], 'fxtwitter.com')
                        except IndexError:
                            try:
                                text = 'fxtwitter.com'.join(text.split('twitter.com'))
                                if text.split('/')[2][0:4] == 'fxfx':
                                    text = text.replace(text.split('/')[2], 'fxtwitter.com')
                            except:
                                pass
                        except:
                            pass
                        clip = '{}'.format(text)
                        clipboard.Clipboard.copy('{}'.format(text))
                    self.ClipText = clip
                    if self.TextFiled.text != '':
                        SendText(host=self.TextFiled.text, text=clip)
                    def _pass():
                        pass
                    icon = IconLeftWidget(icon='ClipBoardCopy.png')
                    icon.icon_size = 100
                    widget = _MDListsWidget(icon, text=clip)
                    widget.font_style = '_ja-JP'
                    widget.raw_text = clip
                    widget.height = 220
                    widget.width = 500
                    widget.text_color = '#FFFFFF'
                    icon.bind(on_press=lambda _: self.copy_text(widget))
                    widget.bind(on_press=lambda _: self.copy_text(widget))
                    self.ViewList.set_widget(widget=widget)
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
        try:
            self.Threads4.join(0)
        except:
            pass

    def get_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(('8.8.8.8', 80))
            return sock.getsockname()[0]

    def send(self):
        if self.TextFiled.text.startswith('192') or self.TextFiled.text.startswith('127') or self.TextFiled.text == '' and 8 <= len(self.TextFiled.text):
            with open(os.path.join(os.getcwd(), 'previous_ip.txt'), 'w', encoding='utf-8') as ip:
                ip.write(self.TextFiled.text)
            if self.TextFiled.text != '':
                SendText(host=self.TextFiled.text, text=clipboard.Clipboard.paste())

    @mainthread
    def clear(self):
        self.ViewList.delete_all()
        clipboard.Clipboard.copy('\uFEFF')
        _was_get_list.clear()


if __name__ == '__main__':
    ClipboardShare().run()
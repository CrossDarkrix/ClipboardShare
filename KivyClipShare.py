#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Version 3.2b

import asyncio
import base64
import os
import socket
import time
import threading
import ssl
import json
from kivy.lang import Builder
from kivy.core import clipboard
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import mainthread
from kivy.utils import platform
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineIconListItem, OneLineListItem
from kivymd.uix.list.list import IconLeftWidget
from kivymd.uix.widget import MDWidget
from kivymd.uix.selectioncontrol.selectioncontrol import MDCheckbox
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField


WillClosed = [False]
Threads = [None]
Threads2 = [None]
Threads3 = [None]
Threads4 = [None]
Threads5 = [None]
_was_get_list = []
PortNum = 50618
BROADCAST_PORT = 54545
clipText = [clipboard.Clipboard.paste()]
allow_bk = [True]
out_thread = []
if_check1 = [False]
if_check2 = [False]


class _MDDialog(MDDialog):
    def __init__(self, **kwargs):
        super(_MDDialog, self).__init__(**kwargs)


class OneItemText(OneLineListItem):
    def __init__(self, **kwargs):
        super(OneItemText, self).__init__(**kwargs)
        self.font_style = 'H6'


class BackgroundAllow(object):
    def __init__(self, allow):
        if allow:
            self.thread = threading.Thread(target=self.work)
            out_thread.append(self.thread)
            self.start()
        else:
            allow_bk[0] = False
            for o in out_thread:
                try:
                    o.join(0)
                except:
                    pass

    def work(self):
        while allow_bk[0]:
            if not allow_bk:
                break
            time.sleep(0.1)

    def start(self):
        self.thread.start()


class _MDLabelCheckBox(MDWidget):
    def __init__(self, **kwargs):
        super(_MDLabelCheckBox, self).__init__(**kwargs)
        self.layout = BoxLayout()
        self.layout.size = (1300, 100)
        self.label = _MDLabel()
        self.checkbox = MDCheckbox()
        if not os.path.exists(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt')):
            with open(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt'), 'w', encoding='utf-8') as fx:
                fx.write('False')
            if_check1[0] = False
            self.checkbox.active = False
        else:
            _fx = open(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt'), 'r', encoding='utf-8').read()
            if _fx == 'True':
                if_check1[0] = True
                self.checkbox.active = True
            if _fx == 'False':
                if_check1[0] = False
                self.checkbox.active = False
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.checkbox)
        try:
            text_language_code = open(os.path.join(os.getcwd(), 'language_setting.txt'), 'r', encoding='utf-8').read()
            if text_language_code == 'ja-JP':
                self.label.text = 'fxtwitterモード'
            else:
                self.label.text = 'fxtwitter Mode'
        except:
            self.label.text = 'fxtwitterモード'
        self.checkbox.bind(on_press=lambda _x: self._on_checkbox())
        self.add_widget(self.layout)

    def _on_checkbox(self):
        if self.checkbox.active:
            with open(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt'), 'w', encoding='utf-8') as fx:
                fx.write('True')
            if_check1[0] = True
        else:
            with open(os.path.join(os.getcwd(), 'fxtwitter_mode_setting.txt'), 'w', encoding='utf-8') as fx:
                fx.write('False')
            if_check1[0] = False


class _MDLabelCheckBox2(MDWidget):
    def __init__(self, **kwargs):
        super(_MDLabelCheckBox2, self).__init__(**kwargs)
        self.layout = BoxLayout()
        self.layout.size = (1310, 80)
        self.label = _MDLabel()
        self.checkbox = MDCheckbox()
        if os.path.exists(os.path.join(os.getcwd(), 'allow_background_setting.txt')):
            _fx2 = open(os.path.join(os.getcwd(), 'allow_background_setting.txt'), 'r', encoding='utf-8').read()
            if _fx2 == 'True':
                self.checkbox.active = True
                if_check2[0] = True
            if _fx2 == 'False':
                self.checkbox.active = False
                if_check2[0] = False
        if not os.path.exists(os.path.join(os.getcwd(), 'allow_background_setting.txt')):
            with open(os.path.join(os.getcwd(), 'allow_background_setting.txt'), 'w', encoding='utf-8') as ff:
                ff.write('False')
            if_check2[0] = False
            self.checkbox.active = False
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.checkbox)
        try:
            text_language_code = open(os.path.join(os.getcwd(), 'language_setting.txt'), 'r', encoding='utf-8').read()
            if text_language_code == 'ja-JP':
                self.label.text = 'バックグラウンド動作の許可'
            else:
                self.label.text = 'allow background'
        except:
            self.label.text = 'バックグラウンド動作の許可'
        self.checkbox.bind(on_press=lambda _x: self._on_check())
        self.add_widget(self.layout)

    @mainthread
    def _on_check(self):
        if self.checkbox.active:
            with open(os.path.join(os.getcwd(), 'allow_background_setting.txt'), 'w', encoding='utf-8') as ff:
                ff.write('True')
            BackgroundAllow(True)
        else:
            with open(os.path.join(os.getcwd(), 'allow_background_setting.txt'), 'w', encoding='utf-8') as ff:
                ff.write('False')
            BackgroundAllow(False)


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
        self.specific_text_color = [0, 0, 0, 0]
        self.size = (50, 100)
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
        _thread = threading.Thread(target=asyncio.run, daemon=True, args=(self.detect(), ))
        Threads2[0] = _thread
        _thread.start()

    def on_detection(self):
        pass

    async def detect(self):
        while True:
            if '{}'.format(clipboard.Clipboard.paste()) != '': # クリップボードの中が空白か
                if '{}'.format(clipboard.Clipboard.paste()) != '\u200B': # クリップボードの中が空白文字か
                    if '{}'.format(clipboard.Clipboard.paste()) != clipText[0]: # クリップボードの中が前回登録した文字列か
                        if self.string_detect('{}'.format(clipboard.Clipboard.paste())): # クリップボードの中が過去に保存されていたか
                            clipText[0] = '{}'.format(clipboard.Clipboard.paste()) # コピーした内容の外部保存
                            _was_get_list.append('{}'.format(clipboard.Clipboard.paste())) # すでに登録した文字列のリスト
                            try:
                                self.dispatch('on_detection')
                            except:
                                pass
                            time.sleep(0.89)
                        else:
                            for _ in range(2):
                                try:
                                    _was_get_list.remove('{}'.format(clipboard.Clipboard.paste()))
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

class send_Device_IP(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        MESSAGE = b'CLIPBOARDSHARE_DISCOVERY'
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while not WillClosed[0]:
            sock.sendto(MESSAGE, ('<broadcast>', BROADCAST_PORT))
            time.sleep(5)


class ReceiveiP_Device(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def checkiP(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(('8.8.8.8', 80))
            return '{}'.format(sock.getsockname()[0])

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', BROADCAST_PORT))
        known_peers = {}
        while not WillClosed[0]:
            data, addr = sock.recvfrom(1024)
            if data == b'CLIPBOARDSHARE_DISCOVERY':
                ip = addr[0]
                if ip != self.checkiP():
                    hostname = socket.getfqdn(ip)
                    if socket.getfqdn('localhost') != hostname:
                        known_peers[ip] = hostname
                        with open(os.path.join(os.getcwd(), 'ip_address_list'), 'w', encoding='utf-8') as j:
                            json.dump(known_peers, j, indent=2)
            time.sleep(0.01)


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
            _context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            _context.load_cert_chain(certfile=os.path.join(os.getcwd(), "SSL-CRT.crt"), keyfile=os.path.join(os.getcwd(), "SSL.key"))
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(('0.0.0.0', PortNum))
            self.s.listen(100)
            while not WillClosed[0]:
                full_data = b''
                Loop = True
                (insock, _) = self.s.accept()
                conn = _context.wrap_socket(insock, server_side=True)
                while Loop:
                    try:
                        data = conn.recv(1073741824)
                        if len(data) <= 0:
                            Loop = False
                        else:
                            full_data += data
                    except:
                        pass
                text = full_data.decode('utf-8')
                if text != '':
                    if text != '\u200B':
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
                    threading.Thread(target=self.send, daemon=True, args=(text, )).start()
                except:
                    pass
            except:
                pass

    def send(self, text):
        _context = ssl.create_default_context()
        _context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        _context.load_verify_locations(os.path.join(os.getcwd(), "SSL-CRT.crt"))
        _context.check_hostname = False
        conn = _context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.host)
        conn.connect((self.host, PortNum))
        conn.sendall(text.encode('utf-8'))


kivy_lang_sheet = """
<_MDFlatButton>:   
<_MDListWidget>:
<_MDLabel>:
Screen:
    size: (241, 412)
    BoxLayout:
        id: Layout
        orientation: 'vertical'
        size: (241, 412)
        MDTextField:
            id: TextFiled
            size: (30, 20)
            font_size: 50
            background_color: '#3d3d3d'
            foreground_color: '#FFFFFF'
            theme_height: 'Custom'
            theme_width: 'Custom'
            width: 200
            height: 30
            hint_text: '%s'
            font_name_hint_text: '_ja-JP'
            helper_text_mode: 'on_focus'
            on_focus: if self.focus: app.load_menu()
        _MDFlatButton:
            id: Btn1_send
            text: '%s'
            halign: 'center'
            theme_width: 'Custom'
            theme_height: 'Custom'
            theme_font_size: 'Custom'
            theme_line_height: 'Custom'
            pos: (10, 100)
            color: '#FF0808'
            width: 200
            height: 400
            outline_color: '#FF0808'
            outline_width: 3
            font_size: 130
            line_width: 2
            line_color: '#FF0808'
            on_press: app.send()
        MDScrollView:
            id: ListView
            halign: 'center'
            font_name: '_ja-JP'
            size: (50, 500)
            pos: (0, 500)
        _MDFlatButton:
            id: Btn2
            text: '%s'
            halign: 'center'
            font_size: 153
            theme_width: 'Custom'
            theme_height: 'Custom'
            theme_font_size: 'Custom'
            pos_hint: {'y': -10}
            color: '#FF0808'
            width: 200
            height: 400
            outline_color: '#FF0808'
            outline_width: 3
            line_width: 2
            line_color: '#FF0808'
            on_press: app.clear()
        MDScrollView:
            halign: 'center'
            id: Check_fxtwitter
        MDScrollView:
            halign: 'center'
            id: check_background
        _MDLabel:
            id: LabelIP
            halign: 'center'
            font_size: 130
            text: '{}'.format(app.get_ip())
        MDIconButton:
            id: lang
            icon: 'language.png'
            icon_size: 50
            icon_color: '#FF0C0C'
            theme_width: 'Custom'
            theme_height: 'Custom'
            theme_font_size: 'Custom'
            theme_line_height: 'Custom'
            pos_hint: {'center_x': .9}
            on_press: app.load_lang()
"""



class ClipboardShare(MDApp):
    dialog = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = '_ja-JP'
        Threads4[0] = send_Device_IP()
        Threads4[0] .start()
        Threads5[0] = ReceiveiP_Device()
        Threads5[0].start()
        if not os.path.exists(os.path.join(os.getcwd(), 'language_setting.txt')):
            with open(os.path.join(os.getcwd(), 'language_setting.txt'), 'w', encoding='utf-8') as _text:
                _text.write('ja-JP')
        text_language_code = open(os.path.join(os.getcwd(), 'language_setting.txt'), 'r', encoding='utf-8').read()
        if text_language_code == 'ja-JP':
            _kivy_lang_sheet = kivy_lang_sheet % ('対象のiPを入力してください...', '送信する', '内容を削除する')
        else:
            _kivy_lang_sheet = kivy_lang_sheet % ('please input target ip address...', 'send text', 'clear copied text')
        self.Screen = Builder.load_string(_kivy_lang_sheet)
        if platform == 'android':
            import android
            android.start_service(title='ClipShare', description='Monitoring Clipboard Service', arg='running')
        self.ReceiveClip = ReceiveClipboardText()
        self.Detection_clipboard = DetectClipboardText()
        self.WIDGET = _MDListWidget()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        self.title = 'ClipShare'
        if not os.path.exists(os.path.join(os.getcwd(), 'MemoSyncIcon.png')):
            with open(os.path.join(os.getcwd(), 'MemoSyncIcon.png'), 'wb') as fm:
                fm.write(base64.b64decode('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AQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIDAncCDuz/60yUC3/nOJz7xK7/y+PElc80hQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECKwh8La3/dIvffjDD/SF1sAeWOPhwDWXCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCGnJDKq4RIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CSgIdcJUhoCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECQwIackMqrhEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoJKAh1wlSGgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJDAhpyQyquESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEOgkoCHXCVIaAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAkMCzw5ddG26wFe+8ra3/eqvTh9vJAECBAgQIECAAAECBAgQIECAAAECBAgQIEDgFgLve98tVrXm/xfwHXJeBwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYU0JBbEFdqAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAhpyXgMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEFhTQkFsQV2oCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECGnJeAwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQWFNCQWxBXagIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIacl4DBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBBYUeHbB3FKfQOBRiYhXS0S8ViLicYk7gPr87s7wnx6UGL635tVr65i770v3dm2dl65bz2vVsZZD1tOqI+8vfcz93rqOpfdZ589919ennt/a69L1r933mM+ldY3lvfR+q56lHcbqbdU1Nu/S+639rl1Hq/6l62jtv1XPVq9PdVp6v1PrWMuxVc/SDlP316pv6vyp48b2u1YdU+utx11b39j+6/Va59fW0crb+3qv/U6tay8uU/fTe9zaPnOf/9r1tXwvrWPuflvr19cvrafOM3a+1jpjdbhPgAABAgQIEJgroCE3V8z4ewIvlYj4comIb5SIyEbd1A/Krf8hmDo/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IECAAAECBAgQIECgr4CGXF9P2QgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAjcE9CQu8fhhAABAgQIECBAgAABAgQIECBAgAABAgQIECBAgEBfAQ25vp6yESBAgAABAgQIECBAgAABAgQIECBAgAABAgQIELgnoCF3j8MJAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgb4CGnJ9PWUjQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgcE9AQ+4ehxMCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECfQU05Pp6ykaAAAECBAgQIECAAAECBAgQIECAAAECBAgQIEDgnoCG3D0OJwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgT6CmjI9fWUjQABAgQIECBAgAABAgQIECBAgAABAgQIECBAgMA9AQ25exxOCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECPQV0JDr6ykbAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgXsCGnL3OJwQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ6CugIdfXUzYCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC9wQ05O5xOCFAgAABAgQIECBAgAABAgQIECBAgAABAgQIECDQV0BDrq+nbAQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgTuCWjI3eNwQoAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQKCvgIZcX0/ZCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECNwT0JC7x+GEAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQF8BDbm+nrIRIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQuCegIXePwwkBAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBvgIacn09ZSNAgAABAgQIECBAgAABAgQIECBAgAABAgQIECBwT0BD7h6HEwIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJ9BTTk+nrKRoAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQOCegIbcPQ4nBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBPoKaMj19ZSNAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAwD0BDbl7HE4IECBAgAABAgQIECBAgAABAgQIECBAgAABAgQI9BXQkOvrKRsBAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBewIacvc4nBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDoK6Ah19dTNgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQL3BDTk7nE4IUCAAAECBAgQIECAAAECBAgQIECAAAECBAgQINBXQEOur6dsBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBO4JaMjd43BCgAABAgQIECBAgAABAgQIECBAgAABAgQIECBAoK+AhlxfT9kIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQI3BPQkLvH4YQAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBAXwENub6eshEgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBC4J6Ahd4/DCQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIG+AhpyfT1lI0CAAAECBAgQIECAAAECBAgQIECAAAECBAgQIHBPQEPuHocTAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAn0FNOT6espGgAABAgQIECBAgAABAgQIECBAgAABAgQIECBA4J6Ahtw9DicECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIE+gpoyPX1lI0AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIDAPQENuXscTggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAj0FdCQ6+spGwECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIF7As/eO3NCgAABAgQIECBAgMApBV4uEfHtEhF5nsdXSkR8r8TdsXX/UYmI10rckT4ucXf+oMTd+cMSEc+UiHhTiYgfKBHx5hJ311v3c9wPlribd7eSPxEgQIAAAQIECBAgQIAAgfUENOTWs7YSAQIECBAgQIAAge4C2RD7WomIb5SI+FaJiBdL3J3n9fqYDbfuBW4kYTb03l4ionV8R4m7++8sEfHDJTT2NvI4lUGAAAECBAgQIECAAIHdCWjI7e6RKZgAAQIECBAgQOCIAvmdZNlQ+3qJiOdLRGTDLY95PRtrRzTpuadsOKZbHueukY28d5W4a9Rlwy6vv7tERDb08jv/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0XUaur7u+EM9H3rdfXWd22Xf9R1b17H9zu20r0OrrrHW2Zqv73irnlPX2Tdv93yrjm67cz0/9/r3Xde5nVoO566jXrhSj6269nXUbt0CNuTWfX1HW91tmYjnZUabxsATCZz7B9dEy+yd1g/QXiINzijweCbic5mIb2TOWICpCEwgUD+P9v1+XO2r1OrXPV7nPc5ToHu96jp2q+226573fFiBrnfruvTN2hqne7xvHOePE2g5t65nq/1xs6+v11MyEf86E9F17D7f17PbryvXGqeOt/rX+e54rfbVbt9+rXaHjlPtu4/d8Vt1d9vVOHW81a/brp7XY/Wrcep467HaVb9qV8freeux26/bbt9xuv3qefVvzVPnq33rsduuxuseb/U/9XjffK06ql/N32pXx7vtq189Vrt6vu9jq193vla7feep8VrjdI9X++743Xbd89Wv1a51vK9fd556Xv3qefexNV8db/Wv893xjn1+7Hjdfq16j62r+nXnqeN9j91+VV/3eN84db761Tjd4/W8+9htX+drvHrefTy0X2u8emVc/b68XrjSnc9zAv8oYEPO18FRAq1vWEcNptPsBFzf2V0SBRGI+p9WL89E/I8MGALrFjj051Grfev4uvWWu7p9r9e+7ZYroXICBOYu8NpMxL2ZuVfbX99Q31dbv7Dsr0CLOQm4jsNejaH+fg1Vles7lOQyxjnX9Z7b1/lUV4fDVPLLmNeG3DKukyoJECBAgEAKvCpjQ86XAwECBAgQIEBgaoG6L/OLt6uvBI+rPZb6zHVc6pXbr27Xdz8nrQgQIDC0wOWhBzQeAQIECBAgMJ7AMzMR92XGm8fIBAgQIECAAAECFwvUfVjdl13cylECBAgQIECAAAECVwvYkLvawzMCBAgQILAIgfof2YsoVpEECBAgQIAAgRUJuA9b0cW0FAIECBAgQIDAGQVsyJ0R21QECBAgQGAogfpFUH223FDjGocAAQIECBAgQOBigbrvqvuwi1s5SoAAAQIECBAgQOBiARtyF7s4SoAAAQIEZi1weybiZZlZl6o4AgQIECBAgMAqBOq+q+7DVrEoiyBAgAABAgQIEDibgA25s1GbiAABAgQIDC/whszw4xqRAAECBAgQIEDgagH3XVd7eEaAAAECBAgQIHCYgA25w7y0JkCAAAECsxJ4TibiWZlZlaYYAgQIECBA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ECBAgAABAgQIECBAgACBQQRuzET8u0zEqzKDDG2QCwQ+mon4jUzElcwFDR0iQIAAAQIECEwkYENuInjTEiBAgAABAgQIECBAgAABAusXuJyJ+OFMxJsy61/3VCv8w0zEhzMR381MVY15CRAgQIAAAQI7ARtyOwt/IkCAAAECBAgQIECAAAECBAiMKvAvMhFvy4w61aYH/0wm4hcyEd/ObJrE4gkQIECAAIGJBWzITXwBTE+AAAECBAgQIECAAAECBAhsT+ANmYgfy0TUK+m2JzHuir+Uifj5TMRDmXHnNDoBAgQIECBA4CIBG3IXqThGgAABAgQIECBAgAABAgQIEDiDwEszET+Vibg5c4aJNzbFg5ndxtxXMhtDsFwCBAgQIEBgUgEbcpPym5wAAQIECBAgQIAAAQIECBAgEPE9mYifzUTcniEztMDDmYgPZCI+nxl6FuMRIECAAAECBK4VsCF3rYkjBAgQIECAAAECBAgQIECAAIFJBO7LRPxcJuLuzCSlrHrSRzIR/z4T8ceZVS/Z4ggQIECAAIGJBWzITXwBTE+AAAECBAgQIECAAAECBAgQ6ArcmdltzD07023l+akCj2cifjUT8T8zp46qPwECBAgQIEDgWgEbcteaOEKAAAECBAgQIECAAAECBAgQmIXArZmIn8lEvCgzi9JWWcR/zkT8VmaVS7QoAgQIECBAYCIBG3ITwZuWAAECBAgQIECAAAECBAgQILCvwI2ZiHdmIl6d2be3docK/E4m4iOZiHol3aHjaE+AAAECBAgQKAEbciXhkQABAgQIECBAgAABAgQIECAwc4FLmYgfykS8OTPzohdc3icyEb+cifhuZsELUjoBAgQIECAwmYANucnoTUyAAAECBAgQIECAAAECBAgQOE3gn2ci3p45bSy92wJ/non4hUzEtzPt9s4QIECAAAECBLoCNuS6Ip4TIECAAAECBAgQIECAAAECBBYm8PpMxI9lIi5nFraIBZT7pUzEz2ciHsosoHAlEiBAgAABApML2JCb/BIogAABAgQIECBAgAABAgQIECAwjMBLMxHvzkTckhlmbKPsBB7M7DbmvpLZnfcnAgQIECBAgEBXwIZcV8RzAgQIECBAgAABAgQIECBAgMDCBe7PRPxMJuKOzMIXNcPyH85EfCAT8ZeZGRaqJAIECBAgQGByARtyk18CBRAgQIAAAQIECBAgQIAAAQIExhF4Ribi5zIR92TGmWvLoz6SifhQJuKPM1sWsXYCBAgQIECgK2BDriviOQECBAgQIECAAAECBAgQIEBgZQJPzUS8NxPx7MzKFjmD5TyeifjVTMTvZWZQmBIIECBAgACByQVsyE1+CRRAgAABAgQIECBAgAABAgQIEDiPwK2Z3VtZfm/mPHNvcZbfzET8VmaLAtZMgAABAgQIlIANuZLwSIAAAQIECBAgQIAAAQIECBDYiMCNmYh/l4l4TWYji59gmb+TifhIJqJeSTdBKaYkQIAAAQIEJhKwITcRvGkJECBAgAABAgQIECBAgAABAlMLXMpE/GAm4i2Zqata7/yfyER8OBPxaGa967UyAgQIECBAYCdgQ25n4U8ECBAgQIAAAQIECBAgQIAAgU0LvDUT8fbMpilGXfxnMxEfzER8KzPqlAYnQIAAAQIEJhawITfxBTA9AQIECBAgQIAAAQIECBAgQGBuAq/PRPxEJuJyZm5VLr+eL2Ui3peJ+LvM8tdlBQQIECBAgMC1AjbkrjVxhAABAgQIECBAgAABAgQIECBA4B8EXpyJ+OlMxC0ZNEMLPJjZbcx9JTP0LMYjQIAAAQIEphSwITelvrkJECBAgAABAgQIECBAgAABAgsQeF4m4j2ZiDsyCyh8YSU+nIn4QCbic5mFLUK5BAgQIECAwIUCNuQuZHGQAAECBAgQIECAAAECBAgQIECgK3BfJuK9mYh7M91Wnp8q8Egm4hczEZ/KnDqq/gQIECBAgMCUAjbkptQ3NwECBAgQIECAAAECBAgQIEBggQJ3ZiJ+NhPx3MwCFzLzkh/PRPyHTMTvZmZetPIIECBAgACBCwVsyF3I4iABAgQIECBAgAABAgQIECBAgECfwK2Z3WfMPZDp6+X8oQKXMhH/JbN7vJI5dDTtCRAgQIAAgSkEbMhNoW5OAgQIECBAgAABAgQIECBAgMCKBG7MRPxEJuI1mRUtcGZLqVfKfSQTUa+km1mZyiFAgAABAgSeJGBD7kkY/kiAAAECBAgQIECAAAECBAgQIHC8QL2S6wczEW/NHD+entcX+KNMxC9lIh7NXL+PswQIECBAgMA0AjbkpnE3KwECBAgQIECAAAECBAgQIEBg9QJvyUT8QCaiNuxWv/AzL/AvMhG/kIn4ZubMRZiOAAECBAgQuK6ADbnr8jhJgAABAgQIECBAgAABAgQIECBwqsDrMhE/nom4nDl1VP27An+diXhfJuLrmW4rzwkQIECAAIEpBGzITaFuTgIECBAgQIAAAQIECBAgQIDABgVenIl4dybi5swGIUZecm3EvT8T8eXMyJMangABAgQIELiugA256/I4SYAAAQIECBAgQIAAAQIECBAgMLTA/ZmIn8tE3JEZehbjPZyJ+EAm4nMZLgQIECBAgMAUAjbkplA3JwECBAgQIECAAAECBAgQIECAQNyb2W3MPT0DZmiBRzMRv5iJ+GRm6FmMR4AAAQIECFxPwIbc9XScI0CAAAECBAgQIECAAAECBAgQGF3gqZmI92QinpMZfdrNTfB4JuLXMhG/m9kcgwUTIECAAIFJBGzITcJuUgIECBAgQIAAAQIECBAgQIAAga7ArZndZ8w9kOm28vxUgUuZiP+S2T1eyZw6uv4ECBAgQIDARQI25C5ScYwAAQIECBAgQIAAAQIECBAgQGAygRszET+RiXhNZrJyVj9xvVLu1zMR9Uq61S/cAgkQIECAwBkFbMidEdtUBAgQIECAAAECBAgQIECAAAEC+wvUK7l+MBPx1sz+/bU8TOBTmYhfykQ8kjlsDK0JECBAgACBiwVsyF3s4igBAgQIECBAgAABAgQIECBAgMDMBN6Sifg3mYjasJtZmYsv5y8yEb+QifhmZvHLsgACBAgQIDCpgA25SflNToAAAQIECBAgQIAAAQIECBAgcKjAazO7t7S8IXPoKNr3CXw5E/G+TMTXM329nCdAgAABAgQuErAhd5GKYwQIECBAgAABAgQIECBAgAABArMXeCAT8e5MxC2Z2Ze9uAJrI6425mqjbnELUTABAgQIEJhQwIbchPimJkCAAAECBAgQIECAAAECBAgQOF3guZmI92Yi7sicPq4Rrhaot678QCai3try6laeESBAgAABAhcJXLrooGP7C3w2c+XK/j3W1fI7mYhvZyKuZMZf46HvEX+uumrlrfqGrqM1T9Vx6GNrvFPrbo17aH19dQw1T9U19HhV/9DjVr37PlYd+7avdkPXXXUMNe6p41Q9td7W46nztMat4/uOv2+9NW73cd95uv26z/vGObbOvnG7dfQ9P7aOvnG754euuzv+UM+PrfNQx2PnGWqd+44zdp3lNvY8+6636tm3fbUbqv4a59g6qp7uY43b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R2ry3EzEj2YiLmVGmsywBAgQILBYARtyi710CidAgAABAgQIECBAgAABAgQIECCwXYGbMxHvykS8InM+j3szEe/MRNyYOd/8ZiJAgACBZQnYkFvW9VItAQIECBAgQIAAAQIECBAgQIAAAQJPEricifiRTMQbM09qMPAf78jsNgJvzQw8ieEIECBAYHUCNuRWd0ktiAABAgQIECBAgAABAgQIECBAgMD2BOqtIr8vE/G2TMSVzOke9Yq8n8pE3Jk5fVwjECBAgMA2BGzIbeM6WyUBAgQIECBAgAABAgQIECBAgACBTQm8IRPxjszxn+1Wr8D7yUzE0zOborRYAgQIEBhAwIbcAIiGIECAAAECBAgQIECAAAECBAgQIEBgngL12XL1WXM3ZfprrVfc/Vgm4v5Mfz8tCBAgQIDARQI25C5ScYwAAQIECBAgQIAAAQIECBAgQIAAgVUJvCAT8Z5MxFMy7SW+PRPx4ky7nTMECBAgQGAfARty+yhpQ4AAAQIECBAgQIAAAQIECBAgQIDAKgSemYl4bybirsxuaW/JRLwuszvuTwQIECBA4BSBS6d01jfis5krV1gQIECAAAECBAgQIECAAAECBAgQILA8gW9mIv4wE/GmzPLWoWICBAj0Cbwwc8m+UB/USOe9Qm4kWMMSIECAAAECBAgQIECAAAECBAgQIDB/gXrrShtx879WKiRAgMCSBWzILfnqqZ0AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQGD2AjbkZn+JFEiAAAECBAgQIECAAAECBAgQIECAAAECBAgQILBkARtyS756aidAgAABAgQIECBAgAABAgQIECBAgAABAgQIEJi9gA252V8iBRIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECCxZwIbckq+e2gkQIECAAAECBAgQIECAAAECBAgQIECAAAECBGYvYENu9pdIgQQIECBAgAABAgQIECBAgAABAgQIECBAgAABAksWsCG35KundgIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgdkL2JCb/SVSIAECBAgQIECAAAECBAgQIECAAAECBAgQIECAwJIFbMgt+eqpnQABAgQIECBAgAABAgQIECBAgAABAgQIECBAYPYCNuRmf4kUSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgsGQBG3JLvnpqJ0CAAAECBAgQIECAAAECBAgQIECAAAECBAgQmL2ADbnZXyIFEiBAgAABAgQIECBAgAABAgQIECBAgAABAgQILFnAhtySr57aCRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEZi9gQ272l0iBBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECSxawIbfkq6d2AgQIECBAgAABAgQIECBAgAABAgQIECBAgACB2QvYkJv9JVIgAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIDAkgVsyC356qmdAAECBAgQIECAAAECBAgQIECAAAECBAgQIEBg9gI25GZ/iRRIgAABAgQIECBAgAABAgQIECBAgAABAgQIECCwZAEbcku+emonQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCYvYANudlfIgUSIECAAAECBAgQIECAAAECBAgQIECAAAECBAgsWcCG3JKvntoJECBAgAABAgQIECBAgAABAgQIECBAgAABAgRmL2BDbvaXSIEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJLFrAht+Srp3YCBAgQIECAAAECBAgQIECAAAECBAgQIECAAIHZC9iQm/0lUiABAgQIECBAgAABAgQIECBAgAABAgQIECBAgMCSBWzILfnqqZ0AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQGD2AjbkZn+JFEiAAAECBAgQIECAAAECBAgQIECAAAECBAgQILBkARtyS756aidAgAABAgQIECBAgAABAgQIECBAgAABAgQIEJi9wP/fnh3TAADAMAzjz3o0Gs0MKveMIDd/kYEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJlAUGu/J7tBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC8wKC3PxFBhIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECJQFBLnye7YTIECAAAECBAgQIECAAAECBAgQIECAAAECBAjMCwhy8xcZSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgUBYQ5Mrv2U6AAAECBAgQIECAAAECBAgQIECAAAECBAgQIDAvIMjNX2QgAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBAWUCQK79nOwECBAgQIECAAAECBAgQIECAAAECBAgQIECAwLyAIDd/kYEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJlAUGu/J7tBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC8wKC3PxFBhIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECJQFBLnye7YTIECAAAECBAgQIECAAAECBAgQIECAAAECBAjMCwhy8xcZSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgUBYQ5Mrv2U6AAAECBAgQIECAAAECBAgQIECAAAECBAgQIDAvIMjNX2QgAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBAWUCQK79nOwECBAgQIECAAAECBAgQIECAAAECBAgQIECAwLyAIDd/kYEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJlAUGu/J7tBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC8wKC3PxFBhIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECJQFBLnye7YTIECAAAECBAgQIECAAAECBAgQIECAAAECBAjMCwhy8xcZSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgUBYQ5Mrv2U6AAAECBAgQIECAAAECBAgQIECAAAECBAgQIDAvIMjNX2QgAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBAWUCQK79nOwECBAgQIECAAAECBAgQIECAAAECBAgQIECAwLyAIDd/kYEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJlAUGu/J7tBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC8wKC3PxFBhIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECJQFBLnye7YTIECAAAECBAgQIECAAAECBAgQIECAAAECBAjMCwhy8xcZSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgUBYQ5Mrv2U6AAAECBAgQIECAAAECBAgQIECAAAECBAgQIDAvIMjNX2QgAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBAWUCQK79nOwECBAgQIECAAAECBAgQIECAAAECBAgQIECAwLyAIDd/kYEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJlAUGu/J7tBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC8wKC3PxFBhIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECJQFBLnye7YTIECAAAECBAgQIECAAAECBAgQIECAAAECBAjMCwhy8xcZSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgUBYQ5Mrv2U6AAAECBAgQIECAAAECBAgQIECAAAECBAgQIDAvIMjNX2QgAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBAWUCQK79nOwECBAgQIECAAAECBAgQIECAAAECBAgQIECAwLyAIDd/kYEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJlAUGu/J7tBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC8wKC3PxFBhIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECJQFBLnye7YTIECAAAECBAgQIECAAAECBAgQIECAAAECBAjMCwhy8xcZSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgUBYQ5Mrv2U6AAAECBAgQIECAAAECBAgQIECAAAECBAgQIDAvIMjNX2QgAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBAWUCQK79nOwECBAgQIECAAAECBAgQIECAAAECBAgQIECAwLyAIDd/kYEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJlAUGu/J7tBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC8wKC3PxFBhIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECJQFBLnye7YTIECAAAECBAgQIECAAAECBAgQIECAAAECBAjMCwhy8xcZSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgUBYQ5Mrv2U6AAAECBAgQIECAAAECBAgQIECAAAECBAgQIDAvIMjNX2QgAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBAWUCQK79nOwECBAgQIECAAAECBAgQIECAAAECBAgQIECAwLyAIDd/kYEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJlAUGu/J7tBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC8wKC3PxFBhIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECJQFBLnye7YTIECAAAECBAgQIECAAAECBAgQIECAAAECBAjMCwhy8xcZSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgUBYQ5Mrv2U5y46BmAAAHFklEQVSAAAECBAgQIECAAAECBAgQIECAAAECBAgQIDAvIMjNX2QgAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBAWUCQK79nOwECBAgQIECAAAECBAgQIECAAAECBAgQIECAwLyAIDd/kYEECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQJlAUGu/J7tBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC8wKC3PxFBhIgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECJQFBLnye7YTIECAAAECBAgQIECAAAECBAgQIECAAAECBAjMCwhy8xcZSIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgUBYQ5Mrv2U6AAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECfwQOHCyP1vHKvKEAAAAASUVORK5CYII='))
        self.icon = os.path.join(os.getcwd(), 'MemoSyncIcon.png')
        if not os.path.exists(os.path.join(os.getcwd(), 'ClipBoardCopy.png')):
            with open(os.path.join(os.getcwd(), 'ClipBoardCopy.png'), 'wb') as fc:
                fc.write(base64.b64decode('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'))
        if not os.path.exists(os.path.join(os.getcwd(), 'ip_address_list')):
            with open(os.path.join(os.getcwd(), 'ip_address_list'), 'w', encoding='utf-8') as f:
                f.write('{"192.168.1.0": "0"}')
        self.text_menu = MDDropdownMenu(caller=self.Screen.ids['TextFiled'], hor_growth='left', position='bottom', max_height=700)
        self.text_menu.position = 'top'
        self.text_menu.width = 400
        self.text_menu.pos_hint = {'x': 0}
        self.LangBtn = MDDropdownMenu(caller=self.Screen.ids['lang'], hor_growth='left', position='bottom')
        self.LangBtn.position = 'top'
        self.Detection_clipboard.bind(on_detection=lambda _c: self.auto_get_and_send_clipboard())
        self.ReceiveClip.bind(on_receive=lambda _li: self.add_list())
        self.bind(on_stop=lambda _: self.closed())
        self.ClipText = ''
        self.Screen.ids['ListView'].add_widget(self.WIDGET)
        self.Screen.ids['Check_fxtwitter'].add_widget(_MDLabelCheckBox())
        self.Screen.ids['check_background'].add_widget(_MDLabelCheckBox2())
        self.dialog = MDDialog(text="please Restart App")

    def build(self):
        return self.Screen

    @mainthread
    def load_lang(self):
        self.LangBtn.items = [
            {'text': 'japanese', 'viewclass': 'OneItemText', 'on_release': lambda text='ja-JP': self.lang_callback(text)},
            {'text': 'English', 'viewclass': 'OneItemText', 'on_release': lambda text='en-US': self.lang_callback(text)}
        ]
        self.LangBtn.open()

    @mainthread
    def load_menu(self):
        self.text_menu.items = self.sort_dict([{'text': ips, 'viewclass': 'OneItemText', 'on_release': lambda text=ips: self.menu_callback(text)} for ips, _ in json.load(open(os.path.join(os.getcwd(), 'ip_address_list'), 'r', encoding='utf-8')).items() if ips != ''])
        self.text_menu.open()

    def menu_callback(self, text):
        self.Screen.ids['TextFiled'].text = text
        self.text_menu.dismiss()

    def lang_callback(self, text):
        if text == 'ja-JP':
            with open(os.path.join(os.getcwd(), 'language_setting.txt'), 'w', encoding='utf-8') as _text:
                _text.write('ja-JP')
        else:
            with open(os.path.join(os.getcwd(), 'language_setting.txt'), 'w', encoding='utf-8') as _text:
                _text.write('en-US')
        self.restart_dialog(text)
        self.LangBtn.dismiss()

    @mainthread
    def restart_dialog(self, text):
        self.dialog = _MDDialog(text="please Restart App", buttons=[_MDFlatButton(text="Close App", theme_text_color="Custom", text_color='#FF0C0C', on_release=self.close_alert)])
        self.dialog.open()

    def close_alert(self, o):
        self.dialog.dismiss()
        self.stop()

    @mainthread
    def auto_get_and_send_clipboard(self):
        if if_check1[0]:
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
            clipboard.Clipboard.copy('{}'.format(text))
        if clipboard.Clipboard.paste() != '':
            if clipboard.Clipboard.paste() != '\u200B':
                self.add_list2()

    def sort_dict(self, data: list[dict]) -> list[dict]:
        return list({element['text']: element for element in data}.values())

    @mainthread
    def add_list(self):
        clip = clipboard.Clipboard.paste()
        if clipboard.Clipboard.paste() != '':
            if clip != '\u200B':
                if clip != self.ClipText:
                    if if_check1[0]:
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
                    if self.Screen.ids['TextFiled'].text != '':
                        if self.Screen.ids['TextFiled'].text != '\u200B':
                            SendText(host=self.Screen.ids['TextFiled'].text, text=clip)
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
                    self.WIDGET.set_widget(widget=widget)
                    _was_get_list.append(clip)

    def add_list2(self):
        clip = clipboard.Clipboard.paste()
        if clipboard.Clipboard.paste() != '':
            if clip != '\u200B':
                if clip != self.ClipText:
                    if if_check1[0]:
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
                    if self.Screen.ids['TextFiled'].text != '':
                        if self.Screen.ids['TextFiled'].text != '\u200B':
                            SendText(host=self.Screen.ids['TextFiled'].text, text=clip)
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
                    self.WIDGET.set_widget(widget=widget)
                    _was_get_list.append(clip)

    @mainthread
    def copy_text(self, widget):
        clipboard.Clipboard.copy(self.WIDGET.get_text(widget=widget))

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
            Threads4[0].join(0)
        except:
            pass
        try:
            Threads5[0].join(0)
        except:
            pass

    def get_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(('8.8.8.8', 80))
            return sock.getsockname()[0]

    def send(self):
        if self.Screen.ids['TextFiled'].text != '\u200B':
            SendText(host=self.Screen.ids['TextFiled'].text, text=clipboard.Clipboard.paste())

    @mainthread
    def clear(self):
        self.WIDGET.delete_all()
        clipText[0] = ''
        clipboard.Clipboard.copy('\u200B')
        _was_get_list.clear()


if __name__ == '__main__':
    ClipboardShare().run()
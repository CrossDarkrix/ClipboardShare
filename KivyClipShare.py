#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Version 3.3b

import asyncio
import os
import socket
import time
import threading
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
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.list.list import IconLeftWidget
from kivymd.uix.widget import MDWidget
from kivymd.uix.selectioncontrol.selectioncontrol import MDCheckbox
from kivymd.uix.menu import MDDropdownMenu

WillClosed = [False]
Threads = [None]
Threads2 = [None]
Threads3 = [None]
_was_get_list = []
PortNum = 50618
clipText = [clipboard.Clipboard.paste()]
allow_bk = [True]
out_thread = []
if_check1 = [False]
if_check2 = [False]


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
        self.label.font_size = 75
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.checkbox)
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
        self.label.font_size = 47
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.checkbox)
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


class DetectChange_iP(EventDispatcher):
    def __init__(self, **kwargs):
        super(DetectChange_iP, self).__init__(**kwargs)
        self.register_event_type('on_change_ip')
        self.ip = ''
        _thread = threading.Thread(target=asyncio.run, daemon=True, args=(self.check(), ))
        Threads3[0] = _thread
        _thread.start()

    def on_change_ip(self):
        pass

    async def check(self):
        while not WillClosed[0]:
            if self.ip != self.check_ip():
                try:
                    await self.dispatch('on_change_ip')
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
            size: (50, 20)
            font_size: 50
            background_color: '#3d3d3d'
            foreground_color: '#FFFFFF'
            theme_height: 'Custom'
            theme_width: 'Custom'
            width: 200
            height: 80
            hint_text: '対象のiPを入力してください...'
            font_name_hint_text: '_ja-JP'
            helper_text_mode: 'on_focus'
            on_focus: if self.focus: app.load_menu()
        _MDFlatButton:
            id: Btn1_send
            text: '送信する'
            halign: 'center'
            theme_width: 'Custom'
            theme_height: 'Custom'
            theme_font_size: 'Custom'
            theme_line_height: 'Custom'
            pos: (0, 100)
            color: '#FF0808'
            width: 200
            height: 400
            font_size: 130
            outline_color: '#FF0808'
            outline_width: 3
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
            text: '内容を削除する'
            halign: 'center'
            theme_width: 'Custom'
            theme_height: 'Custom'
            theme_font_size: 'Custom'
            color: '#FF0808'
            width: 200
            height: 400
            font_size: 130
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
            text: '{}'.format(app.get_ip())
            font_size: 130
"""



class ClipboardShare(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = '_ja-JP'
        self.Screen = Builder.load_string(kivy_lang_sheet)
        if platform == 'android':
            import android
            android.start_service(title='ClipShare', description='Monitoring Clipboard Service', arg='running')
        self.ReceiveClip = ReceiveClipboardText()
        self.Detection_clipboard = DetectClipboardText()
        self.WIDGET = _MDListWidget()
        self.CheckiP = DetectChange_iP()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        self.title = 'ClipShare'
        self.icon = os.path.join(os.getcwd(), 'images', 'MemoSyncIcon.png')
        if not os.path.exists(os.path.join(os.getcwd(), 'ip_address_list.txt')):
            with open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'w', encoding='utf-8') as ip:
                ip.write('192.168.1.0, ')
        else:
            text_ip = ', '.join(list(set(open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'r', encoding='utf-8').read().split(', '))))
            with open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'w', encoding='utf-8') as fw:
                fw.write(text_ip)
        self.text_menu = MDDropdownMenu(caller=self.Screen.ids['TextFiled'])
        self.text_menu.position = 'top'
        self.text_menu.width = 400
        self.Detection_clipboard.bind(on_detection=lambda _c: self.auto_get_and_send_clipboard())
        self.ReceiveClip.bind(on_receive=lambda _li: self.add_list())
        self.bind(on_stop=lambda _: self.closed())
        self.ClipText = ''
        self.Screen.ids['ListView'].add_widget(self.WIDGET)
        self.Screen.ids['Check_fxtwitter'].add_widget(_MDLabelCheckBox())
        self.Screen.ids['check_background'].add_widget(_MDLabelCheckBox2())

    def build(self):
        return self.Screen

    @mainthread
    def load_menu(self):
        if 9 <= len(self.Screen.ids['TextFiled'].text) <= 15:
            if self.count_dot(text=self.Screen.ids['TextFiled'].text):
                if not os.path.exists(os.path.join(os.getcwd(), 'ip_address_list.txt')):
                    with open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'w', encoding='utf-8') as ip:
                        ip.write('192.168.1.0, ')
                else:
                    with open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'a', encoding='utf-8') as ip:
                        ip.write(', {}, '.format(self.Screen.ids['TextFiled'].text))
                        text_ip = ', '.join(list(set(open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'r', encoding='utf-8').read().split(', '))))
                        with open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'w', encoding='utf-8') as fw:
                            fw.write(text_ip)
        self.text_menu.items = self.sort_dict([{'text': ips, 'viewclass': 'OneLineListItem', 'on_release': lambda text=ips: self.menu_callback(text)} for ips in open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'r', encoding='utf-8').read().split(', ') if ips != ''])
        self.text_menu.open()

    def count_dot(self, text: str) -> bool:
        if text.count('.') == 4:
            return True
        else:
            return False

    def menu_callback(self, text):
        self.Screen.ids['TextFiled'].text = text
        self.text_menu.dismiss()

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

    def get_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(('8.8.8.8', 80))
            return sock.getsockname()[0]

    def send(self):
        if self.Screen.ids['TextFiled'].text.startswith('192') or self.Screen.ids['TextFiled'].text.startswith('127') or self.Screen.ids['TextFiled'].text == '' and 8 <= len(self.Screen.ids['TextFiled'].text):
            if self.Screen.ids['TextFiled'].text != '':
                SendText(host=self.Screen.ids['TextFiled'].text, text=clipboard.Clipboard.paste())
        if 9 <= len(self.Screen.ids['TextFiled'].text) <= 15:
            if not os.path.exists(os.path.join(os.getcwd(), 'ip_address_list.txt')):
                with open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'w', encoding='utf-8') as ip:
                    ip.write('192.168.1.0, ')
            else:
                with open(os.path.join(os.getcwd(), 'ip_address_list.txt'), 'a', encoding='utf-8') as ip:
                    ip.write(', {}, '.format(self.Screen.ids['TextFiled'].text))

    @mainthread
    def clear(self):
        self.WIDGET.delete_all()
        # clipboard.Clipboard.copy('\uFEFF')
        clipboard.Clipboard.copy('\u200B')
        _was_get_list.clear()


if __name__ == '__main__':
    ClipboardShare().run()
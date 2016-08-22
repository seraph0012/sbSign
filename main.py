# -*- coding: utf-8 -*-
import kivy
kivy.require('1.9.1-dev')

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.garden import filebrowser

import os
from PIL import Image
from kivy.app import App
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import kivy.utils as kutils


class MyFileChooser(BoxLayout):
    choose = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MyColorPicker(BoxLayout):
    old_color = ListProperty([])
    new_color = ListProperty([])
    submit = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SBSignWidget(BoxLayout):
    input_img = None

    def dismiss_popup(self):
        self._popup.dismiss()

    def on_outer_pick(self):
        self.ids.outer_btn.background_color = self.picker.new_color
        self._popup.dismiss()

    def on_inner_pick(self):
        self.ids.inner_btn.background_color = self.picker.new_color
        self._popup.dismiss()

    def on_file(self, path, filename):
        with Image.open(os.path.join(path, filename[0])) as img:
            self.input_img = os.path.join(path, filename[0])
        self.dismiss_popup()

    def on_picker(self, picker):
        self.picker = MyColorPicker(cancel=self.dismiss_popup, 
            old_color = self.ids[picker + '_btn'].background_color)
        self.picker.submit = self.on_outer_pick if picker == 'outer' else self.on_inner_pick
        self._popup = Popup(title="选择颜色", content=self.picker,
                            title_font = 'simsun.ttc',
                            size_hint=(None, None), size = (400, 400))
        self._popup.open()

    def on_file_choose(self):
        content = MyFileChooser(cancel=self.dismiss_popup,
            choose=self.on_file)
        self._popup = Popup(title="选择图片文件", content=content,
                            title_font = 'simsun.ttc',
                            size_hint=(0.95, 0.95))
        self._popup.open()

    def on_gen_commands(self):
        out_file = open('meow.txt', 'w')
        pre_command = '/spawnitem customsign 1 \'{"signData":["?replace;'

        after_command = 'frameColors":["{}", "{}"]\''.format(
            kutils.get_hex_from_color(self.ids.inner_btn.background_color),
            kutils.get_hex_from_color(self.ids.outer_btn.background_color))

        raw_img = Image.open(self.input_img)
        x, y = raw_img.size
        rgb_img = raw_img.convert('RGB')
        w = x / 32
        h = y / 8
        for i in range(w):
            for j in range(h):
                out_file.write('{} {}\n'.format(i + 1, j + 1))
                out_str = pre_command
                for ii in range(32):
                    for jj in range(8):
                        pos = '{}00{}01'.format(str(ii + 1).zfill(2), str(8 - jj).zfill(2))
                        r, g, b, = rgb_img.getpixel((i * 32 + ii, j * 8 + jj))
                        out_str += '{}={}ff;'.format(pos, kutils.get_hex_from_color((r/255.0, g/255.0, b/255.0))[1:])
                out_file.write(out_str + '\n')
        raw_img.close()



class SBSignApp(App):
    def build(self):
        return SBSignWidget()

if __name__ == '__main__':\
    SBSignApp().run()
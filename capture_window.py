__author__ = 'tkcook'

import gphoto2 as gp
from gi.repository import Gtk, GLib, GdkPixbuf, Gio
import time
from components import FileManager
from glob import glob
import os

def set_config(camera, context, configs):
    config = camera.get_config(context)
    for name, value in configs:
        child = None
        for n in name:
            child = config.get_child_by_name(n)
        child.set_value(value)

    camera.set_config(config, context)

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Preview')
        box = Gtk.Box()
        self.files = FileManager()
        box.add(self.files)

        self.event_box = Gtk.EventBox()
        self.image = Gtk.Image()
        self.event_box.add(self.image)
        box.add(self.event_box)
        self.connect('delete-event', Gtk.main_quit)
        self.camera = gp.Camera()
        self.context = gp.Context()
        self.camera.init(self.context)

        configs = [
            (['settings', 'capture'], 1),
            (['imgsettings', 'iso'], '100') # 1 = ISO 100
        ]

        set_config(self.camera, self.context, configs)
        time.sleep(1)
        GLib.idle_add(self.show_preview)
        self.event_box.connect('button_press_event', self.capture)

        self.add(box)

    def set_pixbuf(self, buf):
        self.image.set_from_pixbuf(buf)
        pass

    def show_preview(self):
        file = gp.CameraFile()
        self.camera.capture_preview(file, self.context)
        data = file.get_data_and_size()
        data = memoryview(data)
        stream = Gio.MemoryInputStream.new()
        stream.add_data(data)
        pixbuf = GdkPixbuf.Pixbuf.new_from_stream(stream)
        self.set_pixbuf(pixbuf)
        return True

    def capture(self, a, b):
        file = self.camera.capture(gp.GP_CAPTURE_IMAGE, self.context)
        data = self.camera.file_get(file.folder, file.name, gp.GP_FILE_TYPE_NORMAL, self.context)
        data = data.get_data_and_size()

        dest_path = self.files.get_path_for_selection()
        files = sorted(glob(os.path.join(dest_path, 'img*.jpg')))
        max = int(os.path.basename(files[-1])[3:-4]) if len(files) > 0 else -1
        fname = os.path.join(dest_path, 'img{:05d}.jpg'.format(max+1))
        with open(fname, 'wb') as outfile:
            outfile.write(memoryview(data))
        self.files.fill_tree()

    def run(self):
        Gtk.main()
        self.camera.exit(self.context)
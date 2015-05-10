__author__ = 'tkcook'

from gi.repository import Gtk
import os

class FileManager(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.button = Gtk.FileChooserButton(title='Choose a Root Folder', action=Gtk.FileChooserAction.SELECT_FOLDER)
        self.button.set_current_folder(os.getcwd())
        self.button.connect('file-set', self.do_file_set)

        self.treestore = Gtk.TreeStore(str, str)
        self.treeview = Gtk.TreeView(self.treestore)
        self.image_cell = Gtk.CellRendererPixbuf()
        self.tvcol_image = Gtk.TreeViewColumn(None, self.image_cell, stock_id=1)
        self.treeview.append_column(self.tvcol_image)
        self.cell = Gtk.CellRendererText()
        self.tvcol = Gtk.TreeViewColumn(None, self.cell, text=0)
        self.treeview.append_column(self.tvcol)
        self.selection = self.treeview.get_selection()
        self.selection.connect('changed', self.row_selected)
        self.selection.set_select_function(lambda selection, model, path, current: os.path.isdir(self.get_path_for_path(model, path)))
        self.fill_tree()

        self.add_box = Gtk.Box()

        self.dir_entry = Gtk.Entry()
        self.dir_entry.connect('changed', self.entry_changed)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.BUTTON)
        self.add_folder_button = Gtk.Button()
        self.add_folder_button.set_image(image)
        self.add_folder_button.set_sensitive(False)
        self.add_folder_button.connect('clicked', self.add_folder)

        self.add(self.button)
        self.add(self.treeview)
        self.add_box.add(self.dir_entry)
        self.add_box.add(self.add_folder_button)
        self.add(self.add_box)

    def entry_changed(self, entry):
        self.update_add_button()

    def row_selected(self, selection):
        self.update_add_button()

    def update_add_button(self):
            self.add_folder_button.set_sensitive(self.is_addable())

    def get_path_for_path(self, model, path):
        folder = self.button.get_filename()
        if path is not None:
            elements = [model[path[0:end+1]][0] for end in range(len(path))]
            folder = os.path.join(folder, *elements)
        return folder

    def get_path_for_selection(self):
        model, iter = self.selection.get_selected()
        path = model.get_path(iter) if iter is not None else None
        return self.get_path_for_path(model, path)

    def is_addable(self):
        parent = self.get_path_for_selection()
        child = self.dir_entry.get_text()
        return (len(child) > 0 and
                os.path.isdir(parent) and
                not os.path.exists(os.path.join(parent, child)))

    def add_folder(self, button):
        path = self.get_path_for_selection()
        path = os.path.join(path, self.dir_entry.get_text())
        os.mkdir(path)
        model, iter = self.selection.get_selected()
        prior_path = model.get_path(iter)
        model.append(iter, (self.dir_entry.get_text(), Gtk.STOCK_DIRECTORY))
        self.treeview.set_model(model)
        self.dir_entry.set_text('')
        self.selection.select_path(prior_path)

    def do_file_set(self, button):
        self.fill_tree()
        self.treeview.set_model(self.treestore)

    def fill_tree(self):
        model, iter = self.selection.get_selected()
        prior_path = model.get_path(iter) if iter is not None else None
        folder = self.button.get_filename()
        self.treestore.clear()
        self.do_fill_tree(None, folder)
        if prior_path is not None:
            self.selection.select_path(prior_path)


    def do_fill_tree(self, parent, path):
        for file in sorted(os.listdir(path)):
            fullpath = os.path.join(path, file)
            if os.path.isdir(fullpath):
                child = self.treestore.append(parent, (file, Gtk.STOCK_DIRECTORY))
                self.do_fill_tree(child, os.path.join(path, file))
        for file in sorted(os.listdir(path)):
            fullpath = os.path.join(path, file)
            if not os.path.isdir(fullpath):
                child = self.treestore.append(parent, (file, Gtk.STOCK_FILE))

if __name__=='__main__':
    win = Gtk.Window()
    win.add(FileManager())
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

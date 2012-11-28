#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import os
import subprocess as sp
import gtk
import gio
from pprint import pprint

# TODO: Use logging.

pprint # Shut pyflakes.

class EjectsyApp:

    def __init__(self):
        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_visible(False)

        self.status_icon.set_from_stock(gtk.STOCK_HARDDISK)
        self.status_icon.connect('activate', self.on_left_click)
        self.status_icon.connect('popup-menu', self.on_right_click)
        self.status_icon.set_tooltip('Ejectsy')

        self.monitor = gio.VolumeMonitor()
        self.monitor.connect('volume-added', self.on_volume_added)
        self.monitor.connect('volume-removed', self.on_volume_removed)

        self.update_ui()

    def update_ui(self, show_icon=None):

        if show_icon is None:
            show_icon = bool(filter(lambda v: not self.is_internal(v),
                self.monitor.get_volumes()))

        self.status_icon.set_visible(show_icon)

    def on_volume_added(self, monitor, volume):
        print('New volume', volume)
        if not self.is_internal(volume):
            self.update_ui(True)

    def on_volume_removed(self, monitor, volume):
        print('Volume removed', volume)
        self.update_ui()

    def is_internal(self, volume):

        block_path = ('/sys/class/block/' +
                os.path.basename(volume.get_identifier('unix-device')))

        return not (os.path.islink(block_path) and
                '/usb' in os.path.realpath(block_path))

    def on_left_click(self, icon):
        event = gtk.get_current_event()

        volumes = self.monitor.get_volumes()
        pprint(volumes)

        popup = gtk.Menu()

        for volume in volumes:
            pprint(dict((i, volume.get_identifier(i))
                for i in volume.enumerate_identifiers()))

            if self.is_internal(volume):
                continue

            menu = gtk.MenuItem(volume.get_name() +
                    ' (' + volume.get_drive().get_name() + ')')
            submenu = gtk.Menu()
            menu.set_submenu(submenu)
            popup.append(menu)

            # XXX: Show something if `not volume.can_mount`.
            if volume.get_mount() is None:
                submenu.append(self.mk_menu_item('Mount', self.mount, volume))
                submenu.append(self.mk_menu_item('Mount and Open',
                    self.mount_and_open, volume))

            else:
                submenu.append(
                        self.mk_menu_item('Open', self.open_volume, volume))
                submenu.append(
                        self.mk_menu_item('Unmount', self.unmount, volume))

        if len(popup) == 0:
            dummy_item = gtk.MenuItem('No volumes detected')
            dummy_item.set_sensitive(False)
            popup.add(dummy_item)

        popup.show_all()
        popup.popup(None, None, gtk.status_icon_position_menu, event.button,
                event.time, icon)

    def mk_menu_item(self, label, activate_callback, *args):
        item = gtk.MenuItem(label)
        item.connect('activate', activate_callback, *args)
        return item

    def mount(self, menu_item, volume):
        print('Mounting', menu_item, volume)
        volume.mount(None, lambda volume, result: None)

    def mount_and_open(self, menu_item, volume):
        print('Mounting and opening', menu_item, volume)
        volume.mount(None,
                lambda volume, result: self.open_volume(menu_item, volume))

    def unmount(self, menu_item, volume):
        print('Unmounting', menu_item, volume)
        volume.get_mount().unmount(lambda mount, result: None)

    def open_volume(self, menu_item, volume):
        print('Opening volume', menu_item, volume)
        # TODO: xdg-open has informative return codes. Use them for error
        # reporting to the user.
        # FIXME: This process doesn't fork off if `nautilus` isn't already
        # running. In such cases, nautilus gets killed when ejectsy is killed.
        sp.Popen(['xdg-open', volume.get_mount().get_root().get_uri()])

    def on_right_click(self, icon, button, time):
        menu = gtk.Menu()

        about = gtk.MenuItem('About')
        quit = gtk.MenuItem('Quit')

        about.connect('activate', self.show_about_dialog)
        quit.connect('activate', gtk.main_quit)

        menu.append(about)
        menu.append(quit)

        menu.show_all()
        menu.popup(None, None, gtk.status_icon_position_menu, button, time,
                icon)

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name('Ejectsy')
        about_dialog.set_comments('A simple non-intrusive external-disk '
                'management application, that sits in the tray.')
        about_dialog.set_website('http://github.com/sharat87/ejectsy')
        about_dialog.set_version('0.1')
        about_dialog.set_authors(['Shrikant Sharat Kandula'])
        about_dialog.set_license('MIT License (http://mitl.sharats.me)')

        about_dialog.run()
        about_dialog.destroy()


def main():
    EjectsyApp()
    gtk.main()

if __name__ == '__main__':
    main()

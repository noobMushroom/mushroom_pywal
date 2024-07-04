#!/usr/bin/env python3
try:
    import gtk
except ImportError:
    print("[ERROR] gtk_reload: GTK reload requires PyGTK.")
    exit(1)


def gtk_reload():
    """Reload GTK2 themes."""
    events = gtk.gdk.Event(gtk.gdk.CLIENT_EVENT)
    data = gtk.gdk.atom_intern("_GTK_READ_RCFILES", False)
    events.data_format = 8
    events.send_event = True
    events.message_type = data
    events.send_clientmessage_toall()


gtk_reload()

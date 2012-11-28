# Ejectsy

An external/usb drive monitor that sits in the tray. For Linux. Written in
python. Inspired by [ejecter][https://launchpad.net/ejecter].

# Usage

This isn't rocket science, but still. Just clone this repo and start ejectsy,

    git clone https://github.com/sharat87/ejectsy.git
    python ejectsy/main.py

Just make sure you have the necessary dependencies (Only pygtk should be
enough, which should already be there if you're on ubuntu).

You may not see any icon in the tray, this is because the icon only appears *if*
there are any external disks connected. So, once you connect a USB drive, you
should see a hard disk like icon (unless your theme is weird). Click on this
icon to get a list of the devices connected and manage them.

## Screenshots

Take a look at the following screenshots to get an idea of what you can do.

![screenshot-unmounted][https://github.com/sharat87/ejectsy/raw/master/screenshots/menu-unmounted.png
"With an unmounted device"]

![screenshot-mounted][https://github.com/sharat87/ejectsy/raw/master/screenshots/menu-mounted.png
"With a mounted device"]

# Meta

## Feedback

Found a problem or otherwise have something to say? [Open an
issue][https://github.com/sharat87/ejectsy/issues] or [drop me a
line][mailto:shrikantsharat.k@gmail.com].

## Alternatives

- [Ejecter][https://launchpad.net/ejecter]
- [Media Applet][http://media-applet.googlecode.com]
- [Mountie][https://github.com/Toobkrow/mountie]

## License

[MIT License][http://mitl.sharats.me]

#!/usr/bin/env python3
from i3ipc import Connection
from subprocess import call

i3 = Connection()


def bindnotify(i3, event):
    # print(event.binding.__dict__)
    bind = event.binding

    mods_dict = [
        ['Mod4', 'Super'],
        ['shift', 'Shift'],
        ['ctrl', 'Control'],
        ['Mod1', 'Alt'],
    ]
    mods = '+'.join([
        mod[1]
        for mod in mods_dict
        if mod[0] in bind.mods
    ])
    if mods: 
        mods += '+'

    call('notify-send -t 1 -a i3wm'.split(' ') +
        [bind.command, '%s%s' % (mods, bind.symbol)])


def workspacenotify(i3, event):
    # print(event.change)
    if event.change in "focus":
        if event.old.num != -1:
            call('i3wswp'.split(' ')+[format(event.current.name)])
            call('polybar-msg hook pbws 1'.split(' '))


def windownotify(i3, event):
    # print(event.change)

    if event.container.fullscreen_mode == 0:
        call('polybar-msg cmd show'.split(' '))
    else:
        call('polybar-msg cmd hide'.split(' '))

    if event.change == "focus":
        if event.container.window_class == 'mpv':
            call('mpc -q seek -1'.split(' '))
            call('mpc -q pause'.split(' '))
            # call('polybar-msg hook mediatitle 2'.split(' '))

    if event.change == "focus":
        call('polybar-msg hook pbtitle 1'.split(' '))

    if event.change == "title":
        call('polybar-msg hook pbtitle 2'.split(' '))

    if event.change == "close":
        if event.container.window_class == 'mpv':
            call('mpc -q seek -1'.split(' '))
            # if event.container.focused == True:
            #     call('pbmedia mpvclose'.split(' '))

    if event.change == "close":
        if event.container.window_instance == "castterm":
            call('pbrectime stop'.split(' '))

    if event.change == "new":
        if event.container.window_instance == "castterm":
            call('pbrectime start'.split(' '))

        
# i3.on('binding', bindnotify)
i3.on('window', windownotify)
i3.on('workspace', workspacenotify)

# WORKSPACE = (1 << 0)
# OUTPUT = (1 << 1)
# MODE = (1 << 2)
# WINDOW = (1 << 3)
# BARCONFIG_UPDATE = (1 << 4)
# BINDING = (1 << 5)

i3.main()

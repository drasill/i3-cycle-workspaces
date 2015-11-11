i3-cycle-workspaces
===================

A python script to cycle some workspaces with the same key binding.

What ?
------

On i3 you can often press a key to go to a specific workspace.
For exemple with the default config, `mod+2` goes the workspace "2".

When this script runs (in background), if you press `mod+2` while *already*
being on the workspace 2, you'll go the next workspace.

Why ?
-----

This is actually useful for me, when I need, like, three workspaces dedicated to
some terms.

For exemple :

In the i3 config :
```
bindsym $mod+p workspace 20:Terms
```

With `cycle.py --ws 20:` running, you can press `$mod+p` to cycle to the
workspaces :
* 20:Terms
* 21:Terms
* 22:Terms
* 20:Terms
* *etc.*

How ?
-----

*i3-cycle-workspaces* will detect when a `bindsym` to go to a workspace is
pressed.

If already on the workspace and if it matches the configuration, it will cycle.

It's fast because it uses the i3 IPC `binding` event.

I suppose you need a recent version of i3wm for this to work.

Installation
------------

Ubuntu

```
sudo apt-get install x11-utils python-pip git
sudo pip install i3ipc
mkdir -p ~/.config/i3 && cd ~/.config/i3
git clone https://github.com/drasill/i3-cycle-workspaces
```

And add the script to your i3wm config (after you understand the command line
options) :

```
exec --no-startup-id ~/.config/i3/i3-cycle-workspaces/cycle.py --ws 2
```


Options
-------

*It's recommanded you manually launch the script with some options before adding
it to your i3 config.*

Use the `--ws` option to specify a workspace *regex*.

You can then use a `--cycle` option to specify a number of workspace cycle
(otherwise the default is `3`).

All workspaces matching this regex will react to the cycle.

Exemple :

```
cd ~/.config/i3/i3-cycle-workspaces
cycle.py --ws 5

# Or:
./cycle.py --ws 5 --cycle 2

# You can also use `--ws` many times like this :
./cycle.py --ws 5 --cycle 5 --ws 10 --cycle 3

# You can do this so that ALL workspaces will cycle :
./cycle.py --ws .
```


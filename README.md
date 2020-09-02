# steam-dmenu

Reads installed Steam games from one or multiple Steam libraries and offers a selection in dmenu compatible format.

## Requirements
- Steam (obviously)
- python 3
- xdg-open
- some dmenu compatible application (dmenu, rofi, bemenu, wofi...)

## Configuration
While dmenu is the default, any compatible alternative or additional parameters for dmenu can be used with the `--dmenu` (`-d`) flag.
The Steam library is assumed to be in `~/.local/share/Steam`, however the `--library` (`-l`) flag takes any number of alternative library locations.

### Example with rofi and 2 library locations
`steam_dmenu.py -d 'rofi -dmenu -i' -l '~/.local/share/Steam' '~/Games/Steam'`

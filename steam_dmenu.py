#!/usr/bin/env python

import sys
import glob
from os.path import expanduser
from subprocess import Popen, PIPE
from typing import Tuple
import vdf

def main() -> None:
    returncode, stdout = open_dmenu(get_games())

    if returncode == 1:
        sys.exit()
    else:
        launch_game(stdout.decode().split(':')[0])

def get_games() -> str:
    apps = glob.glob('{}/.local/share/Steam/steamapps/appmanifest_*.acf'.format(expanduser('~')))
    games = ""
    for file in apps:
        with open(file) as game:
            appstate = vdf.parse(game)['AppState']
            games += '{}: {}\n'.format(appstate['appid'], appstate['name'])

    return games

def open_dmenu(games: str) -> Tuple[int, bytes]:
    dmenu = Popen(
        [
            'dmenu',
        ],
        stdin=PIPE,
        stdout=PIPE
    )
    (stdout, _) = dmenu.communicate(input=games.encode('UTF-8'))
    return dmenu.returncode, stdout

def launch_game(appid: str):
    Popen(['steam', 'steam://run/{}'.format(appid)])

if __name__ == "__main__":
    main()

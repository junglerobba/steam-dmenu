#!/usr/bin/env python

import argparse
import sys
import glob
from os.path import expanduser
from subprocess import Popen, PIPE
from typing import List, Tuple
import vdf

def main() -> None:
    args = parse_arguments()
    returncode, stdout = open_dmenu(args.dmenu, get_games(args.library))
    appid = stdout.decode().split(':')[0]
    if returncode == 1 or not appid or not appid.isdigit():
        sys.exit()
    else:
        launch_game(appid)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Launch installed Steam games using dmenu')
    parser.add_argument(
        '--dmenu',
        '-d',
        dest='dmenu',
        default='dmenu -i',
        help='Custom dmenu command (default is \'dmenu -i\')'
    )
    parser.add_argument(
        '--libraries',
        '-l',
        dest='library',
        nargs='*',
        default=['~/.local/share/Steam'],
        help='Steam library location[s] (default is \'~/.local/share/Steam\')'
    )
    parsed_args = parser.parse_args()

    return parsed_args

def get_games(libraries: List[str]) -> str:
    games = ""
    for library in libraries:
        library = library.replace('~', expanduser('~'))
        apps = glob.glob('{}/steamapps/appmanifest_*.acf'.format(library))
        for file in apps:
            with open(file) as game:
                appstate = vdf.parse(game)['AppState']
                games += '{}: {}\n'.format(appstate['appid'], appstate['name'])

    return games

def open_dmenu(dmenu: str, games: str) -> Tuple[int, bytes]:
    dmenu = Popen(
        dmenu.split(),
        stdin=PIPE,
        stdout=PIPE
    )
    (stdout, _) = dmenu.communicate(input=games.encode('UTF-8'))
    return dmenu.returncode, stdout

def launch_game(appid: str):
    Popen(['steam', 'steam://run/{}'.format(appid)])

if __name__ == "__main__":
    main()

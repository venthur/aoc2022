from itertools import product
from collections import deque


def read_input(fn):
    with open(fn) as fh:
        line = fh.read().strip()

    return deque(line)


def load_tiles():
    tiles_str = """
        ####

        .#.
        ###
        .#.

        ..#
        ..#
        ###

        #
        #
        #
        #

        ##
        ##
    """
    tiles = []
    for ts in tiles_str.split('\n\n'):
        ts = ts.strip()
        tile = dict()
        for y, line in enumerate(ts.splitlines()):
            line = line.strip()
            for x, char in enumerate(line):
                tile[x, y] = char
        tiles.append(tile)

    return deque(tiles)


def pp(tunnel, tile, x, y):
    print(f'Tile at {x, y}')
    tunnel = tunnel.copy()

    xs, ys = zip(*tile)
    for yi in range(0, max(ys)+1):
        for xi in range(0, max(xs)+1):
            if tile.get((xi, yi), '.') == '#':
                tunnel[xi+x, yi+y] = '#'

    xs, ys = zip(*tunnel)
    for yi in range(min(ys)-1, 0+2):
        if yi == 1:
            print('-------')
        else:
            for xi in range(0, 7):
                print(tunnel.get((xi, yi), '.'), end='')
        print()
    print()


def task1(fn):
    pattern = read_input(fn)
    tiles = load_tiles()

    tunnel = dict()
    total_height = 0
    for rock in range(2022):
        # get next tile
        tile = tiles[0]
        tiles.rotate(-1)

        # position, 2 from the left and 3 units above highest
        xs, ys = zip(*tile)
        width = len(set(xs))
        height = len(set(ys))
        x = 2
        y = - total_height - height - 2

        #print('next', x, y, total_height)
        #pp(tunnel, tile, x, y)

        while True:
            # test if tile is settled

            # push left or right
            push = pattern[0]
            pattern.rotate(-1)
            xi = x-1 if push == '<' else x+1

            # collision detection
            bang = False
            if xi < 0 or xi+width-1 > 6:
                #print('bang - wall')
                bang = True
            else:
                for yt, xt, in product(range(height), range(width)):
                    if tile.get((xt, yt), '.') == tunnel.get((xi+xt, y+yt), '.') == '#':
                        bang = True
                        break

            if not bang:
                x = xi

            #print(push)
            #pp(tunnel, tile, x, y)

            # go down
            yi = y + 1

            # collision detection
            bang = False
            if yi + height - 1 > 0:
                bang = True
            else:
                for yt, xt, in product(range(height), range(width)):
                    if tile.get((xt, yt), '.') == tunnel.get((x+xt, yi+yt), '.') == '#':
                        bang = True
                        break

            #print('down')
            #pp(tunnel, tile, x, yi)

            if not bang:
                y = yi
            else:
                #print('settled')
                for yt, xt, in product(range(height), range(width)):
                    if tile.get((xt, yt), '.') == '#':
                        tunnel[x+xt, y+yt] = '#'
                total_height = abs(min(y for (x, y), v in tunnel.items() if v == '#')) + 1
                break

    return total_height


assert task1('test_input.txt') == 3068
print(task1('input.txt'))

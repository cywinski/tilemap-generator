from tilemap import TileMap, load
from tilemap_exceptions import (
    InvalidData,
    verify_dimensions,
    verify_grounds
)


def create_map_from_input(mode):
    """
    Function that visualizes or loads Tile Map based on User's povided input

    :param mode: Mode chosen by User in main function
    """

    if mode == '5':
        load_from_input()
    elif mode not in {'1', '2', '3', '4', '5'}:
        print(f"Wrong typed in number: '{mode}'")
    else:
        try:
            input_w = int(input('Enter width: '))
            input_h = int(input('Enter height: '))
        except ValueError:
            print(f"Wrong given dimensions")
        except TypeError:
            print(f"Wrong type of given dimensions")
        else:
            verify_dimensions(input_w, input_h)
            min_pts = ask_for_points('min_pts')
            max_pts = ask_for_points('max_pts')
            if mode == '1':
                tmap = create_map(input_w, input_h, [], {}, min_pts=min_pts, max_pts=max_pts)
            elif mode == '2':
                grounds = get_grounds()
                verify_grounds(input_w, input_h, grounds=grounds)
                tmap = create_map(input_w, input_h, grounds, {}, min_pts=min_pts, max_pts=max_pts)
            elif mode == '3':
                own_grounds = get_own_grounds(input_w, input_h)
                verify_grounds(input_w, input_h, own_grounds=own_grounds)
                tmap = create_map(input_w, input_h, [], own_grounds, min_pts=min_pts, max_pts=max_pts)
            elif mode == '4':
                grounds = get_grounds()
                own_grounds = get_own_grounds(input_w, input_h)
                verify_grounds(input_w, input_h, grounds=grounds, own_grounds=own_grounds)
                tmap = create_map(input_w, input_h, grounds, own_grounds, min_pts=min_pts, max_pts=max_pts)
            if_visualize(tmap)
            if_save(tmap)


def create_map(width, height, grounds, own_grounds, min_pts, max_pts):
    """
    Function that creates Tile Map based on User's input

    :returns: Tile Map object
    """

    if min_pts is None:
        if max_pts is None:
            tmap = TileMap(width, height, grounds, own_grounds, min_pts=min_pts, max_pts=max_pts)
        else:
            tmap = TileMap(width, height, grounds, own_grounds, min_pts=min_pts)
    elif (min_pts is None) and (max_pts is None):
        tmap = TileMap(width, height, grounds, own_grounds, max_pts=max_pts)
    else:
        tmap = TileMap(width, height, grounds, own_grounds)
    return tmap


def get_own_grounds(input_w, input_h):
    """
    Function that gets own_grounds from User's input

    :returns: Own User's grounds if provided, if not empty dictionary
    :rtype: dict
    """

    i = True
    input_own_grounds = dict()
    while i:
        input_name = input('Enter name of custom ground: ')
        input_rgb = input('Enter RGB tuple of custom ground: ')
        if not input_rgb:
            raise InvalidData(f"Wrong given RGB tuple")
        omit_sign("'", input_rgb)
        if ('(' and ')') not in input_rgb:
            raise InvalidData(f"Wrong given RGB tuple")
        input_own_grounds[input_name] = eval(input_rgb)
        verify_grounds(input_w, input_h, own_grounds=input_own_grounds)
        if_next = input('Do you want to enter another custom ground?([y]/n) ')
        if if_next == ('n'.lower() or 'no'.lower()):
            i = False
        if if_next != ('y'.lower() or 'yes'.lower()):
            i = False
    return input_own_grounds if input_own_grounds else {}


def get_grounds():
    """
    Function that gets grounds from User's input

    :returns: List of grounds chosen by User, if User did not chose
    any ground, empty list
    :rtype: list
    """

    input_grounds = input('Choose grounds: ')
    input_grounds = omit_sign("'", input_grounds)
    stripped = [elem.strip() for elem in input_grounds.split(',')]
    return stripped if stripped else []


def if_visualize(tmap):
    """
    Function that asks User if he wants to visualize Tile Map
    """

    i = True
    while i:
        input_vis = input('Do you want to visualize your tile map?([y]/n) ')
        if input_vis == ('y'.lower() or 'yes'.lower()):
            tmap.visualize()
            i = False
        if input_vis == ('n'.lower() or 'no'.lower()):
            i = False


def if_save(tmap):
    """
    Function that asks User if he wants to save Tile Map
    """
    j = True
    i = True
    while i:
        input_save = input('Do you want to save your tile map?([y]/n) ')
        if input_save == ('y'.lower() or 'yes'.lower()):
            while j:
                input_path = input('Enter name of a file: ')
                if input_path:
                    tmap.save(omit_sign("'", input_path))
                    i = False
                    j = False
        if input_save == ('n'.lower() or 'no'.lower()):
            i = False


def omit_sign(sign, sentence):
    """
    Function that omits provided sign in sentence
    """

    return sentence.translate({ord(sign): None})


def ask_for_points(point):
    """
    Function that ask User if he wants to provide limit of
    'min_pts' or 'max_pts'

    :returns: None if User do not want to provide limit, if he does,
    returns that limit
    """

    i = True
    while i:
        input_pts = input(f"Do you want to specify '{point}'?([y]/n) ")
        if input_pts == ('y'.lower() or 'yes'.lower()):
            try:
                input_val = int(input(f"Enter value of '{point}': "))
                i = False
            except ValueError:
                print(f"Wrong given value")
                i = False
            except UnboundLocalError:
                print(f"Wrong type of given value")
                i = False
            else:
                input_val = None if input_val == '' else input_val
                return input_val
        if input_pts == ('n'.lower() or 'no'.lower()):
            i = False
            return None


def load_from_input():
    """
    Function that loads and visualizes image from imput provided by User
    """

    i = True
    while i:
        input_file = input('Enter name of file: ')
        if input_file:
            load(omit_sign("'", input_file))
            i = False

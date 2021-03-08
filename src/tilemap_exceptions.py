class InvalidData(Exception):
    """
    Class of Exception that raises when User provides invalid data to Tile Map
    """

    pass


rgb_of_grounds = {
            'water': (51, 153, 255),
            'land': (125, 200, 100),
            'sand': (255, 255, 153),
            'forest': (0, 100, 0),
            'stone': (160, 160, 160),
            'ice': (204, 255, 255),
            'snow': (255, 255, 255),
    }


def verify_dimensions(width, height, grounds=None, own_grounds=None):
    """
    Function that verify dimensions given by User to Tile Map object
    """

    if not (width and height):
        raise InvalidData(f"Wrong dimensions")
    if type(width) != int or type(height) != int:
        raise InvalidData(f"Wrong type of dimensions")
    if (not grounds) and (not own_grounds):
        if (width < 4) or (height < 4):
            raise InvalidData(f"Dimentions are too small")
    if grounds and (not own_grounds):
        if (width < 2*len(grounds)) or (height < 2*len(grounds)):
            raise InvalidData(f"Dimentions are too small")
    if own_grounds and (not grounds):
        if (width < 2*len(own_grounds)) or (height < 2*len(own_grounds)):
            raise InvalidData(f"Dimentions are to small")
    if own_grounds and grounds:
        if (width < 2*len(grounds) + len(own_grounds)) or \
           (height < 2*len(grounds) + len(own_grounds)):
            raise InvalidData(f"Dimentions are too small")


def verify_pts(width, height, grounds=None, own_grounds=None, min_pts=None, max_pts=None):
    """
    Function that verify 'min_pts' and 'max_pts' given by User
    to Tile Map object
    """

    if min(width, height) % 2 == 0:
        l_lim = min(width, height)/2
        h_lim = max(width, height)/2
    else:
        l_lim = (min(width, height)-1)/2
        h_lim = (max(width, height)-1)/2
    if min_pts or min_pts in {0, 1}:
        if type(min_pts) != int:
            raise InvalidData(f"Wrong type of given points")
        if not max_pts:
            if min_pts > max((h_lim, (len(grounds) + len(own_grounds)))):
                raise InvalidData(f"Amount of minimal points to choose is too big")
        if min_pts < (len(grounds) + len(own_grounds)):
            raise InvalidData(f"Amount of points to choose needs to be greater than amount of chosen grounds")
    if max_pts or max_pts in {0, 1}:
        if type(max_pts) != int:
            raise InvalidData(f"Wrong type of given points")
        if not min_pts:
            if max_pts < max(l_lim, (len(grounds) + len(own_grounds))):
                raise InvalidData(f"Amount of points to choose is to small")
        if max_pts < (len(grounds) + len(own_grounds)):
            raise InvalidData(f"Amount of points to choose needs to be greater than amount of chosen grounds")
    if min_pts and max_pts and min_pts > max_pts:
        raise InvalidData(f"Wrong points")


def verify_grounds(width, height, grounds=None, own_grounds=None, min_pts=None, max_pts=None):
    """
    Function that verify grounds chosen or provided by User
    """

    if grounds:
        if len(grounds) > (width*height):
            raise InvalidData(f"Amount of grounds is too big")
        for ground in grounds:
            if ground not in rgb_of_grounds.keys():
                raise InvalidData(f"Ground '{ground}' is not available, try to type in your own ground")
    if own_grounds:
        if type(own_grounds) != dict:
            raise InvalidData(f"Grounds given by you should be dictionary")
        if len(own_grounds) > (width*height):
            raise InvalidData(f"Amount of custom grounds is too big")
        for rgb in own_grounds.items():
            if type(rgb[1]) != tuple:
                raise InvalidData(f"Wrong given ground : '{rgb[0]}'")
            if len(rgb[1]) != 3:
                raise InvalidData(f"Wrong given color of ground: '{rgb[0]}'")
            for digit in rgb[1]:
                if (digit < 0) or (digit > 255):
                    raise InvalidData(f"Wrong given color of ground : '{rgb[0]}'")
    if grounds and own_grounds:
        if (len(grounds) + len(own_grounds)) > (width*height):
            raise InvalidData(f"Amoint of grounds is too big")

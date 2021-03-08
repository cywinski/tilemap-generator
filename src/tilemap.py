from tilemap_exceptions import (
    verify_dimensions,
    verify_pts,
    verify_grounds,
    )
from tilemap_help_functions import (
    convert_to_np,
    find_every_zero,
    stack_array,
    choose_random_coordinate,
    add_to_set,
    )
from PIL import Image, ImageDraw
import numpy as np
from random import randint, choice
from math import sqrt


class TileMap:
    """
    A Class used to construct a Tile Map

    Allows to construct a simple Tile Map with various types
    of colors of the grounds. Size of Map is declared by user.
    Class also allows to visualize, save and load a Tile Map.
    """

    rgb_of_grounds = {
            'water': (51, 153, 255),
            'land': (125, 200, 100),
            'sand': (255, 255, 153),
            'forest': (0, 100, 0),
            'stone': (160, 160, 160),
            'ice': (160, 230, 255),
            'snow': (255, 255, 255),
    }

    def __init__(self, width, height, grounds=None, own_grounds=None, min_pts=None, max_pts=None):
        """
        Initiates an TileMap object

        :param width: Width of a Map
        :type width: int
        :param height: Height of a Map
        :type height: int
        :param grounds: List of basic grounds given in Class
        (default grounds are 'water' and 'land')
        :type grounds: list
        :param own_grounds: Dictionary of grounds that can be provided by User
        :type own_grounds: dict
        :param min_pts: Determine minimal amount central points of grounds
        :type min_pts: int
        :param max_pts: Determine maximal amount central points of grounds
        :type max_pts: int

        :param chosen_pts: Chosen central points with its grounds
        :type chosen_pts: dict
        :param zeros_array: NumPy zeros array with same dimensions as Tile Map
        :type zeros_array: numpy.ndarray
        :param list_central_pts: List with randomly chosen
        central points' grounds
        :type list_central_pts: list
        :param every_zero: Two NumPy arrays with coordinates
        of every zero in list
        with central points' grounds, first contains X-coordinates,
        second contains Y-coordinates
        :type every_zero: numpy.ndarray
        :param cords_of_zeros: NumPy two dimensional array with coordinates of
        every zeroin list with central points' grounds
        :type cords_of_zeros: numpy.ndarray
        :param rgb_array: NumPy array with RGB tuples with
        colors of points' grounds
        :type rgb_array: numpy.ndarray
        :param image: Image made from rgb_array of a visualized pixels
        :type image: PIL.Image.Image
        """

        verify_dimensions(width, height, grounds, own_grounds)
        self.width = width
        self.height = height
        verify_grounds(width, height, grounds, own_grounds, min_pts, max_pts)
        self.grounds = ['water', 'land'] if not grounds else grounds
        self.own_grounds = dict() if not own_grounds else own_grounds
        verify_pts(width, height, grounds, own_grounds, min_pts, max_pts)
        self.min_pts = None if not min_pts else min_pts
        self.max_pts = None if not max_pts else max_pts
        self.chosen_pts = dict()
        self.zeros_array = np.zeros((self.height, self.width), dtype=int)
        self.list_central_pts = self.central_pts_to_array(
            self.zeros_array.tolist(),
            TileMap.amount_central_pts(self.width, self.height, self.grounds, self.own_grounds, min_pts=min_pts, max_pts=max_pts))
        self.copy = self.list_central_pts[:][:]
        self.every_zero = find_every_zero(convert_to_np(self.copy))
        self.cords_of_zeros = stack_array(self.every_zero[0], self.every_zero[1])
        self.rgb_array = convert_to_np(self.measure_distances(self.list_central_pts), dtype=np.uint8)
        self.image = Image.fromarray(self.rgb_array)

    def colors_to_use(self):
        """
        Method that checks colors of grounds used to construct Tile Map

        :returns: List of RGB tuples of grounds' colors used in Tile Map
        :rtype: list
        """

        colors = []
        if self.grounds:
            for item in self.grounds:
                colors.append(TileMap.rgb_of_grounds[item])
        if self.own_grounds:
            for item in self.own_grounds.values():
                colors.append(item)
        return colors if colors else [TileMap.rgb_of_grounds['water'], TileMap.rgb_of_grounds['land']]

    def every_color_was_used(self):
        """
        Method that checks if every color of grounds has been already used
        so that every color chosen by User will appear in Map at least one time

        :returns: True if every color has been used at least one time,
        otherwise False
        :rtype: bool
        """

        if set(self.chosen_pts.values()) == set(self.colors_to_use()):
            return True
        else:
            return False

    def which_color_not_used(self):
        """
        Method that checks which color of grounds has not been used so far

        :returns: List of not used colors
        :rtype: list
        """

        not_used_colors = []
        for color in self.colors_to_use():
            if color not in self.chosen_pts.values():
                not_used_colors.append(color)
        return not_used_colors

    def central_pts_to_array(self, zeros_array, amount_central_pts):
        """
        Method that applies particular amount of central points to zeros array

        :param zeros_array: NumPy array full of zeros with dimensions same as
        dimensions of Map
        :type zeros_array: numpy.ndarray
        :param amount_central_pts: Amount of central points to choose
        :type amount_central_pts: int
        :returns: Modified zeros list with RGB tuples of central points applied
        :rtype: list
        """

        colors = self.colors_to_use()
        used_colors = set()
        while amount_central_pts > 0:
            # Chooses a random point in list to be central point
            # of a particular ground
            central_x, central_y = choose_random_coordinate(self.height, self.width)
            # Checks if point has not been already chosen to be a ground
            if zeros_array[central_x][central_y] not in colors:
                if ((self.every_color_was_used()) or (amount_central_pts > (len(self.grounds) - len(used_colors)))):
                    add_to_set(used_colors, choice(colors))
                    self.apply_to_list(central_x, central_y, zeros_array, choice(colors))
                # Guarantees that every ground will be chosen at least one time
                elif (not self.every_color_was_used()) and (amount_central_pts == (len(self.grounds) - len(used_colors))):
                    add_to_set(used_colors, self.which_color_not_used()[0])
                    self.apply_to_list(central_x, central_y, zeros_array, self.which_color_not_used()[0])
                amount_central_pts -= 1
        return zeros_array

    def apply_to_list(self, x, y, ls, ground):
        """
        Method that changes value of element in list and adds
        central point with its ground as an item in dictionary

        :param x: X-coordinate of element in a list
        :type x: int
        :param y: Y-coordinate of element in a list
        :type y: int
        :param ls: List of elements to edit
        :type ls: list
        :param ground: Type of ground of a particular element in list
        :type ground: tuple
        """

        ls[x][y] = ground
        self.chosen_pts[x, y] = ground

    @staticmethod
    def amount_central_pts(width, height, grounds, own_grounds, min_pts=None, max_pts=None):
        """
        Staticmethod that randomly chooses amount of central points
        in particular Tile Map. If User do not determine both
        'min_pts' and 'max_pts', amount will be chosen
        with a use of variables 'l_lim' and 'h_lim' to limit that amount.
        It will eliminate cases where Map would look unrealistic
        """

        if min(width, height) % 2 == 0:
            l_lim = min(width, height)/2
            h_lim = max(width, height)/2
        else:
            l_lim = (min(width, height)-1)/2
            h_lim = (max(width, height)-1)/2
        if min_pts and max_pts:
            return randint(min_pts, max_pts)
        elif min_pts and not max_pts:
            return randint(min_pts, max((h_lim, (len(grounds) + len(own_grounds)))))
        elif max_pts and not min_pts:
            return randint(max(l_lim, (len(grounds) + len(own_grounds))), max_pts)
        else:
            return randint(l_lim, h_lim)

    def measure_distances(self, ls_central_pts):
        """
        Method that measures distances for every zero in list with
        central points, from zero to every central point and
        chooses minimal distance

        :param ls_central_pts: List with central points and zeros
        :type ls_central_pts: list
        :returns: List with only RGB tuples
        :rtype: list
        """

        for zero in range(len(self.every_zero[0])):
            # Makes dictionary of distances from particular zero
            # to every central point, and grounds corresponding to them
            zero_distances = dict()
            for point in self.chosen_pts.keys():
                # Measures distances between particular zero in list
                # and every central point
                dist = sqrt(((self.cords_of_zeros[0, zero]-point[0])**2) + ((self.cords_of_zeros[1, zero]-point[1])**2))
                zero_distances[point] = dist
            minimal_dist = min(zero_distances.values())
            rgb_list = self.apply_ground(zero_distances, minimal_dist, ls_central_pts, zero)
        return rgb_list

    def apply_ground(self, distances, min_dist, ls_central_pts, zero):
        """
        Method that changes elements in list with central points
        from zero to RGB tuples of grounds

        :param distances: Dictionary of distances from particular zero
        to every central point
        :type distances: dict
        :param min_dist: Minimal distance to central point(s)
        :type min_dist: float
        :param ls_central_pts: List with central points and zeros
        :type ls_central_pts: list
        :param zero: Particular zero from where distances are measured
        :type zero: int
        :returns: List with RGB tuple in place of particular zero
        :rtype: list
        """

        # List of element(s) with smallest distance(s) to zero
        cords = [elem for elem in TileMap.get_keys(distances, min_dist)]
        if len(cords) > 1:
            # Chooses random ground from grounds of same distances to that zero
            chosen_ground = choice(cords)
            ls_central_pts[self.cords_of_zeros[0, zero]][self.cords_of_zeros[1, zero]] = self.chosen_pts[chosen_ground]
        else:
            ls_central_pts[self.cords_of_zeros[0, zero]][self.cords_of_zeros[1, zero]] = self.chosen_pts[cords[0]]
        return ls_central_pts

    @staticmethod
    def get_keys(dictionary, val):
        """
        Staticmethod that gets key(s) of items with given values in dictionary

        :param dictionary: Dictionary to search in
        :type dictionary: dict
        :param val: Value of searched items
        :type val: tuple
        """

        keys = []
        for key, value in dictionary.items():
            if val == value:
                keys.append(key)
        return keys

    def expand_image(self):
        """
        Method that expands image object 16 times to make every pixel
        bigger and better visible

        :returns: Expanded image object
        :rtype: PIL.Image.Image
        """

        im_w, im_h = self.width, self.height
        expanded_image = Image.new("RGB", (im_w * 16, im_h * 16))
        for p_col in range(im_w):
            for p_row in range(im_h):
                color = self.image.getpixel((p_col, p_row))
                for x in range(16):
                    for y in range(16):
                        expanded_image.putpixel((p_col * 16 + x, p_row * 16 + y), color)
        return expanded_image

    def img_with_grid(self):
        """
        Method that draw grid on expanded image so that
        every pixel is highlighted

        :returns: Image object with a black grid
        :rtype: PIL.Image.Image
        """

        image = self.expand_image()
        draw = ImageDraw.Draw(image)
        x_start, x_end = 0, image.width
        y_start, y_end = 0, image.height
        width_step_size = int(image.width / self.width)
        height_step_size = int(image.height / self.height)

        for x in range(0, image.width, width_step_size):
            line = ((x, y_start), (x, y_end))
            draw.line(line, fill=(0, 0, 0))
        for y in range(0, image.height,  height_step_size):
            line = ((x_start, y), (x_end, y))
            draw.line(line, fill=(0, 0, 0))
        return image

    def visualize(self):
        """
        Method that visualizes constructed Tile Map
        """

        self.img_with_grid().show()

    def save(self, path):
        """
        Method that saves constructed Tile Map in provided file
        """
        try:
            self.img_with_grid().save(path)
        except ValueError:
            print(f"Unknown file extension")


def load(path):
    """
    Method that loads and visualizes image from provided file
    """
    try:
        im = Image.open(path)
    except FileNotFoundError:
        print(f"File '{path}' does not exists")
    except OSError:
        print(f"Unable to load content from file: {path}")
    else:
        im.show()

from run_functions import (
    create_map_from_input,
)


def main():
    print('    WELCOME IN THE TILE MAP GENERATOR!')
    print(f'''
    {'*'*69}
    SHORT INSTRUCION:
    In Tile Map Generator you can create your own Tile Map with
    desired size and types of grounds.
    {'-'*32}
    TYPES OF GROUNDS TO CHOOSE FROM:
        - 'water',
        - 'land',
        - 'sand',
        - 'forest',
        - 'stone',
        - 'ice',
        - 'snow'
    {'-'*32}
    ---> Type '1' to create new map with basic grounds
    ---> Type '2' to create new map with chosen grounds
    ---> Type '3' to create new map with Your own grounds
    ---> Type '4' to create new map with both chosen and Your own grounds
    ---> Type '5' to load and visualize an existing map from file
    {'*'*69}
    After creating a new Map, you will be asked if you want to save it.
    ''')
    action = input('>>>Type number in: ')
    action = action.translate({ord("'"): None})
    create_map_from_input(action)


if __name__ == "__main__":
    main()

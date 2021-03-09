# TileMap Generator

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

Project for PIPR (Computer Science and Programming Fundamentals) course at Warsaw University of Technology. This is my first ever programming project. Its purpose is to generate tile-maps with desired number of colors and size.
Documentation of project is in `doc.pdf` file.


![Sample Image](https://github.com/bartooo/tilemap-generator/blob/main/images/sample-map.png)
## Getting Started <a name = "getting_started"></a>

- Clone the repository.
- Install Python3.
- Follow instructions in next paragraph to setup venv and install required packages.
- Project should be ready to run.

### Installing
#### For Windows
1. Open cmd.
2. Make new virtual environment. 
```
python -m venv <name-of-venv>  
```
3. Activate virtual environment.
```
<name-of-venv>\Scripts\activate.bat
```
4. Install all packages listed in `requirements.txt`
```
pip install -r requirements.txt
```

## Usage <a name = "usage"></a>

- Run `run.py` file.
- Select mode:
    1. Creates new tile-map with only two types of lands: land and water.
    2. Creates new tile-map with grounds provided in program:
        - water
        - land
        - sand
        - forest
        - stone
        - ice
        - snow
    3. Creates new tile-map with types of grounds provided by User which will be prompted for name and RGB tuple for every provided land.
    4. Creates new tile-map where User can select grounds from provided grounds in program but also can provide his own ground. It is basically mix of mode 2 and 3.
    5. Loads and visualizes existing map from `.png` file.
- Enter width of tile-map.
- Enter height of tile-map.
- Choose to specify number of 'min_pts' and 'max_pts' which are central points of every land in tile-map. Many central points results in many diffrent islands in tile-map, few central points results in few diffrent islands in tile-map. By providing 'min_pts' and/or 'max_pts' you provide limits on number of central points.
- Choose to visualize tile-map.
- Choose to save tile-map.

### Size of tile-map
Both width and height should be an integer and has to be at least two times greater than number of provided grounds.

### Limits of central points
#### Lower limit of central points: `'min_pts'`
- Should be an integer.
- Cannot be greater than (if higher limit not provided):
```python
max(h_lim, (len(grounds) + len(own_grounds)))
```
where:
```python
h_lim = max(width, height)/2 if max(width, height) % 2 == 0 else (max(width, height)-1)/2
```
- Cannot be greater than higher limit.
- Cannot be less than:
```python
len(grounds) + len(own_grounds)
```
#### Higher limit of central points: `'max_pts'`
- Should be an integer.
- Cannot be less than (if lower limit not provided):
```python
max(l_lim, (len(grounds) + len(own_grounds)))
```
where:
```python
l_lim = min(width, height)/2 if min(width, height) % 2 == 0 else (min(width, height)-1)/2
```
- Cannot be less than:
```python
len(grounds) + len(own_grounds)
```
- Cannot be less than lower limit.

### Types of grounds
#### Chosing from grounds provided in program
User can choose grounds from:
- water
- land
- sand
- forest
- stone
- ice
- snow

When program prompts for chosen grounds, they should be entered in form:
```
Choose grounds: water, sand, forest, snow
```
#### Entering grounds with custom colors
When program prompts for name of custom ground, it should be a string, different from other grounds provided:
```
Enter name of custom ground: <name-of-custom-color>
```
When program prompts for RGB tuple of custom ground, it should be a tuple with three integers, every integer should be in range [0, 255]:
```
Enter RGB tuple of custom ground: (0, 244, 200)
```

### Saving tile-map
When program prompts for name of file, it should be a string with `.png` or `.jpg` extension:
```
Enter name of a file: <name-of-file>.png / <name-of-file>.jpg
```

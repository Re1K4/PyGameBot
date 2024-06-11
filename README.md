# Name
PyGameBot

## Overview
This is a generic game bot program template using PyAutoGui and OpenCV.

Most games can be automated.

## Requirement
pip install pyautogui

pip install opencv-python

pip install pywin32

pip install keyboard


## Usage
This is a template and will not work as is.

It is necessary to describe the main loop processing according to the operation you wish to automate.

The variable app_name must be set to the title of the game window.

This program will be terminated by pressing the ESC key. (check_esc_key function)

## Features
### Event Class

    Object with coordinates and color values on the screen

#### Constructor:

    Obj = ev([int] x, [int] y, [tuple]([int] R,[int] G,[int] B))
 
     Argument:
     
       x:x-coordinate
       
       y:y-coordinate
       
       R,G,B : Colorvalue[0-255])
  
#### Method:

Obj.checkColor(self) return bool
>Compares the color values of the pixels corresponding to the object's xy-coordinates on the current screen and returns a match (true) or mismatch (false).

### Time Class

    Objects that measure time

#### Constructor:

    Obj = tm()
 
#### Method:

Obj.set(self) return None
>Get the current time and enable the timer use flag.

Obj.distance(self) return float
>Calculate the time difference from the last time set() was called.

Obj.reset(self) return None
>Disable the timer use flag. The next time set() is called, the time is overwritten and can be reused.    

## Author
[![Twitter: ReekerZrZr](https://img.shields.io/twitter/follow/ReekerZrZr?style=social)](https://x.com/ReekerZrZr)

## Licence

[MIT](https://opensource.org/licenses/mit-license.php)

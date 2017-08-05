Tested on Python 3.4 and Windows 10

Packages Needed:
Box2d         (Tested on 2.3.1)
Numpy         (Tested on 1.12.1)
Pygame 	      (Tested on 1.9.3)

Optional Packages
Opencv-python (Tested on 3.2.0.7)



--Installation Guide--
1. Follow the first section of this link (until "The Testbed Examples")
https://github.com/pybox2d/pybox2d/blob/master/INSTALL.md
Box2D-2.3.1 is installed when pybox2d is installed

2. pip install numpy

3. pip install pygame==1.9.3



--Notes--
Currently, you just need to run main.py to start the program. All settings should be changed in the source files.

The graphics packages originally had issues with where you ran main.py from. This has been fixed for pygame, but if you plan on using opencv or another graphics package you'll either have to run it from its parent directory or fix the issues in the code.



---Package Files---
The following files are from the graphics/physics packages, and will probably not need to be edited:
    -backends/
    -data/
    -pgu/
    -framework.py
    -physicsSettings.py
All others were written for this research project (or are being reused).
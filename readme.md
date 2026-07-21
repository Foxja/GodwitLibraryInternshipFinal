# GODWIT BIRD INTERACTIVE SCREEN LIBRARY INTERNSHIP

<h3 align="center"> <strong> An interactive screen, written in python, rendered using pygame, and using a Microsoft Kinect </strong> </p>

## About

Hey! This project is an interactive screen that uses a Microsoft Kinect to allow participants to learn information about animals!

Contains:
* 
* 
* Customizable, flexible, and versatile. 


## How to run

1. To begin, please download all files in this Github project, minus this readme file. I have left the Virtual Enviroment (.venv) contents included because the plugins installed there are required to make the program run. INSTALLING THE PLUGINS USING PIP MANUALLY WILL NOT WORK. Pykinect2's pip installation has errors in it, you will need to download it directly from the Pykinect2 Github page. Additionally, the default version of comtypes Pykinect2 will install is incorrect. Version comtypes 1.1.7 is the version I have and it works for me.
2. Because of version requirements from Pygame and PyKinect2, this program requires a specific version of python: 3.6.8. [Install it here](https://www.python.org/downloads/release/python-368/). For me, this would be a Windows installation, but install it on whatever version you would need for your system.
3. I believe the xbox kinect SDK is required. [Install it here](https://www.microsoft.com/en-us/download/details.aspx?id=44561)
3. Open the folder with all files in VSCode. My understanding is that it must be set up in it as VSC will automatically recognize the virtual environment. Alternatively, you could configure your own venv.
4. Run the program.
5. To close out of the program, press the q key

## How to modify
The following is a brief guide for how to modify my code without breaking the project.
### How to add more rows/columns
The code is designed to be easily customized, so that adding more rows/columns is easy. To change the code, open pygameFinalMenu.py and change N_ROWS and N_COLS on lines 21 and 22. Additionally, you will need to add more images, sounds, and text. ALL OF THESE ARE REQUIRED TO ADD. The program will not work without them. If you can't find a sound for the animal, you will have to add a sound file with no contents.
### How to change out entries
Simply replace the images, sounds, and text. Please name all of the files something similar. The piece of code that grabs images, sounds, and text grabs the entries alphabetically, so as long as the files for each group are in the same order, it will work correctly. 
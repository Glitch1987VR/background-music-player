# background-music-player

This is one of my first Python projects.
Use it as you want.

# features 
0. only work on windows (I think)
1. Plays music when the system is silent
2. Wait-times for silence can be adjusted without going into the script
3. Folder browsing to select the folder containing you .mp3s (can work with .wav but probably not all of them)
4. The system can be easily paused and resumed without closing the script
5. Volume can also be adjusted
6. Folderpath, Volume and Wait-times will be saved in a config (quite reliable)
       The config should be created in the folder the .pyw is contained in, so put the script (.pyw) in an empty folder
7. A next file button, so you can skip the current one (not reliable)
8. A visible log system (Note: the logs are not helpful, I know from experience)
9. A window title which changes depending on the file playing 😱, crazy I know

![alt text](background-music-player-graphicial-v1.1.png)

To tweak things outside the gui boundaries, check the contents of .pyw
I have left some comments with instructions/possibilities there

# usage/installation
1. download the .pyw in the root folder (for ease of use, put it in an empty folder) (older versions can be found in old_files)
2. download .requirement.txt (you can put it in the same folder as the .pyw)
3. make sure you have [python](https://www.python.org) and [pip](https://pypi.org/project/pip/) on your system
       - pip usually comes preinstalled with python
4. open a command line (cmd, powershell, etc) and run:
       ``pip install -r "path\to\.requirements.txt"``
   this will install all the needed libraries for the script (.pyw) (I hope)
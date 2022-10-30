import appuifw
import zipfile
import shutil
import sysinfo
import os
from os import path

# The menu will have graphical glitches if using the default "large" screen size
appuifw.app.screen = 'normal'

# Search for a file extension recursively, from Forum Nokia wiki
# https://web.archive.org/web/20080906144605/http://wiki.forum.nokia.com/index.php/How_to_search_a_file_extension
def findfile(folder, file_extension):
    p=[]
    stack = [(folder, os.listdir(folder))]
    while stack:
        folder, names = stack[-1]
        while names:
            name = names.pop()
            pth = path.join(folder, name)
            if path.isfile(pth):
                if name.lower().endswith(file_extension):
                    p.append(pth)
            elif path.isdir(pth):
                stack.append((pth, os.listdir(pth)))
                break
        else:
            stack.pop()
    return p

while True:
    # File picker UI.
    cd = []  # Current directory stack, for example ["E:", "Games", "J2ME"]
    name = None
    while True:
        ls = []  # Directory listing
        if len(cd):
            try:
                if cd[0] == "m":
                    # Mail (messaging/bluetooth received files) are stored in a private folder, the
                    # directory structure is a mess so I just brute forced it by using a recursive
                    # search function.
                    # The full paths are saved in "msgpaths" and the directory listing only shows
                    # the filenames. When selecting a file name, the full path is looked up from the
                    # "msgpaths" list.
                    msgpaths = sorted(findfile("C:/Private/1000484b/Mail2", ".jar"))
                    for i in msgpaths:
                        ls.append(unicode(path.basename(i)))
                else:
                    for i in sorted(os.listdir('/'.join(cd))):
                        if path.isdir('/'.join(cd) + '/' + i) or i.lower().endswith('.jar'):
                            ls.append(unicode(i))
            except:
                appuifw.note(u"Error reading directory", "error")
                cd.pop()
                continue
        else:
            ls.append(u"C:")
            ls.append(u"D:")
            ls.append(u"E:")
            ls.append(u"Messaging")
            ls.append(u"About")

        # Create a selection list from the dir structure, if the user selects Cancel (right softkey)
        # then go back a directory or quit the app.
        choice = appuifw.selection_list(choices=ls)
        if choice == None:
            if len(cd):
                cd.pop()
                continue
            else:
                break

        if len(cd):
            if choice == 0:
                cd.pop()
            else:
                if cd[0] == "m":
                    name = msgpaths[choice - 1]
                    break
                else:
                    cd.append(str(ls[choice]))
                    if path.isfile('/'.join(cd)):
                        name = '/'.join(cd)
                        break
        else:
            if choice == 0:
                cd.append("C:")
            elif choice == 1:
                cd.append("D:")
            elif choice == 2:
                cd.append("E:")
            elif choice == 3:
                cd.append("m")
            else:
                appuifw.note(u"JavaResizer: scale old J2ME games to run on your S60 device!\ngithub.com/gtrxAC")
            
    if name == None:
        break

    # Ask user for the app's original size and the wanted scale size
    origw = appuifw.query(u"App's intended screen width? For example 176.","number")
    if origw == None:
        break
    origh = appuifw.query(u"App's intended screen height? For example 208.","number")
    if origh == None:
        break
    sctype = appuifw.selection_list(choices=[u"Keep aspect ratio", u"Stretch to fill", u"Integer scale 2x", u"Center without scaling", u"Custom"])
    if sctype == None:
        break

    scrres = sysinfo.display_pixels()
    # Keep aspect ratio
    if sctype == 0:
        scale = min(float(scrres[0])/origw, float(scrres[1])/origh)
        scalew = int(origw*scale)
        scaleh = int(origh*scale)

    # Stretch to fill
    elif sctype == 1:
        scalew = scrres[0]
        scaleh = scrres[1]

    # Integer scale 2x
    elif sctype == 2:
        scalew = 2*origw
        scaleh = 2*origh

    # Center without scaling
    elif sctype == 3:
        scalew = origw
        scaleh = origh
        
    else:
        scalew = appuifw.query(u"Width to scale to? For example 240.","number")
        if scalew == None:
            break
        scaleh = appuifw.query(u"Height to scale to? For example 320.","number")
        if scaleh == None:
            break
    
    namelist = []

    # Extract the zip to a temp directory (D: ramdisk)
    # While reading, we also save a list of all file names that we pack into the new zip.
    try:
        os.mkdir("D:/JavaResizer")
    except:
        # Assume the directory already exists
        pass
    z = zipfile.ZipFile(name, "r")
    namelist = z.namelist()
    for i in namelist:
        # In the namelist, '/' as the final char means that file is a directory
        if i[-1] == '/':
            os.mkdir("D:/JavaResizer/" + i)
        else:
            # But sometimes the directories are not listed as entries in the zip
            # So we need to check them and create the dirs manually if needed
            try:
                extracted = open("D:/JavaResizer/" + i, "wb")
            except:
                os.makedirs(path.dirname("D:/JavaResizer/" + i))
                extracted = open("D:/JavaResizer/" + i, "wb")
            
            extracted.write(z.read(i))
            extracted.close()
    z.close()

    # Modify the manifest to add the scaling parameters
    # New lines are added to the beginning so there won't be any blank lines
    mf = open("D:/JavaResizer/META-INF/MANIFEST.MF", "r")
    mfdata = mf.read()
    mf.close()
    mf = open("D:/JavaResizer/META-INF/MANIFEST.MF", "w")
    mf.write("Nokia-MIDlet-Original-Display-Size: " + str(origw) + ", " + str(origh) + "\n")
    mf.write("Nokia-MIDlet-Target-Display-Size: " + str(scalew) + ", " + str(scaleh) + "\n")
    mf.write(mfdata)
    mf.close()

    # Create a new zip containing the modified manifest
    # Note: this zip is uncompressed, shouldn't matter in most cases
    z = zipfile.ZipFile("D:/resized.jar", "w")
    os.chdir("D:/JavaResizer")
    for i in namelist:
        if i[-1] != '/':
            z.write(i)
    z.close()

    # Delete temp files
    try:
        shutil.rmtree("D:/JavaResizer")
    except:
        pass

    # Request user to install the output jar
    ch = appuifw.Content_handler()
    ch.open("D:\\resized.jar")

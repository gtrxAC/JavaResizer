# JavaResizer
A [Python](https://web.archive.org/web/20090209230321/http://wiki.forum.nokia.com/index.php/Category:Python) app for Symbian S60v3 that adds [scaling parameters](https://github.com/Nokia64/J2ME-phone-quirks/blob/main/vendor-specific-MIDlet-attributes.md#series-60) to J2ME apps.

* File picker with access to all drives and Bluetooth received files
* 4 preset scaling options and custom option
* Doesn't modify the original JAR file, creates a temporary copy

![Screenshots of the drive selection, C drive contents, and scaling options](img/screenshot.png)

The scaling doesn't use any smoothing filter, so for best results use integer scaling (128x128 or 128x160 apps scaled to a 240x320 screen, or 176x208 apps to a 352x416 screen).

# Installation
Download Python Runtime and JavaResizer SIS files from [GitHub](https://github.com/gtrxAC/JavaResizer/releases), [MEGA](https://mega.nz/folder/W5kmiTgR#adn6KNHKtCjlaWaMYNOBKQ) or [Google Drive](https://drive.google.com/drive/folders/1tCJ91m3OA5OndPLx4Pih4iNN1xnPKkHh?usp=sharing) and install them.

# Support
Currently S60v3 (including Feature Packs 1 and 2) is supported. S60v5 and anything newer should work too, but are untested.

# Building
So far I've only been able to build on Windows.
1. Install [Python 2.2](https://www.python.org/downloads/release/python-222/). Other versions such as 2.7 won't work because they are not bytecode compatible. Python doesn't provide Linux binaries so it would have to be manually compiled, I had issues with that.
2. Download the build dependencies from [MEGA](https://mega.nz/folder/W5kmiTgR#adn6KNHKtCjlaWaMYNOBKQ) or [Google Drive](https://drive.google.com/drive/folders/1tCJ91m3OA5OndPLx4Pih4iNN1xnPKkHh?usp=sharing) and move them to the same folder where this README file is.
3. On Windows, run `build.bat`. On Linux, run `build.sh` (untested).

# Thanks
I would like to thank a few people for helping with this project:
* RostiTheGamer and geodec29 for testing the app on their devices
* The [Symbian World](https://t.me/symbian_world) Telegram group for assisting with development
from os import path, sep
from sys import argv
from shutil import make_archive, move
from datetime import datetime
from plyer import notification

now = datetime.now()
fileType = 'zip'

# Helper Function to create as zip, and move it
#
#   source      - source file/directory to be zipped
#   destination - final desination of the zipped file
#   name        - name of new file (+ current date and time)
def makeArhiveHelper(source, destination, name):
    # File name is passed + current time.zip
    name = name + " " + str(now)

    # Replace the colons and periods because file naming issues
    name = name.replace(":", "-")
    name = name.replace(".", "-")

    # Clean the arhive names   
    archive_from = path.dirname(source)
    archive_to = path.basename(source.strip(sep))
    
    # zip up with the specs above
    make_archive(name, fileType, archive_from, archive_to)

    # make_archive doesn't like different letter drives for source and destination
    move('%s.%s'%(name,fileType), destination)

if len(argv) < 2 or len(argv) < 3:
    print(r'''
    Usage:
        Arg 1: Source Path
        Arg 2: Desination Path
        Arg 3: Name (+ current date)
    ex: python3 auto.py source destination name
    ex: python3 auto.py C:\Users\Chad \\192.168.X.X\SharedDrive Backups
    ex: python3 auto.py /home/user/Documents /mnt/Backup Backups''')
else:
    # I hope self explanitory
    makeArhiveHelper(argv[1], argv[2], argv[3])

    # Sends a notification to the desktop with the format of
    # Title:   Python Auto Backup
    # Message: TITLE.zip has been backed up to DESTINATION
    notification.notify("Python Auto Backup", argv[3] + ".zip has been backed up to " + argv[2])
# Python Backups!
Who doesn't love a good Python3 based 7zip clone?

I'm kidding, I made this file to automatically backup stuff to my network drive.

pip package `plyer` is needed

Example usage: Documents folder

usage: `auto.py source desination name`

```bash
python3 auto.py /home/user/Documents /mnt/NetworkShare/Backups Documents
```

This will produce a zip file with the name "Documents 12-12-23 4-20-00.zip

It will also notify you with the plyer notification package, but that is easily removable from the code (its at the bottom)

According to plyer documentation this should work on Linux, Windows, and MacOS

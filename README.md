# media_deduplicator
Just a little project for organize your gallery. 

Once all my photos and videos were duplicated three times in a row (because I'm an idiot).
To fix this fuckup, this script was written.

At start you need setup input and output dirs in config block.

Then, run script.

How it works:
Step 1: Sort files by extension
Step 2: Convert heic files to jpeg (because I need it, you can disable that step)
Step 3: Sort files by type
Step 4: Deduplicate photos
Step 5: Deduplicate videos
Step 6: Sort files by date (using exiftool)

After script finished, you will have you photos and videos without duplicates and organized on directories by year -> month

# dependencies
Native applications: exiftool, imagemagick, ffmpeg

# Crosspatform
Writed and tested on Windows WSL. 
If you have trouble - you can write me.

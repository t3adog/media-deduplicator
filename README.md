# media deduplicator
Just a little project for organize your gallery. 

Once all my photos and videos were duplicated three times in a row (because I'm an idiot).
To fix this fuck up, I writed this script.

At start you need setup **root_dir** parameter in config block.
root_dir need next sctructure inside:

* root_dir
    * source <-- Put inside all your photo and videos
    * work
    * output

Then, run script.

``` python3 main.py ```

What will happen:

    1. Sort files by extension into work dir.
    2. Convert heic files to jpeg (because I need it, you can disable that step. Just comment run function __convert_heic_to_jpg__ in main)
    3. Sort files by type
    4. Deduplicate photos (using PHash)
    5. Sort photos by date (using exiftool)
    6. Deduplicate videos (using Videohash)
    7. Sort videos by date (using exiftool)

After script finished, you will have your photos and videos without duplicates and organized on directories by year -> month in output dir.

> Warning: Some photos and videos without exif meta will not sorted at step 5 and 6. You need do it manually.

# quick start

You need install applications: 
* exiftool 
* imagemagick 
* ffmpeg

```pip install -r requirements.txt```

# What about crossplatform?
Writed and tested on Windows WSL. 
If you have trouble - you can write me.

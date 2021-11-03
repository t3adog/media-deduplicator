#!/usr/bin/python3

from posixpath import join
from PIL import Image
from imagededup.methods import PHash
from videohash import VideoHash
import pyheif
import os
import shutil
import time

#####################################################################
# Configuration module

root_dir = "/mnt/d/Data" # IMPLEMENT ME!
input_dir = os.path.join(root_dir, "source") # Keep your files here
photos = [".GIF", ".HEIC", ".JPEG", ".JPG", ".PNG", ".TIF"]
videos = [".MOV", ".MP4"]

#####################################################################

# Init block

work_dir = os.path.join(root_dir, "work")
work_extensions_dir = os.path.join(work_dir, "extensions")
work_types_dir = os.path.join(work_dir, "types")
work_photos_dir = os.path.join(work_types_dir, "photos")
work_videos_dir = os.path.join(work_types_dir, "videos")
work_other_dir = os.path.join(work_types_dir, "other")
output_dir = os.path.join(root_dir, "output")

os.makedirs(input_dir, exist_ok=True)
os.makedirs(work_dir, exist_ok=True)
os.makedirs(work_types_dir, exist_ok=True)
os.makedirs(work_photos_dir, exist_ok=True)
os.makedirs(work_videos_dir, exist_ok=True)
os.makedirs(work_other_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

#####################################################################

def sort_files_by_extension(path):
    '''Recursive get all files from source dir and copy them to work dir, organized by extension'''
    print('process ' + path)

    for dr in os.listdir(path):
        abs_path = os.path.join(path, dr)
        print('  process ' + abs_path)

        if os.path.isdir(abs_path):
            sort_files_by_extension(abs_path)
        else:
            file_extension = parse_file_extension(abs_path)

            work_dir_for_copy = os.path.join(work_extensions_dir, file_extension)
            os.makedirs(work_dir_for_copy, exist_ok=True)
            shutil.copy(abs_path, work_dir_for_copy)


def parse_file_extension(abs_path):
    '''Parse file extension'''
    filename, file_extension = os.path.splitext(abs_path)
    return file_extension.upper()


def convert_heic_to_jpg():
    '''Convert heic files to jpg'''
    dir_with_heic = os.path.join(work_extensions_dir, ".HEIC")
    dir_with_jpeg = os.path.join(work_extensions_dir, ".JPG")

    for file in os.listdir(dir_with_heic):
        print("try convert", file)
        try:
            filename, file_extension = os.path.splitext(file)
            heif_file = pyheif.read(os.path.join(dir_with_heic, file))
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            image.save(os.path.join(dir_with_jpeg, filename + ".jpg"), "JPEG", exif=extract_exif(heif_file.metadata))
            os.remove(os.path.join(dir_with_heic, file))
        except Exception as e:
            print("Error. Skip.", e)


def extract_exif(metadata):
    '''Parse exif from file metadata'''
    for meta in metadata:
        if meta["type"] == "Exif":
            return meta["data"]


def deduplicate_photos():
    '''Find photo duplicates with PHash and MOVE duplicates to scecial dir'''
    phasher = PHash()
    dir_with_duplicates = os.path.join(work_dir, "duplicates", "photos")
    os.makedirs(dir_with_duplicates, exist_ok=True)
    encodings = phasher.encode_images(image_dir=work_photos_dir)
    duplicates = phasher.find_duplicates_to_remove(encoding_map=encodings)
    for dublicate in duplicates:
        shutil.move(os.path.join(work_photos_dir, dublicate), os.path.join(dir_with_duplicates, dublicate))

def deduplicate_videos():
    '''Find video duplicates with VideoHash and MOVE duplicates to special dir'''
    dir_with_duplicates = os.path.join(work_dir, "duplicates", "videos")
    uniq_videos = {}
    duplicates = []
    os.makedirs(dir_with_duplicates, exist_ok=True)
    for video in os.listdir(work_videos_dir):
        print("Process ", video)
        videohash = str(VideoHash(path=os.path.join(work_videos_dir, video)))
        if videohash in uniq_videos:
            duplicates.append(video)
        else:
            uniq_videos[videohash] = video
    
    for duplicate in duplicates:
        shutil.move(os.path.join(work_videos_dir, duplicate), os.path.join(dir_with_duplicates, duplicate))

def sort_files_by_types(path):
    print('process ' + path)

    for dr in os.listdir(path):
        abs_path = os.path.join(path, dr)
        print('  process ' + abs_path)

        if os.path.isdir(abs_path):
            sort_files_by_types(abs_path)
        else:
            file_extension = parse_file_extension(abs_path)
            print("File extension", file_extension)
            work_dir_for_copy = os.path.join(work_types_dir, parse_file_type_by_extension(file_extension))
            print("work_dir_for_copy", work_dir_for_copy)
            os.makedirs(work_dir_for_copy, exist_ok=True)
            shutil.move(abs_path, work_dir_for_copy)


def sort_photos_by_exif_tool():
    '''Sort photos by date using exiftool'''
    os.system('exiftool -d ' + output_dir +
              '/%Y/%m "-directory<datetimeoriginal" ' + work_photos_dir + '/*')

def sort_videos_by_exif_tool():
    '''Sort videos by date using exiftool'''
    os.system('exiftool -d ' + output_dir +
              '/%Y/%m "-directory<CreateDate" ' + work_videos_dir + '/*')


def parse_file_type_by_extension(extension):
    '''Parse filetype by extension'''
    if extension in photos:
        return "photos"
    elif extension in videos:
        return "videos"
    else:
        return "other"


if __name__ == "__main__":
    root_time = time.time()
    start_time = time.time()

    #1
    print("Step 1: sort_files_by_extension")
    #sort_files_by_extension(input_dir)
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    #2
    print("Step 2: convert_heic_to_jpg")
    #convert_heic_to_jpg()
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    #3
    print("Step 3: sort_files_by_types")
    #sort_files_by_types(work_extensions_dir)
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    #4
    print("Step 4: deduplicate_photos")
    #deduplicate_photos()
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    #5
    print("Step 5: sort_photos_by_exif_tool")
    #sort_photos_by_exif_tool()
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    #6
    print("Step 6: deduplicate_videos")
    #deduplicate_videos()
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()


    #7
    print("Step 7: sort_videos_by_exif_tool")
    sort_videos_by_exif_tool()
    print("--- %s seconds ---" % (time.time() - start_time))


    #8
    print("--- FIN %s seconds ---" % (time.time() - root_time))

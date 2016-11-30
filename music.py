#!/usr/bin/python
# -s /Users/rustyparks/Music/Collection/

import argparse
import os
import pprint

import eyed3

file_types = {}
artists = {}


class Show:
    def __init__(self):
        pass
    none = 0
    files = 1
    folders = 2
    tagged = 4
    all = files | folders | tagged

to_print = Show.all


def main():
    arg_parser = argparse.ArgumentParser(description="Music file crawler")
    arg_parser.add_argument("-s", "--source", required=True, help="Source Directory", type=str)
    args = arg_parser.parse_args()

    print args.source

    crawl_folder(args.source)

    print '-----------------------------------'
    pretty_printer = pprint.PrettyPrinter(indent=4)
    pretty_printer.pprint(artists)
    print '-----------------------------------'

    while True and False:
        line = raw_input("Raw")

        try:
            print(eval(line))
        except Exception as e:
            print "Failed to execute command: %s" % e


def crawl_folder(folder_name, current_depth=0):
    global artists

    if current_depth == 0 and to_print > Show.none:
        print '-----------------------------------'
    spaces = '||  ' + '  ' * current_depth
    list_dir = os.listdir(folder_name)
    if not list_dir:
        print "empty dir :: " + folder_name
        os.rmdir(folder_name)

    for item in list_dir:

        if item.startswith('.'):
            continue  # skip .svn and .DS_Store type junk
        filename = os.path.join(folder_name, item)
        if os.path.isdir(filename):
            if to_print & Show.folders:
                print spaces + '+ ' + item
            crawl_folder(os.path.join(folder_name, item), current_depth+1)
        else:
            if to_print & Show.files:
                print spaces + '- ' + item
            filename, file_extension = os.path.splitext(item)

            # force extensions to lower case
            if not file_extension.islower():
                lower_ext = file_extension.lower()
                file_extension = lower_ext
                os.rename(os.path.join(folder_name, item), os.path.join(folder_name, filename + lower_ext))

            if file_extension == '.mp3':
                mp3 = eyed3.load(os.path.join(folder_name,  filename + file_extension))
                if mp3.tag is None:
                    print spaces + '   ' + "tagless mp3"
                    continue
                if mp3.tag.artist:
                    if mp3.tag.artist not in artists:
                        artists[mp3.tag.artist] = {'count': 1}
                    else:
                        artists[mp3.tag.artist]['count'] += 1
                else:
                    if "none" not in artists:
                        artists["none"] = {'count': 1}
                    else:
                        artists["none"]['count'] += 1

                if mp3.tag.title:
                    print spaces + '   ' + mp3.tag.title
                if mp3.tag.track_num:
                    print spaces + '   ' + str(mp3.tag.track_num[0])

            # store file extension
            if file_extension not in file_types:
                file_types[file_extension] = 1
            else:
                file_types[file_extension] += 1

    if current_depth == 0 and to_print > Show.none:
        print '-----------------------------------'
        pretty_printer = pprint.PrettyPrinter(indent=4)
        pretty_printer.pprint(file_types)
        print '-----------------------------------'


if __name__ == "__main__":
    main()

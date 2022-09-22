#!/usr/bin/env python3

from more_itertools import distinct_permutations as idp
import subprocess
import curses
import time
import signal


dictionary = "The Collaborative International Dictionary of English v.0.44"
output_filename = "/home/jwicks/software/sorted-words/curated-9.list"


word_list = []
with open("list-of-words.txt") as file:
    while (line := file.readline().rstrip()):
        word_list.append(line)


stdscr = curses.initscr()
curses.curs_set(0)
curses.noecho()

def handler(signum, frame):
    curses.curs_set(1)
    curses.echo()
    curses.endwin()
    outf.close()
    exit(0)

signal.signal(signal.SIGINT, handler)


window_permutations = curses.newwin(4, 40, 0, 0)
window_permutations.border()
window_permutations.refresh()

window_anagrams_found = curses.newwin(5, 30, 0, 41)
window_anagrams_found.border()
window_anagrams_found.refresh()

anagrams_found = 0
tlist = []

for item in word_list:

    window_permutations.clear()
    list_of_permutations = idp(item)

    for word_letters in list_of_permutations:
        window_permutations.border()
        window_permutations.addstr(1, 1, "Permutating: %s" % item)
        word = ''.join(word_letters)
        window_permutations.addstr(2, 1, "%s" % word)
        window_permutations.refresh()

        word_search = subprocess.run(["sdcv", "-e", "-n", "-u", dictionary, word], stdout=subprocess.PIPE, text=True)

        # Word not found in dictionary then try it capitalized
        if "sorry :(" in word_search.stdout:
            word_search = subprocess.run(["sdcv", "-e", "-n", "-u", dictionary, word.capitalize()], stdout=subprocess.PIPE, text=True)

            if "sorry :(" in word_search.stdout:
                continue


        tlist.append(word)
        if len(tlist) == 2:
            window_anagrams_found.addstr(1, 1, "%s has an anagram!   " % item)
            window_anagrams_found.addstr(2, 1, "%s      " % word)
            window_anagrams_found.refresh()
            break

    if len(tlist) == 1:
        with open(output_filename, "a") as outf:
            outf.write(item)
            outf.write("\n")
            outf.close()

    tlist.clear()

file.close()
curses.endwin()



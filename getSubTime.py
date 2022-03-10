"""
a program that gets the clip of a movie from matching the searched sentence with a line from the movie subtitles

i'm using en-core-web-sm (for english words and not that good for matching words and sentences)
if you want a better matching of the searched word with the subtitles use en_core_web_(md or lg)
with the command 'python spacy -m download en_core_web_md'
"""

import spacy
import tkinter as tk
from tkinter import filedialog
import pysrt
import logging
from moviepy.video.io.VideoFileClip import VideoFileClip


root = tk.Tk()
root.withdraw()
root.call("wm", "attributes", ".", "-topmost", True)

# use 'en_core_web_md' for better matching
nlp = spacy.load("en_core_web_sm")

logging.basicConfig(
    level=logging.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s"
)


# you select a subtitles file this function returns the start and end of the line your looking for
def get_start_end_time():
    print("select the sub")
    subs_file = filedialog.askopenfilename()
    sub = pysrt.open(subs_file, encoding="latin-1")
    searched_text = input("Enter the sentence you want to find :")
    for subed_line in sub:
        # calculates the similarity between the 'searched_text' and a subtitle line from the subtitles
        similarity = calc_similarity(subed_line.text, searched_text)
        if 0.8 <= similarity <= 1.0:
            # get the start, end time in seconds
            start_in_seconds = (
                subed_line.start.seconds
                + subed_line.start.minutes * 60
                + subed_line.start.hours * 3600
            )
            end_in_seconds = (
                subed_line.end.seconds
                + subed_line.end.minutes * 60
                + subed_line.end.hours * 3600
            )
            return [start_in_seconds, end_in_seconds]


def calc_similarity(text1, text2):
    base = nlp(text1)
    compare = nlp(text2)
    return base.similarity(compare)


# input start,end time in seconds , output a clip from the movie from start to end in the chosen dir
def extract_clip(start, end):
    print('select the the targeted movie file')
    the_movie = filedialog.askopenfilename()

    print('select where you want to output the extracted clip')
    extracted_clip_dir = filedialog.askdirectory()
    output_video_path = f"{extracted_clip_dir}/Extracted Clip.mp4"

    with VideoFileClip(the_movie) as movie:
        clip = movie.subclip(start, end)
        clip.write_videofile(output_video_path, audio_codec="aac")


try:
    start_time, end_time = get_start_end_time()
    extract_clip(start_time, end_time)
except TypeError:
    print("Sentence Not found in the subtitles")

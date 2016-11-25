# Chinese Text Segmenter

This is a tool I've written in the processing of trying to learn Mandarin. It
segments a text into words, allowing to calculate the most common words which
occur in a a given book. It can also sort these words normalized by their
general frequency, to give a list of the words which are common in that book
but not common generally.

## Installing

Run `python setup.py install` to install. This requires having Python 2.

## Usage

Note that this program expects UTF-8 input files. For files in GB18030 format
(commonly used in china), the command `iconv -f GB18030 -t utf-8` can be used
to convert them.

The following commands can be run:

* `zhtext segment FILE`: Determines the word boundaries in a given chinese text and outputs that text with the words separated by spaces.
* `zhtext words FILE`: Using the same word segmentation algorithm, outputs the most common words in a given text, along with how many times each occurs.

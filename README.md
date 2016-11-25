# Chinese Text Tools

These are some tools I've written in the processing of trying to learn Mandarin.

## Installing

Run `python setup.py install` to install.

## Usage

Note that this program expects UTF-8 input files. For files in GB18030 format
(commonly used in china), the command `iconv -f GB18030 -t utf-8` can be used
to convert them.

* `zhtext segment FILE`: Determines the word boundaries in a given chinese text and outputs that text with the words separated by spaces.
* `zhtext words FILE`: Using the same word segmentation algorithm, outputs the most common words in a given text, along with how many times each occurs.

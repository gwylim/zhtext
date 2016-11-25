# Chinese Text Tools

These are some tools I've written in the processing of trying to learn Mandarin.

## Installing

Run `python setup.py install` to install.

## Usage

* `zhtext segment FILE`: Determines the word boundaries in a given chinese text and outputs that text with the words separated by spaces.
* `zhtext counts FILE`: Using the same word segmentation algorithm, outputs the most common words in a given text, along with how many times each occurs.

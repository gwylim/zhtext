# -*- coding: utf-8 -*-

import hanzi
import collections
import re
import pkg_resources

def read_dictionary():
    '''
    Read and construct dictionary of words, with traditional, simplified, pinyin, and definitions
    '''
    dict_data = pkg_resources.resource_stream(__name__, 'data/cedict_1_0_ts_utf-8_mdbg.txt')
    dict_re_s = r'(\S+)\s+(\S+)\s+\[(.*)\]\s+/(.*)/'
    dict_re = re.compile(dict_re_s, flags=re.UNICODE)

    def read_dict_entry(s):
        if len(s) == 0 or s[0] == '#':
            return None
        groups = dict_re.match(s).groups()
        return {'traditional': groups[0], 'simplified': groups[1], 'pinyin': groups[2], 'definition': groups[3]}
    dictionary = collections.defaultdict(list)
    for line in dict_data.readlines():
        entry = read_dict_entry(line.strip().decode('utf-8'))
        if entry is not None:
            dictionary[entry['simplified']].append(entry)
    return dictionary

def split_hanzi_nonhanzi(text):
    '''
    Splits the given string into alternating non-hanzi and hanzi parts. Each part
    will be non-empty, except that the first part will always consist of non-hanzi
    characters (and will be an empty string if the input starts with a hanzi).
    '''
    text_parts = []
    current_part = ''
    current_part_is_hanzi = False
    for c in text:
        if hanzi.is_hanzi(c):
            if not current_part_is_hanzi:
                current_part_is_hanzi = True
                text_parts.append(current_part)
                current_part = ''
            current_part += c
        else:
            if current_part_is_hanzi:
                current_part_is_hanzi = False
                text_parts.append(current_part)
                current_part = ''
            current_part += c
    if current_part:
        text_parts.append(current_part)
    return text_parts

def read_frequencies(dictionary, text_parts):
    '''
    Reads the frequencies of the sequence of characters making up each word in the
    dictionary in the given text. This does not attempt to take into account word
    boundaries, just counts the raw frequency of each string.
    '''
    max_word_length = 20
    hanzi_parts = text_parts[1::2]
    frequencies = collections.Counter()
    for part in hanzi_parts:
        for i in xrange(len(part)):
            for j in xrange(i, min(i + max_word_length, len(part))):
                word = part[i:j]
                if word in dictionary:
                    frequencies[word] += 1
    return frequencies

def read_subtlex_frequencies():
    '''
    Reads word frequency data from SUBTLEX-CH dataset (see
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2880003/)
    '''
    freq_data = pkg_resources.resource_stream(__name__, 'data/SUBTLEX-CH-WF')
    result = collections.defaultdict(lambda: 1)
    for line in freq_data.readlines():
        word, count = line.decode('utf-8').split()[:2]
        result[word] = int(count)
    return result

def split_into_words(dictionary, frequencies, text):
    dp = [None for i in xrange(len(text) + 1)]
    lengths = [0 for i in xrange(len(text) + 1)]
    products = [1 for i in xrange(len(text) + 1)]
    dp[0] = 0
    for i in xrange(1, len(text) + 1):
        dp[i] = None
        for j in xrange(i):
            if dp[j] is None:
                continue
            w = text[j:i]
            # we allow length 1 non-words in case some characters don't have entries in the dictionary
            if w not in dictionary and i - j > 1:
                continue
            if dp[i] is None or lengths[dp[i]] > lengths[j]:
                dp[i] = j
                continue
            if lengths[dp[i]] < lengths[j]:
                continue
            # lengths are equal, break ties by product of frequencies
            w_freq = max(1, frequencies[w])
            # TODO: optimize a bit by removing repeated stuff
            prev_freq = max(1, frequencies[text[dp[i]:i]])
            if prev_freq * products[dp[i]] < w_freq * products[j]:
                dp[i] = j
        if dp[i] is not None:
            lengths[i] = lengths[dp[i]] + 1
            products[i] = products[dp[i]] * max(1, frequencies[text[dp[i]:i]])
    if dp[len(text)] is None:
        return [text]
    result = []
    i = len(text)
    while dp[i] != i:
        result.append(text[dp[i]:i])
        i = dp[i]
    result.reverse()
    return result

def segment(dictionary, frequencies, text_parts):
    '''
    Segment the parts containing hanzi from the output of split_hanzi_nonhanzi into
    words. The output has the same format as split_hanzi_nonhanzi, except that the
    hanzi parts contain a list of strings which are the words, instead of a single
    string.
    '''
    segmented_text_parts = []
    for i, part in enumerate(text_parts):
        if i % 2 == 0:
            segmented_text_parts.append(part)
        else:
            segmented_text_parts.append(split_into_words(dictionary, frequencies, part))
    return segmented_text_parts

def get_words(segmented_text_parts):
    '''
    Returns the words from the output of segment
    '''
    result = []
    map(result.extend, segmented_text_parts[1::2])
    return result

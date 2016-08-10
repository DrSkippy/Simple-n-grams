#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import codecs
import argparse
import fileinput

from simple_n_grams.simple_n_grams import SimpleNGrams

if sys.version_info[0] < 3:
    try:
        reload(sys)
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
        sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    except NameError:
        pass

if __name__ == "__main__":
    grams_parser = argparse.ArgumentParser(
            description="See list of 1 and 2 grams (bag-of-words) for input corpus--1 docudment per line.")
    grams_parser.add_argument("file_name", metavar= "file_name", nargs="?", default=[], 
            help="Input file name (optional).")
    grams_parser.add_argument("-n", "--number-of-grams", dest="number_of_grams", default=None,
            help="Limit list to top n 1-grams and top n 2-grams.")
    grams_parser.add_argument("-c", "--char-limit", dest="char_limit", default=2, 
            help="The shortest grams to include in the count.")
    grams_parser.add_argument("-p", "--pretty-print", dest="pretty_print", action="store_true", default=False,
            help="Prettier output format")
    grams_parser.add_argument("-k", "--n-grams", dest="n_grams", default=2,
            help="N-gram depth (default 2)")
    grams_parser.add_argument("-t", "--space-tokenizer", dest="space_tokenizer", default=False, action="store_true",
            help="Use alternate tokization on white-space only.")
    grams_parser.add_argument("-w", "--twitter-tokenizer", dest="twitter_tokenizer", default=False, action="store_true",
            help="Use alternate Twitter tokization with hashtags and mentions intact.")
    grams_parser.add_argument("-f", "--filter", dest="filter", default=None,
            help="List of terms to filter \"the,and,happy\"")
    opts = grams_parser.parse_args()

    if opts.space_tokenizer:
        tokenizer = "space"
    elif opts.twitter_tokenizer:
        tokenizer = "twitter"
    else:
        tokenizer = "word"

    f = SimpleNGrams(char_lower_cutoff=int(opts.char_limit), n_grams=opts.n_grams, tokenizer=tokenizer)
    if opts.filter is not None:
        tmp = [x.lower().strip() for x in opts.filter.split(",")]
        f.sl.add_session_stop_list(tmp)
    for row in fileinput.FileInput(opts.file_name,openhook=fileinput.hook_encoded("utf-8")):
        f.add(row)
    if opts.number_of_grams is None:
        res = f.get_repr(opts.number_of_grams)
    else:
        res = f.get_repr(int(opts.number_of_grams))
    if opts.pretty_print:
        fmt = ["%5s", "%9s", "%5s", "%9s", "%34s", "%7s"] 
        for x in res.split('\n'):
            tmp_str = x.strip().split(",")
            sys.stdout.write(" ".join([j%i for i,j in zip(tmp_str,fmt)]) + "\n")
    else:
        sys.stdout.write(res)
    f.term_dictionary("./term_dict.pickle", co=int(opts.char_limit))
    # recover with e.g. pickle.load(open("./term_dict.pickle", "rb"))


#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import pickle
import operator
import re
import codecs

from .stop_words import StopWords

if int(sys.version_info[0]) < 3:
    try:
        reload(sys)
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
        sys.stdin = codecs.getreader('utf-8')(sys.stdin) 
    except NameError:
        pass

# pre-compile some res
# xml/html tags
markup_tag_re = re.compile(r'<.*?>', re.UNICODE)
space_tokenizer_re =  re.compile('\s+', re.UNICODE)
word_tokenizer_re =  re.compile('\W+', re.UNICODE)
end_entity_re = re.compile('[\s.,?!\t\n():;#$@&"]', re.UNICODE)
shortened_url_re = re.compile('http://[a-zA-Z]+.[a-zA-Z]+/[a-zA-Z0-9]+/?', re.UNICODE)

class SimpleNGrams:
    
    def __init__(self, 
            char_lower_cutoff = 2,
            char_upper_cutoff = 25,
            cutoff = 0.00001,
            tokenizer = None,
            token_iter = None,
            n_grams = 2):
        self.char_lower_cutoff = char_lower_cutoff
        self.char_upper_cutoff = char_upper_cutoff
        # if cutoff < 1, compare frac else total count
        self.cutoff = cutoff
        # Tokenizer can be either a key word in pre-defined tokenizers or None
        # When None, tokenizer_reg_ex must be defined
        if tokenizer is None:
            if token_iter is not None:
                self.token_iter = token_iter
            else:
                print >>sys.stderr, "Please define valid tokenizer regular expression. Exiting!"
                sys.exit()
        else:
            VALID_TOKENIZERS = ['word','space','twitter']
            if tokenizer.lower() not in VALID_TOKENIZERS:
                print >>sys.stderr, "Please select valid tokenizer from {}. Exiting!".format(VALID_TOKENIZERS)
                sys.exit()
            else:
                if tokenizer.lower().startswith("word"):
                    self.token_iter = self.word_token_iter
                elif tokenizer.lower().startswith("space"):
                    self.token_iter = self.space_token_iter
                elif tokenizer.lower().startswith("twit"):
                    self.token_iter = self.twitter_token_iter
        self.n_grams = int(n_grams)
        self.sl = StopWords()
        self.start_new()

    def word_token_iter(self, row):
        """Split a row on word boundaries as defined by regex W options"""
        return [x.lower() for x in word_tokenizer_re.split(row)]

    def space_token_iter(self, row):
        """Split a row only on whitespace"""
        return [x.lower() for x in space_tokenizer_re.split(row)]

    def twitter_token_iter(self, row):
        res = self.get_twitter_entities(row,"#") \
            + self.get_twitter_entities(row,"@") \
            + [x.upper() for x in self.get_twitter_entities(row,"$")] \
            + self.get_shortened_urls(row)
        #remove id'd tags before tokening remainder
        return res + [x.lower() for x in word_tokenizer_re.split(markup_tag_re.sub(' ', self.remove(row, res)))]

    def remove(self, row_str, word_list):
        for x in word_list:
            row_str = row_str.replace(x, " ")
        return row_str

    def get_twitter_entities(self, row, marker):
        """Extract text items that start with special markers such as @ and #"""
        tags = []
        in_tag = False
        for x in row:
            if x == marker and not in_tag:
                in_tag = True
                tag = marker
            elif in_tag and end_entity_re.findall(x) != []:
                tags.append(tag)
                in_tag = False
            elif in_tag:
                tag += x
        return tags

    def get_shortened_urls(self, row):
        """Extract shortened urls from text"""
        return shortened_url_re.findall(row)

    def start_new(self):
        self.token = {i+1:{"tcnt":0, "gram_dict":{}} for i in range(self.n_grams)}
        self.activities = {}
        self.acnt = 0
        self.max_term_freq = -sys.maxsize

    def add(self, row):
        if row.strip() == '':
           return 
        self.acnt += 1
        act_set = set()
        last_tok_list = []
        for tok in self.token_iter(row):
            # Be sure to deal with lower-ing in tokenizer if necessary!
            #gram = tok.strip().lower()
            gram = tok.strip()
            tmp = gram
            if len(tmp) > self.char_lower_cutoff and len(tmp) < self.char_upper_cutoff and not self.sl[tmp]:
                for i in range(min([self.n_grams, 1 + len(last_tok_list)])):
                    self.token[i+1]["tcnt"] += 1
                    self.token[i+1]["gram_dict"][tmp] = 1 + self.token[i+1]["gram_dict"].get(tmp, 0)
                    if tmp not in act_set:
                        self.activities[tmp] = 1 + self.activities.get(tmp, 0)
                        act_set.add(tmp)
                    tmp = ' '.join(last_tok_list[-(i+1):] + [gram])
                last_tok_list.append(gram)
                if len(last_tok_list) > self.n_grams:
                    last_tok_list.pop(0)

    def _gets(self, rec_tuples, counts):
        for tok in rec_tuples:
            tokenFrac = tok[1]/float(counts)
            activitiesFrac = self.activities[tok[0]]/float(self.acnt)
            if (self.cutoff < 1 and tokenFrac > self.cutoff) or (self.cutoff >= 1 and tok[1] > self.cutoff):
                yield [ tok[1], tokenFrac, self.activities[tok[0]], activitiesFrac, tok[0]]
   
    def get_tokens(self, n=None):
        for i in range(self.n_grams):
            for x in self._gets(sorted(self.token[i+1]["gram_dict"].items(), key=operator.itemgetter(1), reverse=True)[:n], self.token[i+1]["tcnt"]):
                    if x[0] > self.max_term_freq:
                        self.max_term_freq = x[0]
                    yield x

    def build_string_list(self, mixed_list, mant=6):
        fmt = ["%d", "%%4.%df"%mant, "%d", "%%4.%df"%mant, "%s", "%s"]
        return [ f%x for x, f in zip(mixed_list, fmt) ]

    def __iter__(self):
        for x in self.get_tokens():
            yield x 

    def term_dictionary(self, file_name, co=2):
        # E.g.
        # list is [ count terms, count terms /uniq terms, docs appearances, doc appearances/docs ]
        # {'meta': {'cutoff': 3, 'max_term_freq': 17, 'n_docs': 12, 'n_terms': 697},
        # 'terms': {u'answered': [4, 0.005738880918220947, 2, 0.16666666666666666],
        #               u'both': [7, 0.010043041606886656, 3, 0.25],
        #              u'cause': [4, 0.005738880918220947, 2, 0.16666666666666666],
        #   ...
        #
        inner = {}
        term_id = 0
        for x in self.get_tokens():
            if x[0] >= co:
                inner[x[4]] = x[:4] + [term_id]
                term_id += 1
        res = {"terms": inner,
                "meta": {"n_docs":self.acnt , 
                        "n_terms":self.token[1]["tcnt"] ,
                        "max_term_freq": self.max_term_freq ,
                        "cutoff":co}}
        pickle.dump(res, open(file_name, "wb"))
        # make the id-keyed dictionary so we can look it up later
        kv = {}
        for k,v in inner.items():
            kv[k] = v[4]
        fn = file_name.rsplit(".",1)
        if len(fn) > 1:
            fn = ".lookup.".join(fn)
        else:
            fn += ".lookup"
        res = {"terms": kv,
        "meta": {"n_docs":self.acnt , 
                "n_terms":self.token[1]["tcnt"] ,
                "max_term_freq": self.max_term_freq ,
                "cutoff":co}}
        pickle.dump(res, open(fn, "wb"))


    def get_repr(self, n=None):
        # if you want a header in the output
        res = u','.join([ "total count", "percent of total", "activities count", "percent of activities","tokens", "n_gram\n"])
        for x in self.get_tokens(n):
            res += ','.join(self.build_string_list(x) + ["%dgrams\n"%(x[-1].count(" ") + 1)])
        return res


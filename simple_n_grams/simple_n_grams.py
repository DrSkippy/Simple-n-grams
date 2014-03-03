#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import pickle
import operator
import re

from stop_words import StopWords


# xml/html tags
tagRE = re.compile(r'<.*?>', re.UNICODE)

class SimpleNGrams:
    
    def __init__(self, 
            charCutoff = 2,
            charUpperCutoff = 25,
            cutoff = 0.00001,
            space_tokenizer=False,
            n_grams = 2):
        self.char_cutoff = charCutoff
        self.char_upper_cutoff = charUpperCutoff
        # if cutoff < 1, compare frac else total count
        self.cutoff = cutoff
        self.space_tokenizer = space_tokenizer
        self.n_grams = int(n_grams)

        self.sl = StopWords()
        self.start_new()

    def start_new(self):
        self.token = {i+1:{"tcnt":0, "gram_dict":{}} for i in range(self.n_grams)}
        self.activities = {}
        self.acnt = 0
        self.max_term_freq = -sys.maxint

    def add(self, row):
        if row.strip() == '':
           return 
        self.acnt += 1
        if self.space_tokenizer:
            rl = re.compile('\s+', re.UNICODE).split(unicode(row,'utf-8'))
        else:
            rl = re.compile('\W+', re.UNICODE).split(tagRE.sub(' ',row))
        act_set = set()
        last_tok_list = []
        for tok in rl:
            gram = tok.strip().lower()
            tmp = gram
            if len(tmp) > self.char_cutoff and len(tmp) < self.char_upper_cutoff and not self.sl[tmp]:
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
        res = u','.join([ "count", "frac_gram", "act_count", "act_frac", "tokens", "n_gram\n"])
        for x in self.get_tokens(n):
            res += ','.join(self.build_string_list(x) + ["%dgrams\n"%(x[-1].count(" ") + 1)])
        return res


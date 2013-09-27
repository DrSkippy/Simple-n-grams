Simple-n-grams
==============
<pre>
./term_frequency.py -h
usage: term_frequency.py [-h] [-n NUMBER_OF_GRAMS] [-c CHAR_LIMIT] [-p]
                         [-k N_GRAMS] [-f FILTER]
                         [file_name]

See list of 1 and 2 grams (bag-of-words) for input corpus--1 docudment per
line.

positional arguments:
  file_name             Input file name (optional).

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER_OF_GRAMS, --number-of-grams NUMBER_OF_GRAMS
                        Limit list to top n 1-grams and top n 2-grams.
  -c CHAR_LIMIT, --char-limit CHAR_LIMIT
                        The shortest grams to include in the count.
  -p, --pretty-print    Prettier output format
  -k N_GRAMS, --n-grams N_GRAMS
                        N-gram depth (default 2)
  -f FILTER, --filter FILTER
                        List of terms to filter "the,and,happy"

</pre>

Using the example in the data package, the first column is the term count, the second
is the fraction of all term counts, ther third is the number of paragraphs (defined
by \n) containing the term and the fourth, the fraction fo paragraphs.


term_frequency.py Simple-n-grams/data/LanceArmstrongWikipedia.txt 

##1-Grams

<pre>
count,frac_gram,act_count,act_frac,n_gram
13,0.045296,4,1.000000,armstrong,1grams
6,0.020906,2,0.500000,doping,1grams
6,0.020906,4,1.000000,tour,1grams
5,0.017422,2,0.500000,2012,1grams
5,0.017422,4,1.000000,between,1grams
5,0.017422,4,1.000000,france,1grams
5,0.017422,3,0.750000,2005,1grams
4,0.013937,2,0.500000,team,1grams
4,0.013937,2,0.500000,cancer,1grams
4,0.013937,3,0.750000,cycling,1grams
4,0.013937,2,0.500000,usada,1grams
4,0.013937,2,0.500000,lance,1grams
3,0.010453,3,0.750000,competitive,1grams
3,0.010453,2,0.500000,february,1grams
3,0.010453,2,0.500000,january,1grams
3,0.010453,1,0.250000,sport,1grams
3,0.010453,2,0.500000,racing,1grams
3,0.010453,1,0.250000,announced,1grams
3,0.010453,2,0.500000,foundation,1grams
3,0.010453,3,0.750000,professional,1grams
3,0.010453,2,0.500000,having,1grams
2,0.006969,1,0.250000,including,1grams
2,0.006969,1,0.250000,edward,1grams
2,0.006969,2,0.500000,2011,1grams
2,0.006969,2,0.500000,returned,1grams
2,0.006969,2,0.500000,competing,1grams
2,0.006969,2,0.500000,world,1grams
2,0.006969,1,0.250000,postal,1grams
2,0.006969,1,0.250000,brain,1grams
2,0.006969,1,0.250000,decision,1grams
2,0.006969,2,0.500000,won,1grams
2,0.006969,1,0.250000,stage,1grams
2,0.006969,2,0.500000,cyclist,1grams
2,0.006969,2,0.500000,career,1grams
2,0.006969,2,0.500000,anti,1grams
2,0.006969,2,0.500000,uci,1grams
2,0.006969,1,0.250000,1993,1grams
2,0.006969,2,0.500000,october,1grams
2,0.006969,2,0.500000,1996,1grams
2,0.006969,2,0.500000,1999,1grams
2,0.006969,1,0.250000,1998,1grams
2,0.006969,2,0.500000,seven,1grams
2,0.006969,2,0.500000,triathlon,1grams
2,0.006969,1,0.250000,began,1grams
2,0.006969,2,0.500000,agency,1grams
...

</pre>
##2-Grams

<pre>
5,0.017668,4,1.000000,tour france,2grams
3,0.010601,3,0.750000,competitive cycling,2grams
2,0.007067,2,0.500000,anti doping,2grams
2,0.007067,2,0.500000,doping agency,2grams
2,0.007067,2,0.500000,between 1999,2grams
2,0.007067,1,0.250000,lance edward,2grams
2,0.007067,2,0.500000,armstrong foundation,2grams
2,0.007067,2,0.500000,lance armstrong,2grams
2,0.007067,1,0.250000,armstrong began,2grams
2,0.007067,2,0.500000,1999 2005,2grams
1,0.003534,1,0.250000,third 2009,2grams
...
</pre>

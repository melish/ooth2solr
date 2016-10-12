from collections import defaultdict

import argparse
import re


parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?', default='th_en_US_v2.dat', help='Input file')
parser.add_argument('outfile', nargs='?', default='synonyms.txt', help='Output file')

parser.add_argument('--related', action='store_true', help='Include related terms.')
parser.add_argument('--similar', action='store_true', help='Include similar terms.')
parser.add_argument('--generic', action='store_true', help='Include generic terms.')
parser.add_argument('--antonym', action='store_true', help='Include antonyms.')
parser.add_argument('--no-skip-first', action='store_true', help='Don\'t skip the first line.')
parser.add_argument('--ignore-case', action='store_true', help='Make all words lowercase')

args = parser.parse_args()

types = {
    ' (generic term)': args.generic,
    ' (similar term)': args.similar,
    ' (related term)': args.related,
    ' (antonym)': args.antonym,
}
repattern = "|".join([re.escape(t) for t in types])

result = defaultdict(set)
reverse = {}

with open(args.infile) as f:
    if not args.no_skip_first:
        # Skip 'UTF-8' on first line
        f.readline()
    for line in iter(f.readline, ''):
        # line = word|count
        ref, count = line.split('|')
        if ref in reverse:
            ref = reverse[ref]
        for i in range(int(count)):
            # line = (type)|word
            synset = f.readline().rstrip().split('|')[1:]
            for k, v in types.iteritems():
                synset = filter(lambda x: v or not x.endswith(k), synset)
            synset = [re.sub(repattern, '', syn) for syn in synset]
            if args.ignore_case:
                synset = [syn.lower() for syn in synset]
            ref = next((reverse.get(syn) for syn in synset if syn in reverse), ref)
            if args.ignore_case:
                ref = ref.lower()
            result[ref] = result[ref].union(set(synset))
            for syn in (x for x in synset if x not in reverse):
                reverse[syn] = ref
# output to file
with open(args.outfile, 'wb') as f:
    for word, synset in result.iteritems():
        synset = synset.union([word])
        if len(synset) > 1:
            f.write(', '.join(synset))
            f.write('\n')
#    import pprint
#    pp = pprint.PrettyPrinter(indent=2)
#    pp.pprint(result.items())

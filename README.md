# ooth2solr
Convertor from OpenOffice thesaurus (th_en_US_v2) to Solr synonyms.txt.
Accepts input files similar to th_en_US_v2.dat from [OpenOffice dict-en.oxt](http://extensions.openoffice.org/en/project/english-dictionaries-apache-openoffice)

```
usage: convert.py [-h] [--related] [--similar] [--generic] [--antonym]
                  [--no-skip-first] [--ignore-case]
                  [infile] [outfile]

positional arguments:
  infile           Input file
  outfile          Output file

optional arguments:
  -h, --help       show this help message and exit
  --related        Include related terms.
  --similar        Include similar terms.
  --generic        Include generic terms.
  --antonym        Include antonyms.
  --no-skip-first  Don't skip the first line.
  --ignore-case    Make all words lowercase
```
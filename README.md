# ClarAVy

ClarAVy is a tool for tagging malware using antivirus scan data. ClarAVy mainly tags malware according to category/behavior (e.g. ransomware, downloader, autorun) and file properties (e.g. win64, pdf, java). It can also tag malware by the vulnerability that it exploits (e.g. cve_2017_0144, ms08_067) and by packer (e.g. upx, themida).

### How ClarAVy Works 
ClarAVy takes .jsonl files as input, where each line is a JSON VirusTotal report containing antivirus results about a malicious file. ClarAVy tokenizes each antivirus label and identifies the type of each token (i.e. whether it indicates a malicious behavior, file property, etc). Then, it identifies token aliases -- tokens with different spellings but identical meanings (such as bkdr and backdoor). If enough antivirus products output the same token in their labels, it will be included as a tag in the output. 


### Installation:

```
pip install git+https://github.com/NeuromorphicComputationResearchProgram/ClarAVy
```

## Usage:

ClarAVy accepts JSON reports from versions 2 and 3 of the VirusTotal API as input, and automatically detects the version. ClarAVy can accept one or more .jsonl files as input using the -f flag, or a directory of .jsonl files using the -d flag.

```
claravy.py -f /path/to/scan_file.jsonl
```

```
claravy.py -f /path/to/scan_file1.jsonl -f /path/to/scan_file2.jsonl
```

```
claravy.py -d /path/to/scan_dir/
```


By default, ClarAVy writes results to stdout. The -o flag causes the results to be written to a file instead. ClarAVy uses the same output format as AVClass2:

```
claravy.py -f /path/to/scan_file.jsonl -o out_file.txt
```

```
cb327e327196d5f49e711a4d8df07dbc        58      BEH:ransom|17,BEH:exploit|8,VULN:cve_2017_0147|4
```


### Cusomizing ClarAVy Preferences

ClarAVy's default configuration files are located in the claravy/data/ folder. You may also use your own configuration files to change how ClarAVy runs.

The antivirus products listed in claravy/data/default_avs.txt are the set of 90 antivirus products that ClarAVy supports by default. This file also lists if each antivirus product is known to be associated with any other AVs (due to sub-licensing another AV's engine, being owned by the same company, or having a sharing partnership). If multiple antivirus products with known associations agree on a tag, they will be counted as a single vote in total. You can use the -av flag to define your own set of supported antivirus products instead. Antivirus products whose names are not in this file will not be parsed and will not contribute to voting on tags:

```
claravy.py -f /path/to/scan_file.jsonl -av my_av_file.txt
```

ClarAVy automatically determines each token's type after parsing the dataset.  A default taxonomy file can be found in claravy/data/default_taxonomy.txt. It was generated by running ClarAVy on approximately 40 million VirusTotal reports for chunks 0-465 of the VirusShare dataset. Then, we manually reviewed and edited the taxonomy to our own preferences. If you would like to override any token type assignments, you can use the -tax flag to define your own custom token taxonomy:

```
claravy.py -f /path/to/scan_file.jsonl -tax my_taxonomy_file.txt
```

ClarAVy also automatically identifies token aliases, which have different spellings but identical meanings. It does this using both edit distance between tokens and the frequency the two tokens co-occur in reports. We generated the alias mapping in claravy/data/default_aliases.txt using the same method as the token taxonomy. You can use the -al flag to specify your own alias mapping:

```
claravy.py -f /path/to/scan_file.jsonl -al my_alias_file.txt
```


### Adjusting ClarAVy Ranking

You can choose custom thresholds for how many antivirus products must agree in order to output a tag. By default, this is 5 for behavior and file tags, and 1 for vulnerability and packer tags. The -bt, -ft, -vt, and -pt flags set the voting thresholds for behavior, file, vulnerability, and packer tags respectively. 

```
claravy.py -f /path/to/scan_file.jsonl -bt 10 -ft 10 -vt 3 -pt 3
```




### Processing Lots of Data

ClarAVy supports multiprocessing and can handle tens of millions of scan reports. The --num-processes flag sets the number of workers for parsing antivirus scans in parallel, and the --batch-size flag sets the number of scans that each worker processes at a time. Increasing the number of workers and the batch size can impove runtime for large sets of scan reports, but be aware that it will also consume more memory and I/O.

```
claravy.py -f /path/to/scan_file.jsonl --num-processes 8 --batch-size 4000
```


## What Makes ClarAVy Different from AVClass2?

[AVClass2](https://github.com/malicialab/avclass) is a similar tool which also use antivirus scan data to tag malware. ClarAVy distinguishes itself from AVClass2 with its comprehensive antivirus label parsing. Antivirus products output labels in many different types of formats, and certain types of tokens tend to appear in predible locations within those formats. ClarAVy uses the format of an antivirus label to select an appropriate parsing function, which then applies basic pattern matching to determine the type of each token in the label. ClarAVy supports 90 common antivirus products and can parse nearly 900 different antivirus label formats. We developed and validated ClarAVy's parser using over 1.1 billion antivirus labels, and it has coverage for over 99.5\% of them. In the cases of rare antivirus formats which ClarAVy does not support, it is able to infer the types of tokens which it has parsed elsewhere. We believe that this results in a noticable difference in tagging quality.

ClarAVy also uses different strategies for identifying token aliases and for ranking tags produced by antivirus products with known correlations between them.


## What's Next?

ClarAVy does not yet support tagging malware according to family. This is  feature that we are actively developing. We are also working on improved alias detection, removal of low-confidence antivirus labels, and a more intelligent voting strategy. Stay tuned for future updates!

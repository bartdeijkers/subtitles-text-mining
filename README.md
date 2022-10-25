# subtitles-text-mining

---
	Title: Subtitles text-mining using Python
	Author: Bart Deijkers (bartdeijkers@gmail.com)
	Date: 2022-10-19
---

## Dataset NPO Start

Subtitles of the NPO are available starting 2015 via the NPO Start website. 
Only the Dutch subtitles were used for this study.

Subtitles normally do not correspond 100% to the actual spoken text, but are equally suitable as a source for data analysis. Long sentences are made more compact because of the limitations of the medium, without losing essence. This benefits the analysis, because less noise needs to be filtered. In addition, descriptions such as 'applause', 'laughter', 'cheers' and 'music' are easy to filter.

The subtitle analysis in this repository does not take into account pause padding (***) or silence markings for the hearing impaired.

# Helpful Tools

To convert vtt files yourself a script is included. 
Currently the script supports single file conversion or npostart batch conversion utilizing the npostart.nl video tiles metadata objects

### Npostart.nl batch mode example

When programs are watched on npostart.nl you can extract the episode information in json format using firebug. 
The xmlhttprequest starting with 'episodes' contains the meta information needed to parse using the 'scripts/vtt2json.py' script. 
Copy the json data from firebug into a seperate .json file and feed this to the vtt2json.py.

Example:
```sh
$ python .\scripts\vtt2json.py --batch_in meta.json  --method npostart 
```


### Single file example 

For subtitle files (in vtt format) it is also possible to run the vtt2json.py script in individual file mode

Example:
```sh
$ python .\scripts\vtt2json.py --file_in subtitlefile.vtt
```


# Sources
- http://www.natalialevshina.com/Documents/Olomouc_subtitles.pdf

	Discusses methods to analyse vtt subtitles
	- average word lengths
	- correlations between wordform frequencies in each register
	- Principal Component Analysis (similar to Biber's multidimensional analysis)

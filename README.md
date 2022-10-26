# subtitles-text-mining

---

- Title: Subtitles text-mining with Python
- Author: Bart Deijkers (bartdeijkers@gmail.com)
- Date: 2022-10-19

---

## Introduction

Subtitles of the NPO are available starting 2015 via the NPO Start website.
Only the Dutch subtitles were used for this study.

Subtitles normally do not correspond 100% to the actual spoken text, but are equally suitable as a source for data analysis. Long sentences are made more compact because of the limitations of the medium, without losing essence. This benefits the analysis, because less noise needs to be filtered. In addition, descriptions such as 'applause', 'laughter', 'cheers' and 'music' are easy to filter.

The subtitle analysis in this repository does not take into account pause padding (***) or silence markings for the hearing impaired.

## Usage

1. Open subtitle_analysis.ipynb in jupyter.
2. Download and install the requirements defined in the first code cell.
3. download and convert the subtitles using the scripts/vtt2json.py script if needed and place the json files in ./data/json/ folder
4. Run all cells in the jupyter notebook to analyse the provided data

## Docker support

For setting up the development system, a docker-compose.yml is included. To run (assuming docker is installed and running on the local system) type the following in your terminal:

```sh
docker compose -f "docker-compose.yml" up -d --build 
```

You can use the jupyter environment in your browser using the url provided in the docker console after loading the container.
The next terminal line requests the credentials and url to the jupyter environment from the log:

```sh
docker-compose logs -t -f --tail 5
```

Note: The contents of the repository directory are copied to the container volume.

## Helpful Tools

To convert vtt files yourself a script is included.
Currently the script supports single file conversion or npostart batch conversion utilizing the npostart.nl video tiles metadata objects

### Npostart.nl batch mode example

When programs are watched on npostart.nl you can extract the episode information in json format using firebug.
The xmlhttprequest starting with 'episodes' contains the meta information needed to parse using the 'scripts/vtt2json.py' script.
Copy the json data from firebug into a seperate .json file and feed this to the vtt2json.py.

Example:

```sh
python .\scripts\vtt2json.py --file_in meta.json  --method npostart 
```

### Single file example

For subtitle files (in vtt format) it is also possible to run the vtt2json.py script in individual file mode

Example:

```sh
python .\scripts\vtt2json.py --file_in subtitlefile.vtt --method file
```

## Sources

- <https://www.bigdata-expo.nl/nl/programma/text-mining-steeds-belangrijker-om-goed-om-te-kunnen-gaan-met-steeds-meer>
  
  Lecture (in dutch) regarding text-mining by Prof dr ir Jan C. Scholtes.

- Applied Text Analysis with Python (ISBN: 978-1-491-96304-3)
  
  Authors: Benjamin Bengfort, Rebecca Bilbro, and Tony Ojeda

- <http://www.natalialevshina.com/Documents/Olomouc_subtitles.pdf>
  
  Discusses methods to analyse vtt subtitles
  - average word lengths
  - correlations between wordform frequencies in each register
  - Principal Component Analysis (similar to Biber's multidimensional analysis)

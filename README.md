# Conversion from markdown/HTML to TEI

This script is used to convert certain source documents into TEI XML, suitable for the [roman18 corpus](https://github.com/MiMoText/roman18). As such, it is tailored to the specific needs of the ["Mining and Modeling Text"](https://www.mimotext.uni-trier.de/) project. Possible input sources are either HTML snippets from the [Hub18thCFrench project](https://intertextual-hub.uchicago.edu/navigate/hub18thcfrench) or markdown files, which have been generated from EPUB files with the help of [Calibre](https://calibre-ebook.com/).


## Prerequisites

This script uses LXML for the XML handling, and its subproject `cssselect` for HTML parsing. You can install them with your prefered python package management tool, e.g. `pip` or `conda`:

```
pip install lxml cssselect   # or
conda install -c anaconda lxml cssselect 
```


## Usage

The script expects the source files in `.txt` and/or `.html` files at the location given in the `SOURCE_PATH` constant. It will attempt to write the resulting `.xml` files to the location given in the `SAVE_PATH` constant. If this location is not empty, it will issue a warning, but proceed to (over)write the files there. 

If you are fine with these defaults, you can simply run the script like this:

```bash
python convert.py
```


## Configuration

The runtime parameters can be modified by using command line arguments (recommended) or by overwriting the respective constants in the script itself. To list all available options just run:

```bash
python convert.py --help
```

If you e.g. want to convert only a single source file, you could run:

```bash
python convert.py -s path/to/file.txt
```

The script tries to determine the correct handling for source files from various origins, e.g. from wikisource or rousseauonline.ch. If you are just interested which dialect the auto-detection would choose without actually converting the file, you can issue the `--only-probe-dialect` option:

```bash
python convert.py -s path/to/file.txt --only-probe-dialect
```

If the auto-detection fails for some reason, you can enforce usage of a certain source dialect by specifying a `-d` / `--force-dialect` parameter:

```bash
python convert.py -s path/to/file.txt -d "WIKISOURCE"
```

However, be aware that a failing auto-detection means that some preconceptions about the input files are not met, so you are likely to encounter further issues. Available dialects are at the moment "WIKISOURCE", "WIKISOURCE_NC" (wikisource without any chapters), "ROUSSEAU", "EPUBBASE" and "HUB18CFRENCH". The latter operates on HTML, while the other dialects expect markdown which has been generated from Epub files with `Calibre`. 


## Tests

The test suite can be run by executing the following from inside the root directory:

```bash
python3 -m unittest discover
```

Failing tests are regressions and should therefore be considered as bugs.


## Known issues

- The XML build up of the main text body currently does not differentiate between different orders of headings. Every heading will result in its own chapter div element.
- The script can not differentiate between regular chapters and letters (in epistolary novels).
- The script is not able to identify trailers.
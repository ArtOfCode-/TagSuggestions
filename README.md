# TagSuggestions [![Build Status](https://travis-ci.org/ArtOfCode-/TagSuggestions.svg?branch=master)](https://travis-ci.org/ArtOfCode-/TagSuggestions)
A simple Python script for suggesting tags on Hardware Recommendations questions.

## Setup
TagSuggestions is written in Python 3, so you will need Python 3 installed. (Specifically, I wrote it in 3.4.3, if you care or need to know.)

There is one dependency: the `requests` module for Python, which can be installed using

    pip install requests

## Running

Once you're done with setup, run with the `-a` or `--all` switch:

    python main.py -a

or

    python main.py --all
    
to start suggesting tags for all past questions on the site.

If you want to get tag suggestions for specific IDs, call the program with the `-i` or `--ids` switch, and follow it with a square-bracket
enclosed, space-delimited list of IDs to suggest for. For example, to get suggestions for IDs 1040, 972 and 1036:

    python main.py -i [1040 972 1036]

or

    python main.py --ids [1040 972 1036]

Don't include spaces between the square brackets and the start or end of an ID.

If you want to change the site that the script runs for, you can use the `-s` or `--site` switch followed by the API site name:

    python main.py -s softwarerecs

or

    python main.py --site softwarerecs


The API name can usually be found as the part of the URL before `.stackexchange.com`, excluding the protocol.

## License

TagSuggestor is licensed under my usual MIT license.

You **must**:

- include the license and permission notice in copies or substantial portions

You **may**:

- use TS commercially
- distribute without restriction
- modify
- use privately
- sublicense

You **may not**:

- hold me liable if it all goes wrong

Exercise common sense and decency, and I don't bite.
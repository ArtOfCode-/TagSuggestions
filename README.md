# TagSuggestions
A simple Python script for suggesting tags on Hardware Recommendations questions.

## Setup
TagSuggestions is written in Python 3, so you will need Python 3 installed. (Specifically, I wrote it in 3.4.3, if you care or need to know.)

There is one dependency: the `requests` module for Python, which can be installed using

    pip install requests
    
Once you're done there, run

    python main.py -a
    
to start suggesting tags for all past questions on the site. There will soon be a way to suggest for specific IDs.
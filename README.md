# Overview

This project converts bibliographic data encoded in [MARC21](http://en.wikipedia.org/wiki/MARC_standards) to JSON documents ready for indexing in [Elasticsearch](https://www.elastic.co).

# Setup

## Requirements

* Python 3.7+

## Installation

Create a Python 3.7 environment:

```bash
git clone git@github.com:GovWizely/dls_reporting.git
cd dls_reporting
mkvirtualenv -p /usr/bin/python3.7 -r requirements.txt dls_reporting
``` 

# Running

```bash
python main.py /path/to/marcfile.mrc
```

# Contributing

## Run the style checker

```bash
flake8
```

## Run the linter

```bash
pylint dls_reporting
```

## Run the tests

```bash
python -m pytest
```

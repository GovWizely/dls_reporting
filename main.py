#!/usr/bin/env python
"""
Example usage: main.py /path/to/marcfile.mrc
"""
import json
import sys
from collections import Counter

from pymarc import MARCReader


def smart_merge(fields_array):
    """Converts an array of hashes into a single hash. In the event of duplicate keys, the value
    is expressed as an array.

    :param fields_array: The fields array from the MARC entry
    :return: dict representation

    """
    combined = {}
    counter = Counter()
    for entry in fields_array:
        counter[list(entry)[0]] += 1
    for entry in fields_array:
        key = list(entry)[0]
        if counter[key] > 1:
            if combined.get(key):
                combined[key].append(entry[key])
            else:
                combined[key] = [entry[key]]
        else:
            combined[key] = entry[key]
    return combined


def build_elasticsearch_doc(raw_dict):
    """Builds an Elasticsearch-ready document from a MARC record expressed as a dict.

    :param raw_dict: MARC record expressed as a dict
    :return: Document to send to Elasticsearch for indexing
    """
    bib = smart_merge(raw_dict['fields'])
    source_dict = {"type": "bib", "bib": bib}
    output_doc = {"_index": "marc",
                  "_type": "doc",
                  "_id": bib['001'],
                  "_source": source_dict}
    return output_doc


def dump(infile):
    """Reads a MARC infile and writes out consecutive JSON records

    :param infile: MARC file
    """
    with open(infile, 'rb') as file_handle:
        reader = MARCReader(file_handle)
        for record in reader:
            raw_dict = record.as_dict()
            output_doc = build_elasticsearch_doc(raw_dict)
            print(json.dumps(output_doc, indent=2))


if __name__ == '__main__':
    try:
        dump(sys.argv[1])
    except IndexError:
        print('usage: %s marc_file' % sys.argv[0])

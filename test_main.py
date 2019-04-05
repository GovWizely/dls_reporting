"""Unit tests around the MARC->Elasticsearch conversion."""
from main import build_elasticsearch_doc, smart_merge


def test_smart_merge():
    """Tests that smart_merge() converts an array of hashes as expected."""
    arr = [{"001": "9"},
           {"906": {"subfields": [{"a": "1"}, {"b": "ibc2"}], "ind1": " "}},
           {"005": "20180910155447.0"},
           {"008": "940210u198uuuuuonc          f0     eng  "},
           {"906": {"subfields": [{"a": "0"}, {"b": "ibc"}], "ind1": " "}}]
    bib = smart_merge(arr)
    assert bib == {'001': '9',
                   '906': [{'subfields': [{'a': '1'}, {'b': 'ibc2'}], 'ind1': ' '},
                           {'subfields': [{'a': '0'}, {'b': 'ibc'}], 'ind1': ' '}],
                   '005': '20180910155447.0',
                   '008': '940210u198uuuuuonc          f0     eng  '}


def test_build_elasticsearch_doc(mocker):
    """Tests that build_elasticsearch_doc() converts the MARC dict into ES-ready JSON."""
    mocker.patch("main.smart_merge", return_value={'001': '9', '005': '20180910155447.0'})
    doc = build_elasticsearch_doc({"leader": "00847cas a22001815a 4500", "fields": ["dummy"]})
    assert doc == {'_index': 'marc',
                   '_type': 'doc',
                   '_id': '9',
                   '_source': {'type': 'bib',
                               'bib': {
                                   '001': '9',
                                   '005': '20180910155447.0'}}}

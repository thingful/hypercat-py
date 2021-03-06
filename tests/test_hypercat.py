# UNITTEST.PY
# Copyright (c) 2013 Pilgrim Beart <firstname.lastname@1248.io>
#
# Simple unit-tests for hypercat.py
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from nose.tools import *
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from hypercat import hypercat

def test_empty_catalogue():
    print("Running unit tests")

    print("\nTEST: Create minimal empty Catalogue, and render to a string, minimally, then with pretty-printing")
    h = hypercat.Hypercat("")

    s = h.asJSONstr()
    print(s)
    assert_equal(s, """{"catalogue-metadata":[{"rel":"urn:X-hypercat:rels:isContentType","val":"application/vnd.hypercat.catalogue+json"},{"rel":"urn:X-hypercat:rels:hasDescription:en","val":""}],"items":[]}""")

    result = h.prettyprint()
    print(result)
    assert_equal(result, """{
    "catalogue-metadata": [
        {
            "rel": "urn:X-hypercat:rels:isContentType",
            "val": "application/vnd.hypercat.catalogue+json"
        },
        {
            "rel": "urn:X-hypercat:rels:hasDescription:en",
            "val": ""
        }
    ],
    "items": []
}""")

def test_minimal_catalogue():
    print("\nTEST: Create a catalogue containing 1 catalogue and 1 resource, held as data")
    h = hypercat.Hypercat("CatalogueContainingOneCatalogueAndOneResource")
    h2 = hypercat.Hypercat("ChildCatalogue")
    print("about to add child catalogue")
    h.addItem(h2, "http://FIXMEcat")
    r = hypercat.Resource("resource1", "application/vnd.hypercat.sensordata+json")
    print("about to add child resource")
    h.addItem(r, "http://FIXMEresource")
    result = h.asJSON()
    print(result)
    print(h.prettyprint())
    assert_equal(result, {'items': [{'item-metadata': [{'val': 'application/vnd.hypercat.catalogue+json', 'rel': 'urn:X-hypercat:rels:isContentType'}, {'val': 'ChildCatalogue', 'rel': 'urn:X-hypercat:rels:hasDescription:en'}], 'href': 'http://FIXMEcat'}, {'item-metadata': [{'val': 'application/vnd.hypercat.sensordata+json', 'rel': 'urn:X-hypercat:rels:isContentType'}, {'val': 'resource1', 'rel': 'urn:X-hypercat:rels:hasDescription:en'}], 'href': 'http://FIXMEresource'}], 'catalogue-metadata': [{'val': 'application/vnd.hypercat.catalogue+json', 'rel': 'urn:X-hypercat:rels:isContentType'}, {'val': 'CatalogueContainingOneCatalogueAndOneResource', 'rel': 'urn:X-hypercat:rels:hasDescription:en'}]})

def test_two_deep_catalogue():
    print("\nTEST: Create a catalogue 2 deep (and output each level)")
    h1 = hypercat.Hypercat("Top")
    h2 = hypercat.Hypercat("Middle")
    h3 = hypercat.Hypercat("Bottom")
    h1.addItem(h2, "http://FIXMEcat2")
    h2.addItem(h3, "http://FIXMEcat3")
    print("Top:")
    print(h1.asJSON())
    print(h1.prettyprint())
    print("Middle:")
    print(h2.asJSON())
    print(h2.prettyprint())
    print("Bottom:")
    print(h3.asJSON())
    print(h3.prettyprint())

def test_deeper_catalogue():
    print("\nTEST: Creating more than 2 levels of catalogue, then outputting different levels")
    h1 = hypercat.Hypercat("Top")
    h1.addRelation("name","top")
    h2 = hypercat.Hypercat("Middle")
    h2.addRelation("name","middle")
    h3 = hypercat.Hypercat("Bottom")
    h3.addRelation("name","bottom")
    h1.addItem(h2, "http://FIXMEcat2")
    h2.addItem(h3, "http://FIXMEcat3")

    print("Find top catalogue:")
    hN = h1.findByPath("name", "/")
    print(hN.prettyprint())
    assert_equal(hN.values("name")[0], "top")

    print("Find middle catalogue:")
    hN = h1.findByPath("name", "/middle/")
    print(hN.prettyprint())
    assert_equal(hN.values("name")[0], "middle")

    print("Find bottom catalogue:")
    hN = h1.findByPath("name", "/middle/bottom")
    print(hN.prettyprint())
    assert_equal(hN.values("name")[0], "bottom")


def test_fancy_catalogue():
    print("\nTEST: Create a fancy Catalogue with optional metadata")
    h2 = hypercat.Hypercat("Fancy Catalogue")
    h2.supportsSimpleSearch()
    h2.hasHomepage("http://www.FIXME.com")
    h2.containsContentType("application/vnd.hypercat.FIXME+json")
    result = h2.prettyprint()
    print(result)
    assert_equal(result, """{
    "catalogue-metadata": [
        {
            "rel": "urn:X-hypercat:rels:isContentType",
            "val": "application/vnd.hypercat.catalogue+json"
        },
        {
            "rel": "urn:X-hypercat:rels:hasDescription:en",
            "val": "Fancy Catalogue"
        },
        {
            "rel": "urn:X-hypercat:rels:supportsSearch",
            "val": "urn:X-hypercat:search:simple"
        },
        {
            "rel": "urn:X-hypercat:rels:hasHomepage",
            "val": "http://www.FIXME.com"
        },
        {
            "rel": "urn:X-hypercat:rels:containsContentType",
            "val": "application/vnd.hypercat.FIXME+json"
        }
    ],
    "items": []
}""")

def test_multiple_rels():
    print("\nTEST: Add multiple RELS to a catalogue")
    h = hypercat.Hypercat("cat")
    assert_equal(h.values("relation"), [])
    h.addRelation("relation","value1")
    h.addRelation("relation","value2")
    assert_equal(h.values("relation"), ["value1","value2"])
    print(h.prettyprint())

    print("\nTEST: Load a catalogue from a string")
    inString = """{
    "catalogue-metadata": [
        {
            "rel": "urn:X-hypercat:rels:isContentType",
            "val": "application/vnd.hypercat.catalogue+json"
        },
        {
            "rel": "urn:X-hypercat:rels:hasDescription:en",
            "val": "ingestiontestcat"
        }
    ],
    "items": [
        {
            "href": "http://FIXME",
            "item-metadata": [
                {
                    "rel": "urn:X-hypercat:rels:isContentType",
                    "val": "application/vnd.hypercat.catalogue+json"
                },
                {
                    "rel": "urn:X-hypercat:rels:hasDescription:en",
                    "val": "resource1"
                }
            ]
        },
        {
            "href": "http://FIXME2",
            "item-metadata": [
                {
                    "rel": "urn:X-hypercat:rels:isContentType",
                    "val": "application/vnd.hypercat.catalogue+json"
                },
                {
                    "rel": "urn:X-hypercat:rels:hasDescription:en",
                    "val": "resource2"
                }
            ]
        },
        {
            "href": "http://RESOURCEURL",
            "item-metadata": [
                {
                    "rel": "urn:X-hypercat:rels:isContentType",
                    "val": "resourcecontenttype"
                },
                {
                    "rel": "urn:X-hypercat:rels:hasDescription:en",
                    "val": "A resource"
                }
            ]
        }
    ]
}"""
    h = hypercat.loads(inString)
    outString = h.prettyprint()
    assert_equal(inString, outString)
    print(inString)

    print("\nUnit tests all passed OK")

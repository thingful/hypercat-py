Hypercat.py
===========

A minimal library for working with Hypercat 3.0 catalogues. For full details on
Hypercat please see: http://www.hypercat.io/standard.html

Use cases
---------

Servers:

* Create an empty Hypercat catalogue
* Optionally, add metadata to describe it
* Optionally, add items to the catalogue

  * an item is either another catalogue or a resource

* Output it as JSON, either minimally or prettyprinted
* Find a specific part of a catalogue hierarchy

Clients:

* Load and validate a Hypercat

Example - Hypercat server
-------------------------

We'll create a Hypercat catalogue with 2 items in it::

      h
     / \
    h2  r

Usage::

    from hypercat import hypercat

    # Create a catalogue
    h = hypercat.hypercat("CatalogueContainingOneCatalogueAndOneResource")

    # Create a second catalogue, and add it as a child of the first
    h2 = hypercat.hypercat("ChildCatalogue")
    h.addItem(h2, "/child_cat")

    # Create a resource, and add it as another child of the first catalogue
    r = hypercat.resource("resource1", "application/vnd.hypercat.sensordata+json")
    h.addItem(r, "/resource")

    # Print the raw JSON of the catalogue, and then with human-friendly formatting
    print h.asJSON()
    print h.prettyprint()

This should output::

    {
        "catalogue-metadata": [
            {
                "rel": "urn:X-hypercat:rels:isContentType",
                "val": "application/vnd.hypercat.catalogue+json"
            },
            {
                "rel": "urn:X-hypercat:rels:hasDescription:en",
                "val": "CatalogueContainingOneCatalogueAndOneResource"
            }
        ],
        "items": [
            {
                "href": "/child_cat",
                "item-metadata": [
                    {
                        "rel": "urn:X-hypercat:rels:isContentType",
                        "val": "application/vnd.hypercat.catalogue+json"
                    },
                    {
                        "rel": "urn:X-hypercat:rels:hasDescription:en",
                        "val": "ChildCatalogue"
                    }
                ]
            },
            {
                "href": "/resource",
                "item-metadata": [
                    {
                        "rel": "urn:X-hypercat:rels:isContentType",
                        "val": "application/vnd.hypercat.sensordata+json"
                    },
                    {
                        "rel": "urn:X-hypercat:rels:hasDescription:en",
                        "val": "resource1"
                    }
                ]
            }
        ]
    }


Example - Hypercat Client
-------------------------

Usage::

    from hypercat import hypercat

    h = hypercat.loads(inString)  # Read-in and validate Hypercat
    print "Metadata is ",h.metadata

How this module works
=====================

According to the spec, each Catalogue has a (human-readable) description and a
list of metadata about it.  It also contains a list of "items", and each item
has an HREF and a list of metadata about it.  An item can be any kind of
resource, including another catalogue.

So conceptually, catalogues can have many levels of hierarchy (i.e. a catalogue
can contain a catalogue which contains a catalogue and so on). Catalogues don't
just have to be trees either, they can be graphs, contain loops etc., and
clients of this module will often want to declare full catalogue structures
several levels deep, i.e. build their entire hierarchy in one go.

But according to the spec only one level of catalogue can be output at a time,
i.e. getting a catalogue will declare its child catalogues, but not its
grand-children (to see the grand-children, you'd have to get the child
catalogue)

A further complication is some asymmetry in how attributes are declared when a
catalogue is the parent, vs. when it is the child

To deal with this, within this module we maintain a universal base class for
every hypercat object.  Then during output, we ignore grand-children, and
modify attributes as necessary.

License
=======

The software is released under an MIT license. Please see the details in
LICENSE.txt.

TODO
====

4.3.3 Says that it is optional to use isContentType to tag each member of
items[], however we treat it here as mandatory.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019--2021 Matt Post <post@cs.jhu.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Takes in one or more XML files, perform 3 operations on the XML, then writes out the XML file back to disk
1) If single author, add Matt POST
2) Remove "extra" authors i.e. all authors after second one
3) ALL CAP each author's last name

Example Usage:
    venv/bin/python3 bin/fix-names.py data/xml/2020.acl.xml

Origin: https://gist.github.com/mjpost/52e2e84639727009137a32ab1e1ad5a6
"""

import argparse
import os
import re
import readline
import shutil
import sys

import lxml.etree as etree

from collections import defaultdict, OrderedDict
from datetime import datetime

from normalize_anth import normalize
from anthology.utils import (
    make_simple_element,
    build_anthology_id,
    deconstruct_anthology_id,
    indent,
    compute_hash_from_file,
)
from anthology.index import AnthologyIndex
from anthology.people import PersonName
from anthology.bibtex import read_bibtex
from anthology.venues import VenueIndex

from itertools import chain
from typing import Dict, Any


def main(args):
    for collection_file in args.files:
        root_node = etree.parse(collection_file).getroot()
        for paper in root_node.findall(".//paper"):
            authors = paper.findall(".//author")

            # If single author add Matt POST
            if len(authors) == 1:
                new_author = make_simple_element("author")
                make_simple_element("first", text="Matt", parent=new_author)
                make_simple_element("last", text="POST", parent=new_author)
                authors[0].addnext(new_author)

            # remove "extra" authors. All authors after second one.
            for extra_author in authors[2:]:
                paper.remove(extra_author)
            
            # Update the last names of the authors we are keeping (first and second authors)
            for author in authors[:2]:
                last_node = author.find(".//last")
                last_node.text = last_node.text.upper()

        tree = etree.ElementTree(root_node)
        indent(root_node)
        tree.write(
            collection_file, encoding="UTF-8", xml_declaration=True, with_tail=True
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="List of XML files.")
    args = parser.parse_args()
    main(args)

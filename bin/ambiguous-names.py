#!/usr/bin/env python3

"""
Takes a list of collection IDs as arguments, and outputs 
1) List[shared name surface string: str]
2) Dict[shared name surface string: List[IDs:str]]

Example Usage:
  venv/bin/python3 bin/ambiguous-names.py

Origin: https://gist.github.com/mjpost/c1984462bacfb4012a57520c13a08e26
"""

import os
import sys
import pprint

from anthology import Anthology
from anthology.people import PersonName
from anthology.utils import deconstruct_anthology_id


def main():
  anthology = Anthology(importdir=os.path.join(os.path.dirname(sys.argv[0]), "..", "data"))

  print("shared name surface strings")

  ambiguous_author_names_to_ids = {}

  for author, author_ids in anthology.people.name_to_ids.items():
    if len(author_ids) > 1:
      ambiguous_author_names_to_ids[str(author)] = author_ids
  
  ambiguous_author_names = list(ambiguous_author_names_to_ids.keys())
  print(f'Authors with ambiguous names: {ambiguous_author_names}')
  pprint.pprint(ambiguous_author_names_to_ids)


if __name__ == "__main__":
  main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

__version__ = "0.1.0"

__copyright__ = """
    pyObjUtils - Object file library for Python.

   (C) 2010-2016 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import bisect
import operator
import sys

from objutils.section import Section, joinSections

## TODO: diff interface!

## Adress-space constants.
AS_16   = 0
AS_24   = 1
AS_32   = 2
AS_64   = 3

class Image(object):

    def __init__(self, sections = None, meta = None, valid = False):
        if meta is None:
            meta = {}
        self.sections = sections if sections else []
        _validateSections(self.sections)
        self.meta = meta
        self.valid = valid

    def __repr__(self):
        result = []
        for segment in self.sections:
            result.append(repr(segment))
        return '\n'.join(result)

    def __len__(self):
        return len(self.sections)

    def __iter__(self):
        return iter(self.sections)

    def next(self):
        for segment in self.sections:
            yield segment

    def __eq__(self, other):
        if len(self.sections) == len(other.sections):
            return all( operator.eq(l, r) for l, r in zip(self.sections, other.sections))
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def hexdump(self, fp = sys.stdout):
        for idx, section in enumerate(self.sections):
            print("\nSection #{0:04d}".format(idx ), file = fp)
            print("-" * 13, file = fp)
            section.hexdump(fp)


class Builder(object):
    """Construct and `Image` object.
    """

    def __init__(self, sections = None, autoJoin = False, autoSort = False):
        self._sections = sections if sections else []
        _validateSections(self._sections)
        self.address = 0
        self.autoJoin = autoJoin
        self.autoSort = autoSort

    def addSegment(self, data, address = None, dontJoin = False):   # TODO: 'polymorph' signature, move 'dontJoin' to segment!
        address = address if address else self.address  # If Address omitted, create continuous address space.
        if isinstance(data, str):
            data = [ord(x) for x in data] # array.array('B',data)
        if self.autoSort:
            bisect.insort(self._sections, Section(address, data))
        else:
            self._sections.append(Section(address, data))
        if self.autoJoin:
            self.joinSections()
        self.address = address + len(data)
        
    addSection = addSegment

    def addMetaData(self, metaData):
        pass

    def joinSections(self, orderSegments = None):
        self._sections = joinSections(self._sections, orderSegments)

    def hexdump(self, fp = sys.stdout):
        self.image.hexdump(fp)

    @property
    def image(self):
        return Image(self._sections)


def _validateSections(sections):
    """Test for required protocol
    """
    ATTRIBUTES = ('address', 'length', 'data')
    if not '__iter__' in dir(sections):
        raise TypeError("Sections must be iteratable.")
    for section in sections:
        if not all( hasattr(section, attr) for attr in ATTRIBUTES):
            raise TypeError("Section '{0}' doesn't fulfills required protocol (missing attributes).")



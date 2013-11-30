#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1.0"

__copyright__ = """
    pyObjUtils - Object file library for Python.

   (C) 2010-2013 by Christoph Schueler <github.com/Christoph2,
                                        cpu12.gems@googlemail.com>

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

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import struct

from objutils.readers import PlainBinaryReader

class DwarfReader(PlainBinaryReader):

    def __init__(self, image):
        super(DwarfReader, self).__init__(StringIO.StringIO(image), DwarfReader.BIG_ENDIAN)

    def uleb(self):
        result = 0
        shift = 0
        while True:
            bval = self.nextByte()
            result |= ((bval & 0x7f) << shift)
            if bval & 0x80 == 0:
                break
            shift += 7
        return result

    def sleb(self):
        result = 0
        shift = 0
        while True:
            bval = self.nextByte()
            result |= ((bval & 0x7f) << shift)
            shift += 7
            if bval & 0x80 == 0:
                break
        if (shift < 32) or (bval & 0x40) == 0x40:
            mask = - (1 << (len(values) * 7))
            result |= mask
        return result

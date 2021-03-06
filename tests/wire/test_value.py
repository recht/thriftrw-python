# Copyright (c) 2016 Uber Technologies, Inc.
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

from __future__ import absolute_import, unicode_literals, print_function

import pytest

from thriftrw.wire import value
from thriftrw.wire import ttype
from thriftrw.wire.value import _ValueVisitorArgs


@pytest.mark.parametrize('value, visit_name, visit_args', [
    # Primitives
    (value.BoolValue(True), 'visit_bool', (True,)),
    (value.ByteValue(42), 'visit_byte', (42,)),
    (value.DoubleValue(12.34), 'visit_double', (12.34,)),
    (value.I16Value(1234), 'visit_i16', (1234,)),
    (value.I32Value(39813), 'visit_i32', (39813,)),
    (value.I64Value(198735315), 'visit_i64', (198735315,)),
    (value.BinaryValue(b'hello world'), 'visit_binary', (b'hello world',)),

    # Struct
    (value.StructValue([
        value.FieldValue(1, ttype.BOOL, value.BoolValue(True)),
        value.FieldValue(2, ttype.BYTE, value.ByteValue(42)),
    ]), 'visit_struct', ([
        value.FieldValue(1, ttype.BOOL, value.BoolValue(True)),
        value.FieldValue(2, ttype.BYTE, value.ByteValue(42)),
    ],)),

    # Map
    (value.MapValue(ttype.BINARY, ttype.I16, [
        value.MapItem(value.BinaryValue(b'Hello'), value.I16Value(1)),
        value.MapItem(value.BinaryValue(b'World'), value.I16Value(2)),
    ]), 'visit_map', (ttype.BINARY, ttype.I16, [
        value.MapItem(value.BinaryValue(b'Hello'), value.I16Value(1)),
        value.MapItem(value.BinaryValue(b'World'), value.I16Value(2)),
    ])),

    # Set
    (value.SetValue(ttype.I32, [
        value.I32Value(1234),
        value.I32Value(4567),
    ]), 'visit_set', (ttype.I32, [
        value.I32Value(1234),
        value.I32Value(4567),
    ])),

    # List
    (value.ListValue(ttype.I64, [
        value.I64Value(1380),
        value.I64Value(1479),
    ]), 'visit_list', (ttype.I64, [
        value.I64Value(1380),
        value.I64Value(1479),
    ])),
])
def test_visitors(value, visit_name, visit_args):
    """Checks that for each value type, the correct visitor is called."""

    visitor = _ValueVisitorArgs()
    result = value.apply(visitor)
    name = result[0]
    args = result[1:]

    assert visit_name == name
    assert visit_args == args


def test_struct_get():
    struct = value.StructValue([
        value.FieldValue(1, ttype.BOOL, value.BoolValue(True)),
        value.FieldValue(2, ttype.BYTE, value.ByteValue(42)),
        value.FieldValue(3, ttype.LIST, value.ListValue(
            ttype.BINARY,
            [
                value.BinaryValue(b'Hello'),
                value.BinaryValue(b'World'),
            ]
        )),
    ])

    assert struct.get(1, ttype.BOOL).value
    assert value.ByteValue(42) == struct.get(2, ttype.BYTE).value
    assert value.ListValue(ttype.BINARY, [
        value.BinaryValue(b'Hello'),
        value.BinaryValue(b'World'),
    ]) == struct.get(3, ttype.LIST).value

    assert not struct.get(1, ttype.BINARY)

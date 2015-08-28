# Copyright (c) 2015 Uber Technologies, Inc.
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

from thriftrw.loader import Loader


def test_load_from_file(tmpdir):
    tmpdir.join('my_service.thrift').write('''
        struct Foo {
            1: required string a
            2: optional string b
        }
    ''')

    my_service = Loader().load(str(tmpdir.join('my_service.thrift')))
    my_service.Foo(b='b', a='a')


def test_caching(tmpdir, monkeypatch):
    tmpdir.join('my_service.thrift').write('''
        struct Foo {
            1: required string a
            2: optional string b
        }
    ''')

    path = str(tmpdir.join('my_service.thrift'))
    loader = Loader()

    mod1 = loader.load(path)
    assert path in loader.compiled_modules

    mod2 = loader.load(path)
    assert mod1 is mod2

    mod3 = loader.load(path, force=True)
    assert mod3 is not mod2
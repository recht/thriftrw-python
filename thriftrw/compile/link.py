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

from collections import deque

from .exceptions import ThriftCompilerError


class TypeSpecLinker(object):
    """Links together references in TypeSpecs."""

    __slots__ = ('scope',)

    def __init__(self, scope):
        self.scope = scope

    def link(self):
        """Resolve and link all types in the scope."""

        # collection of types whose dependencies need to be linked.
        to_link = deque()

        # Resolve top level type references.
        for name in self.scope.type_specs.keys():
            spec = self.resolve_spec(self.scope.type_specs[name])
            self.scope.type_specs[name] = spec
            to_link.append(spec)

        visited = set()

        def _link(spec):
            spec = self.resolve_spec(spec)
            if spec not in visited:
                # Ask for this type's dependencies to be linked
                to_link.append(spec)
            return spec

        while to_link:
            spec = to_link.popleft()
            if spec in visited:
                # Already linked.
                continue
            visited.append(spec)
            spec.transform_dependencies(_link)

    def resolve_spec(self, spec):
        """Resolves a TypeReference to a Type.

        Does not resolve or link any dependencies."""

        visited = set()
        while spec.is_reference:

            if spec.name in visited:
                raise ThriftCompilerError(
                    'Type "%s" at line %d is a reference to itself.'
                    % (self.name, self.lineno)
                )

            if spec.name not in self.scope.type_specs:
                raise ThriftCompilerError(
                    'Unknown type "%s" referenced at line %d'
                    % (spec.name, spec.lineno)
                )

            visited.add(spec.name)
            spec = self.scope.type_specs[spec.name]

        return spec

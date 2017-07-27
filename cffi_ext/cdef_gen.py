from pycparser import c_generator
from typing import Container


class CDefGenerator(c_generator.CGenerator):
    class Extractor(c_generator.CGenerator):
        def __init__(self, exclude: Container[str]):
            super().__init__()
            self._exclude = exclude

        def visit_Decl(self, n, **kwargs):
            if n.name in self._exclude:
                return ''
            return super().visit_Decl(n)

        def visit_Enum(self, n):
            s = ['enum']
            if n.name:
                s.append(' ')
                s.append(n.name)
            if n.values:
                s.append(' {')
                s.append(', '.join(
                    f'{enumerator.name} = ...'
                    for _, enumerator in enumerate(n.values.enumerators)))
                s.append('}')
            return ''.join(s)

    def __init__(self, exclude: Container[str]=()):
        super().__init__()
        self._extractor = self.Extractor(exclude)

    def visit(self, node):
        if node.__class__.__name__ == 'FileAST':
            return super().visit(node)
        elif node.__class__.__name__ in ('Decl', 'Typedef'):
            return self._extractor.visit(node)
        else:
            return ''


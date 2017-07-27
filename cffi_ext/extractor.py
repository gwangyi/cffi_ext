from . import cdef_gen
from pycparserlibc import cpp, preprocess, parse
from pycparser.c_parser import CParser
from pycparser.c_generator import CGenerator
from typing import List, Union, Any, Dict, Optional


class CExprEval(CGenerator):
    def visit_Cast(self, node):
        return self.visit(node.expr)


def _cdef_macro(preprocessor: Any, parser: Any, macro_types: Optional[Dict[str, Any]]=None):
    def gen():
        pp = preprocessor
        macro_types_ = {} if not macro_types else macro_types
        for m, tp in macro_types_.items():
            if issubclass(tp, int):
                yield f'const int {m};'
            elif issubclass(tp, float):
                yield f'const double {m};'
            elif issubclass(tp, str):
                yield f'const char * const {m};'
            else:
                yield f'{str(tp)} {m};'

        for m, val in pp.macros.items():
            if not m in macro_types_ and not m.startswith('_') and val.value and val.arglist is None:
                e = ''.join(tok.value for tok in pp.expand_macros(pp.tokenize(m)))
                ast = parser.cparser.parse(input=f'int a = {e};', lexer=parser.clex, debug=0)
                expr = CExprEval().visit(ast.ext[0].init)
                expr = expr.replace("&&"," and ")
                expr = expr.replace("||"," or ")
                expr = expr.replace("!"," not ")
                try:
                    v = eval(expr)
                    
                    if isinstance(v, int):
                        yield f'const int64_t {m};'
                    elif isinstance(v, float):
                        yield f'const double {m};'
                    elif isinstance(v, str):
                        yield f'const char * const {m};'
                except Exception:
                    pass
    return '\n'.join(gen())


def cdef_extract(input: str, filename: str="", cpp_args: Union[str, List[str]] = "", fake_defs: bool = True,
        preprocessor: Any = None, parser: Any = None, fake_typedefs: bool = True):
    preprocessor = preprocessor if preprocessor else cpp.Preprocessor()
    parser = parser if parser else CParser()
    processed = preprocess(input, filename=filename, cpp_args=cpp_args, fake_defs=fake_defs,
                           preprocessor=preprocessor)
    ast = parse(processed, parser=parser, fake_typedefs=fake_typedefs)
    macro_defs = _cdef_macro(preprocessor, parser)
    return "\n".join((macro_defs, cdef_gen.CDefGenerator().visit(ast)))


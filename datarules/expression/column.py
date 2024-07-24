import ast

from uneval import quote, Expression


class ColumnExpression(Expression):
    pass


class _ColumnHelper:
    def __call__(self, name):
        return ColumnExpression(ast.Name(name))

    def __getattr__(self, name):
        return self(name)


col = _ColumnHelper()
print(repr(col.x))

import ast

class RewriteExpression(ast.NodeTransformer):
    def visit_BoolOp(self, node):
        self.generic_visit(node)
        print(0)
        print(node.op)
        match node.op:
            case ast.And():
                res = node.values[0]
                for value in node.values[1:]:
                    res = ast.BinOp(res, ast.BitAnd(), value)
                return res

                # return ast.BinOp(node.values[0], ast.BitAnd(), node.values[1])
            case ast.Or():
                # return ast.BinOp(node.values[0], ast.BitOr(), node.values[1])
                res = node.values[0]
                for value in node.values[1:]:
                    res = ast.BinOp(res, ast.BitOr(), value)
                return res

    def visit_Not(self, node):
        return ast.Invert()

    # TODO Undo operator chaining
    # TODO Turn in into '.isin'
    # def visit_Compare(self, node):
    #     self.generic_visit(node)
    #     result = node.left
    #     for op, cmp in zip(node.ops, node.comparators):
    #         result = ast.BinOp()
    #
    #
    #     if 'in' in node.ops:
    #         return

    def visit_If(self, node):
        self.generic_visit(node)
        body = node.body
        if len(body) == 1:
            [statement] = body
            return ast.BinOp(ast.UnaryOp(ast.Invert(), node.test), ast.BitOr(), statement)
        else:
            raise Exception("Multiline body is not supported.")


def rewrite_expression(string):
    parsed = ast.parse(string)
    rewritten = RewriteExpression().visit(parsed)
    ast.fix_missing_locations(rewritten)
    return ast.unparse(rewritten)


expr = "if a > 2: h==3 and d<2"
print(rewrite_expression(expr))

# expr = "if a > 2: h==3 and d<2"

expr = "width < height or width == height or width > height"
print(rewrite_expression(expr))

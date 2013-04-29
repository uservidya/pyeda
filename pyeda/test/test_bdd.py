"""
Test binary decision diagrams
"""

from pyeda.alphas import *
from pyeda.bdd import expr2bdd, bdd2expr, BDDVariable, BDDZERO, BDDONE

aa, bb, cc, dd = [BDDVariable(v.name) for v in (a, b, c, d)]

def test_expr2bdd():
    assert expr2bdd(a) == aa

    assert expr2bdd(-a * -b + a * -b + -a * b + a * b) == 1
    assert expr2bdd(-(-a * -b + a * -b + -a * b + a * b)) == 0

    f = expr2bdd(a * b + a * c + b * c)
    g = expr2bdd(a * b + a * c + b * c)

    assert f == g

    assert f.node.root == a.uniqid
    assert f.node.low.root == b.uniqid
    assert f.node.high.root == b.uniqid
    assert f.node.low.low == BDDZERO
    assert f.node.low.high.root == c.uniqid
    assert f.node.high.low.root == c.uniqid
    assert f.node.high.high == BDDONE
    assert f.node.low.high.low == BDDZERO
    assert f.node.high.low.high == BDDONE

    assert f.support == {aa, bb, cc}
    assert f.inputs == (aa, bb, cc)

def test_bdd2expr():
    f = a * b + a * c + b * c
    assert bdd2expr(expr2bdd(f)).equivalent(f)

def test_traverse():
    f = expr2bdd(a * b + a * c + b * c)
    path = [node.root for node in f.traverse()]
    # 0, 1, c, b(0, c), b(c, 1), a
    assert path == [-2, -1, 3, 2, 2, 1]

def test_equivalent():
    f = expr2bdd(a * -b + -a * b)
    g = expr2bdd((-a + -b) * (a + b))
    assert f.equivalent(f)
    assert g.equivalent(f)

def test_restrict():
    f = expr2bdd(a * b + a * c + b * c)

    assert f.restrict({aa: 0}).equivalent(expr2bdd(b * c))
    assert f.restrict({aa: 1}).equivalent(expr2bdd(b + c))
    assert f.restrict({bb: 0}).equivalent(expr2bdd(a * c))
    assert f.restrict({bb: 1}).equivalent(expr2bdd(a + c))
    assert f.restrict({cc: 0}).equivalent(expr2bdd(a * b))
    assert f.restrict({cc: 1}).equivalent(expr2bdd(a + b))

    assert f.restrict({aa: 0, bb: 0}) == 0
    assert f.restrict({aa: 0, bb: 1}) == cc
    assert f.restrict({aa: 1, bb: 0}) == cc
    assert f.restrict({aa: 1, bb: 1}) == 1

    assert f.restrict({aa: 0, cc: 0}) == 0
    assert f.restrict({aa: 0, cc: 1}) == bb
    assert f.restrict({aa: 1, cc: 0}) == bb
    assert f.restrict({aa: 1, cc: 1}) == 1

    assert f.restrict({bb: 0, cc: 0}) == 0
    assert f.restrict({bb: 0, cc: 1}) == aa
    assert f.restrict({bb: 1, cc: 0}) == aa
    assert f.restrict({bb: 1, cc: 1}) == 1

    assert f.restrict({aa: 0, bb: 0, cc: 0}) == 0
    assert f.restrict({aa: 0, bb: 0, cc: 1}) == 0
    assert f.restrict({aa: 0, bb: 1, cc: 0}) == 0
    assert f.restrict({aa: 0, bb: 1, cc: 1}) == 1
    assert f.restrict({aa: 1, bb: 0, cc: 0}) == 0
    assert f.restrict({aa: 1, bb: 0, cc: 1}) == 1
    assert f.restrict({aa: 1, bb: 1, cc: 0}) == 1
    assert f.restrict({aa: 1, bb: 1, cc: 1}) == 1

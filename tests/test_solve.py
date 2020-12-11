from mathcli import solve


def test_solve():
    solve("x - y", "x")
    solve("x = y", "x")
    solve("2x + sin(y) - sqrt(3x)", "x")
    solve("2x + sin(y) - sqrt(3x) = 2", "x")
    solve("2x + sin(y) - sqrt(3x)", "x", x=1, y=10)
    solve("x = y", "x", y=2)
    solve("x + 2y - sqrt(z)", "x", y=2, z=10)
    solve("x/0", "x")
    solve("sqrt(x) = -1", "x")
    solve("sqrt(x) = -y", "x", y=1)

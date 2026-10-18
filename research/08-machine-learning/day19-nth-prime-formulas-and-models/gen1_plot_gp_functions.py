# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day19-nth-prime-formulas-and-models/gen1_plot_gp_functions.py
# Original location      :: research/08-machine-learning/day19-nth-prime-formulas-and-models/gen1.py   (last edited 2025-08-27)
# What this script does  :: Parses and plots the functions in functions.txt (plots/).
# ----------------------------------------------------------------------------
# plot_functions.py
# Safely read function expressions from functions.txt and plot them.
# Supported funcs: add, sub, mul, div, pow, max, min, sin, cos, tan, sqrt, log, exp, abs, neg, recip, inv
# Variables: x or n

import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------- Safe primitives ----------------
EPS = 1e-12

def sdiv(a, b):
    a = np.asarray(a, dtype=float); b = np.asarray(b, dtype=float)
    out = np.full_like(a, np.nan, dtype=float)
    mask = np.abs(b) > EPS
    np.divide(a, b, out=out, where=mask)
    return out

def slog(a):
    a = np.asarray(a, dtype=float)
    aa = np.abs(a)
    out = np.zeros_like(aa, dtype=float)
    mask = aa > EPS
    np.log(aa, out=out, where=mask)
    return out

def srecip(a):
    a = np.asarray(a, dtype=float)
    out = np.zeros_like(a, dtype=float)
    mask = np.abs(a) > EPS
    np.divide(1.0, a, out=out, where=mask)
    return out

def ssqrt(a):
    a = np.asarray(a, dtype=float)
    a = np.where(np.isfinite(a), a, np.nan)
    a = np.where(a >= 0, a, np.nan)
    with np.errstate(invalid='ignore'):
        return np.sqrt(a)

def stan(a):
    a = np.asarray(a, dtype=float)
    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        y = np.tan(a)
    y = np.where(np.isfinite(y), y, np.nan)
    return np.clip(y, -1e6, 1e6)

def sexp(a):
    a = np.asarray(a, dtype=float)
    return np.exp(np.clip(a, -50, 50))

FUNCS = {
    "add": (2, lambda a, b: a + b),
    "sub": (2, lambda a, b: a - b),
    "mul": (2, lambda a, b: a * b),
    "div": (2, sdiv),
    "pow": (2, np.power),
    "max": (2, np.maximum),
    "min": (2, np.minimum),

    "sin":  (1, np.sin),
    "cos":  (1, np.cos),
    "tan":  (1, stan),
    "sqrt": (1, ssqrt),
    "log":  (1, slog),
    "exp":  (1, sexp),
    "abs":  (1, np.abs),
    "neg":  (1, lambda a: -a),
    "recip":(1, srecip),
    "inv":  (1, srecip),  # alias accepted by preprocessor anyway
}

ALLOWED_FUNCS = set(FUNCS.keys())
ALLOWED_VARS  = {"x", "n"}

# ---------------- Preprocess & validate ----------------
def preprocess(expr: str) -> str:
    """Clean common GP artifacts so the parser doesn't choke."""
    s = expr.strip()

    # balance trailing right-parens if needed
    diff = s.count('(') - s.count(')')
    if diff > 0:
        s += ')' * diff

    # alias: inv(...) -> recip(...)
    s = re.sub(r'\binv\s*\(', 'recip(', s)

    # fix number(variable) -> mul(number, variable), e.g. -0.771(n)
    num = r'([+\-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+\-]?\d+)?)'
    s = re.sub(
        rf'(?<![A-Za-z_]){num}\s*\(\s*([xXnN])\s*\)',
        lambda m: f"mul({m.group(1)}, {m.group(2).lower()})",
        s
    )

    # compress whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def validate_tokens(expr: str):
    names = set(re.findall(r'[A-Za-z_]\w*', expr))
    bad = [w for w in names if w.lower() not in (ALLOWED_FUNCS | ALLOWED_VARS)]
    if bad:
        raise ValueError(f"Unknown identifiers: {sorted(bad)}")

# ---------------- Tiny recursive parser ----------------
class Parser:
    def __init__(self, s: str):
        diff = s.count('(') - s.count(')')
        if diff > 0:
            s = s + (')' * diff)
        self.s, self.i, self.n = s, 0, len(s)

    def peek(self): return self.s[self.i] if self.i < self.n else ''
    def eat_ws(self):
        while self.i < self.n and self.s[self.i].isspace(): self.i += 1
    def expect(self, ch):
        self.eat_ws()
        if self.peek() != ch:
            raise ValueError(f"Expected '{ch}' at pos {self.i}: ...{self.s[max(0,self.i-10):self.i+10]}...")
        self.i += 1

    def parse(self):
        self.eat_ws()
        node = self.parse_expr()
        self.eat_ws()
        if self.i != self.n:
            raise ValueError(f"Unexpected trailing input at pos {self.i}: {self.s[self.i:self.i+20]}")
        return node

    def parse_expr(self):
        self.eat_ws()
        ch = self.peek()
        if ch == '': raise ValueError("Unexpected end of input")
        if ch.isalpha():
            name = self.parse_name()
            self.eat_ws()
            if self.peek() == '(':
                self.i += 1
                args = self.parse_args()
                self.expect(')')
                return ("call", name.lower(), args)
            else:
                if name.lower() in ALLOWED_VARS: return ("var",)
                raise ValueError(f"Unknown identifier '{name}' (only x/n allowed)")
        elif ch.isdigit() or ch in "+-.":
            return ("num", self.parse_number())
        elif ch == '(':
            self.i += 1
            node = self.parse_expr()
            self.expect(')')
            return node
        else:
            raise ValueError(f"Unexpected character '{ch}' at pos {self.i}")

    def parse_name(self):
        start = self.i
        while self.i < self.n and (self.s[self.i].isalnum() or self.s[self.i]=='_'):
            self.i += 1
        return self.s[start:self.i]

    def parse_number(self):
        m = re.match(r'[+\-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+\-]?\d+)?', self.s[self.i:])
        if not m: raise ValueError(f"Invalid number at pos {self.i}")
        self.i += len(m.group(0))
        return float(m.group(0))

    def parse_args(self):
        args = []
        self.eat_ws()
        if self.peek() == ')': return args
        while True:
            args.append(self.parse_expr())
            self.eat_ws()
            if self.peek() == ',':
                self.i += 1; self.eat_ws(); continue
            break
        return args

# ---------------- Evaluate AST ----------------
def eval_node(node, x):
    kind = node[0]
    if kind == "num": return np.full_like(x, node[1], dtype=float)
    if kind == "var": return x
    if kind == "call":
        name, args = node[1], node[2]
        if name not in FUNCS:
            raise ValueError(f"Unknown function '{name}'. Allowed: {', '.join(sorted(FUNCS))}")
        arity, func = FUNCS[name]
        if len(args) != arity:
            raise ValueError(f"Function '{name}' expects {arity} arg(s), got {len(args)}")
        vals = [eval_node(arg, x) for arg in args]
        return func(*vals)
    raise ValueError(f"Unknown node type: {kind}")

def compile_expr(expr: str):
    expr = preprocess(expr)
    validate_tokens(expr)
    node = Parser(expr).parse()
    def f(x):
        return eval_node(node, x)
    return f

# ---------------- Plotting ----------------
def slugify(s: str, maxlen=40):
    s = re.sub(r'\s+', '_', s.strip())
    s = re.sub(r'[^A-Za-z0-9_()+\-.,]', '', s)
    return (s[:maxlen] + '...') if len(s) > maxlen else s

def plot_expr(expr: str, x_domain=(1e-6, 10), num=1000, outdir=Path("plots")):
    outdir.mkdir(parents=True, exist_ok=True)
    f = compile_expr(expr)
    x = np.linspace(x_domain[0], x_domain[1], num)
    y = f(x)
    y = np.where(np.isfinite(y), y, np.nan)

    plt.figure(figsize=(8, 4.5))
    plt.plot(x, y)
    plt.title(expr if len(expr) < 90 else expr[:90] + "…")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True, alpha=0.3)
    filename = outdir / f"{slugify(expr)}.png"
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    return filename

def main():
    txt = Path("functions.txt")
    if not txt.exists():
        print("functions.txt not found. Put one expression per line, e.g.:")
        print("  sin(mul(x, 0.5))")
        print("  add(mul(x, x), 3)")
        print("  div(sin(x), add(1, mul(x, x)))")
        return

    lines = [ln.strip() for ln in txt.read_text(encoding="utf-8").splitlines()]
    lines = [ln for ln in lines if ln and not ln.lstrip().startswith("#")]

    if not lines:
        print("functions.txt is empty."); return

    for idx, expr in enumerate(lines, 1):
        try:
            out = plot_expr(expr)
            print(f"[{idx}] Plotted → {out}")
        except Exception as e:
            print(f"[{idx}] ERROR in expression:\n    {expr}\n    {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()

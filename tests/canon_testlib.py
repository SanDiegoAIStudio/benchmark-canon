"""Shared helpers for the test files: run the CLI in process and build small temp roots."""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
if REPO not in sys.path:
    sys.path.insert(0, REPO)

import canon  # noqa: E402  (imported from the repo folder that holds the tests)

REAL_DATA_DIRS = ("data", "evidence", "memos")


def run(args, root=None, stdin=None):
    """Run canon.main in process; return (exit code, stdout, stderr)."""
    argv = list(args)
    if root is not None:
        argv = ["--root", root] + argv
    out, err = io.StringIO(), io.StringIO()
    old_stdin = sys.stdin
    if stdin is not None:
        sys.stdin = io.StringIO(stdin)
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = canon.main(argv)
            except SystemExit as exc:
                code = exc.code
    finally:
        sys.stdin = old_stdin
    return code, out.getvalue(), err.getvalue()


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def load_json(root, rel):
    return json.loads(read(os.path.join(root, rel)))


def save_json(root, rel, obj):
    write(os.path.join(root, rel), json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def edit_json(root, rel, fn):
    obj = load_json(root, rel)
    fn(obj)
    save_json(root, rel, obj)


def real_rows():
    return load_json(REPO, "data/verdicts.json")["benchmarks"]


def real_canon():
    return load_json(REPO, "data/canon.json")


def copy_real_root(parent):
    """A copy of the data, evidence and memo folders in a new folder under parent."""
    dest = os.path.join(parent, "realcopy")
    for name in REAL_DATA_DIRS:
        shutil.copytree(os.path.join(REPO, name), os.path.join(dest, name))
    return dest


MINI_ROWS = [
    {"id": "one", "name": "Alpha One", "cat": "alpha", "verdict": "caveat",
     "url": "https://example.org/one", "caveat": "first caveat", "aliases": ["A1"]},
    {"id": "two", "name": "Alpha Two", "cat": "alpha", "verdict": "cut",
     "url": "https://example.org/two", "caveat": "second caveat", "aliases": []},
    {"id": "alpha-base", "name": "Alpha", "cat": "alpha", "verdict": "caveat",
     "url": "https://example.org/base", "caveat": "base caveat", "aliases": []},
    {"id": "three", "name": "Beta Three", "cat": "beta", "verdict": "caveat",
     "url": "https://example.org/three", "caveat": "third caveat", "aliases": []},
]


def make_mini(parent, rows=None, checked="2026-08-31"):
    """Write a small valid root: two categories, alpha re-checked after 3 months."""
    rows = [dict(r, round="main") for r in (rows if rows is not None else MINI_ROWS)]
    root = os.path.join(parent, "mini")
    cats = []
    for row in rows:
        if row["cat"] not in cats:
            cats.append(row["cat"])
    save_json(root, "data/verdicts.json", {"checked": checked, "benchmarks": rows})
    primaries = []
    for cat in cats:
        pick = [r for r in rows if r["cat"] == cat and r["verdict"] != "cut"][0]
        primaries.append({"cat": cat, "pick": pick["name"], "pick_id": pick["id"], "rule": "rule for " + cat})
    save_json(root, "data/canon.json", {
        "asof": checked,
        "note": "mini note",
        "produced_by": "mini maker",
        "primaries": primaries,
        "rules": ["first rule", "second rule"],
        "voids": ["a void"],
        "curators": [{"who": "Someone", "note": "a note"}],
        "labels": dict((c, c.capitalize()) for c in cats),
        "revet_months": {"alpha": 3, "default": 6},
    })
    for row in rows:
        write(os.path.join(root, "evidence", row["id"] + ".md"),
              "Some findings.\n\nVERDICT: %s | %s | %s\n" % (row["verdict"], row["name"], row["caveat"]))
    for prim in primaries:
        write(os.path.join(root, "memos", prim["cat"] + ".md"),
              "A memo.\n\nPRIMARY: %s\n" % prim["pick"])
    return root


class TempDirMixin(object):
    """Gives a test a fresh temp folder that is removed afterwards."""

    def make_tmp(self):
        path = tempfile.mkdtemp(prefix="canon-test-")
        self.addCleanup(shutil.rmtree, path, True)
        return path

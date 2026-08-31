import inspect, sys


def is_jupyterlite():
    return "pyodide" in sys.modules


def whitebox_class():
    from whitebox.whitebox_tools import WhiteboxTools
    return WhiteboxTools


def api_search(keywords=(), limit=40):
    cls = whitebox_class()
    words = [w.lower() for w in keywords]
    rows = []
    for name, fn in inspect.getmembers(cls, inspect.isfunction):
        if name.startswith("_"):
            continue
        doc = inspect.getdoc(fn) or ""
        haystack = (name + " " + doc).lower()
        if not words or any(w in haystack for w in words):
            try:
                sig = str(inspect.signature(fn))
            except Exception:
                sig = "(...)"
            rows.append((name, sig, doc.splitlines()[0] if doc else ""))
    return rows[:limit]


def show_tools(keywords=(), limit=40):
    rows = api_search(keywords, limit)
    if not rows:
        print("No matching Python wrapper methods found.")
        return rows
    for name, sig, summary in rows:
        print(f"{name}{sig}\n    {summary}")
    return rows


def native_message():
    if is_jupyterlite():
        print("JupyterLite detected: API discovery works here; native WhiteboxTools execution is intentionally skipped.")
    else:
        print("Standard Python kernel detected: native WhiteboxTools calls can run after `import whitebox; wbt = whitebox.WhiteboxTools()`. ")

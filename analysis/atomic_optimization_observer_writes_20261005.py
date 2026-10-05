"""Atomic operational JSON writes without modifying any frozen producer or fitter."""
from pathlib import Path
from contextlib import contextmanager
import ast,importlib,json,os,time
ROOT=Path(__file__).resolve().parents[1]
def write(path,value):
    path=Path(path).resolve();assert path.is_relative_to(ROOT/'analysis') and path.suffix=='.json'
    data=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    temporary=path.with_name(path.name+f'.observer-{os.getpid()}.tmp')
    temporary.write_bytes(data)
    for attempt in range(500):
        try:os.replace(temporary,path);return
        except OSError as error:
            if error.errno not in (13,22) and getattr(error,'winerror',None) not in (32,33):raise
            if attempt==499:raise
            time.sleep(.1)
@contextmanager
def operational_writes(*roots):
    names=set();pending=list(roots)
    while pending:
        name=pending.pop()
        if name in names:continue
        assert name.startswith('refresh_')
        names.add(name);source=ROOT/'analysis'/f'{name}.py'
        for node in ast.walk(ast.parse(source.read_text(encoding='utf-8'))):
            modules=[alias.name for alias in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) else []
            pending.extend(item for item in modules if item and item.startswith('refresh_') and (ROOT/'analysis'/f'{item}.py').exists())
    bindings=[]
    try:
        for name in sorted(names):
            module=importlib.import_module(name)
            if callable(getattr(module,'write',None)):
                original=module.write;module.write=write;bindings.append((module,original))
        yield
    finally:
        for module,original in reversed(bindings):module.write=original

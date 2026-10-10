"""Discover and pin project import and literal backend sources before151 quality; never import them for inference."""
from pathlib import Path
import sys,time,ast,importlib.metadata as metadata
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def locate(module,source=None,level=0):
    relative=Path(*module.split('.')) if module else Path()
    bases=[ROOT,A,A/'connected_validation_20261002',ROOT/'src']
    if level and source is not None:bases=[source.parent.parents[level-2] if level>1 else source.parent]
    for base in bases:
        p=base/relative
        for candidate in (p.with_suffix('.py'),p/'__init__.py'):
            if candidate.is_file() and candidate.is_relative_to(ROOT):return candidate
    return None

def main():
    import prepare_RFFSparse59_round151_sources_v1_20261009 as generator
    prospective=A/'RFFSparse59_prospective_routes_v1_20261009.json';proof=read(prospective)
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    seeds=[p for p in generator.source_paths() if p.is_file() and p.suffix=='.py']
    abi_path=A/'RFFSparse151_complete_native_predictor_preparation_v1_20261009.json';abi=read(abi_path)
    seeds.extend(Path(p) for p in abi['input_sha256'] if Path(p).suffix=='.py')
    trees=[(A/name,ast.parse(text)) for textset in (generator.generate(p) for p in (147,148,149,150)) for name,text in textset.items()]
    pending=list(dict.fromkeys(seeds));seen={};edges=[];unresolved=set();literal_sources=[]
    while pending or trees:
        if pending:
            source=pending.pop()
            if source in seen:continue
            text=source.read_text(encoding='utf8');tree=ast.parse(text);compile(text,str(source),'exec');seen[source]=sha(source)
        else:source,tree=trees.pop()
        for node in ast.walk(tree):
            modules=[]
            if isinstance(node,ast.Import):modules=[(a.name,0) for a in node.names]
            elif isinstance(node,ast.ImportFrom):
                modules=[(node.module or '',node.level)]+[((node.module+'.' if node.module else '')+a.name,node.level) for a in node.names if a.name!='*']
            for module,level in modules:
                target=locate(module,source,level)
                if target is not None:
                    edges.append({'source':str(source),'module':module,'project_target':str(target)})
                    if target not in seen:pending.append(target)
                elif level==0 and module:unresolved.add(module.split('.')[0])
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.endswith('.py'):
                textpath=Path(node.value)
                candidates=[ROOT/textpath,A/textpath,source.parent/textpath]
                for p in candidates:
                    if p.is_file() and p.is_relative_to(ROOT):
                        literal_sources.append({'source':str(source),'literal':node.value,'project_target':str(p)})
                        if p not in seen:pending.append(p)
                        break
        assert len(seen)<=2500,'Unbounded project closure is not admitted.'
    packages={}
    for name in ('numpy','pandas','polars','scipy','scikit-learn','torch','lightgbm','xgboost','joblib','threadpoolctl','psutil'):
        try:packages[name]=metadata.version(name)
        except metadata.PackageNotFoundError:packages[name]=None
    create(A/'RFFSparse151_project_source_closure_v1_20261009.json',{'status':'passed_actual_project_import_literal_backend_and_generated_source_dependency_closure_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{**{str(p):d for p,d in seen.items()},str(Path(__file__)):sha(__file__),str(prospective):sha(prospective),str(abi_path):sha(abi_path)},
        'project_source_count':len(seen),'project_import_edges':edges,'literal_backend_sources':literal_sources,'nonproject_or_future_module_names':sorted(unresolved),
        'installed_numerical_package_versions':packages,'python_version':sys.version,'generated_future_canonical_modules_not_materialized':True,
        'no_inference_or_training_modules_executed_by_dependency_scan':True,'new_quality_scores':0,'new_future_inference':0,'new_native_fits':0,'test_labels_read':False})
    print({'project_sources':len(seen),'import_edges':len(edges),'literal_sources':len(literal_sources),'new_quality_scores':0},flush=True)
if __name__=='__main__':main()

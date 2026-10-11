"""Check tuple/dynamic data filenames as well as direct paths and Python imports in all24 receivers."""
from pathlib import Path
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import bind_future_import_namespaces_v38_20261009 as current
    import verify_future_service_and_data_namespaces_v22_20261009 as previous
    import bind_future151to153_serial_receivers_v21_20261009 as original
    current.BASE_ROUTE=previous.routed;previous.ORIGINAL_ROUTE=original.route
    meta=read(current.META);records=[];inputs=[Path(__file__),Path(current.__file__),current.META]
    for number,drivers in meta['drivers'].items():
        for name in drivers:
            p=A/name;before=p.read_text(encoding='utf8');after=current.routed(int(number),before)
            compile(after,str(p),'exec')
            modules=lambda s:[x.module for x in ast.walk(ast.parse(s)) if isinstance(x,ast.ImportFrom)]
            assert modules(before)==modules(after)
            files=lambda s:[x.value for x in ast.walk(ast.parse(s)) if isinstance(x,ast.Constant) and isinstance(x.value,str)
                and x.value.endswith(('.py','.json')) and 'service_owned_workflows' not in x.value
                and x.value not in ('BF16Medium153_complete_pipeline_preparation_v17_20261009.json','future151to153_serial_receiver_binding_v21_20261009.json')]
            assert files(before)==files(after),(name,files(before),files(after))
            records.append({'round':int(number),'source':name,'all_original_imports_exact':True,
                'direct_and_tuple_and_dynamic_Python_JSON_artifact_literals_exact':True,'original_file_literal_count':len(files(before))})
            inputs.extend((p,A/drivers[name]))
    create(A/'future_all_file_literal_namespaces_v39_20261009.json',{'status':'passed24_actual_import_and_all_nonservice_Python_JSON_literal_contracts',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},'records':records,
        'actual151_source_admission_service':'RFFSparse59_round151_source_admission_v3_20261009','canonical151_duplicate_artifact_version':1,
        'current151_duplicate_service_version':9,'new_scientific_math':False,'new_scores':0,'test_labels_read':False})
    print({'actual_typed_receivers':len(records),'all_Python_JSON_literals_exact':True})
if __name__=='__main__':main()

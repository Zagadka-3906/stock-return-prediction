"""Actually compile every prospective route and check all administrative record-count guards."""
from pathlib import Path
import ast,sys,time,importlib,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    entries=[(132,40,'nonflag_ReverseBayes40','prepare_nonflag_ReverseBayes40_round132_sources_v1_20261007')]
    results=[];sources=[Path(__file__)];issues=[]
    for number,expected,family,module_name in entries:
        module=importlib.import_module(module_name);plan=A/f'{family}_plan_20261007.json';sources.extend([Path(module.__file__),plan]);data=read(plan)
        assert data['expected_scored_records']==expected
        for parent in data['qualified_anchor_rounds']:
            generated=module.generate(parent);checks=[]
            for name,text in generated.items():
                tree=ast.parse(text);compile(tree,str(A/name),'exec')
                for node in ast.walk(tree):
                    if isinstance(node,ast.Compare) and any(isinstance(x,ast.Constant) and isinstance(x.value,int) for x in node.comparators):
                        expr=ast.unparse(node)
                        if any(x in expr for x in ["len(pilot['records'])", "record['expected_scored_records']", "len(record['ranking'])", "manifest['scored_records'] == full['scored_records']"]):
                            values=[x.value for x in node.comparators if isinstance(x,ast.Constant)]
                            if values!=[expected]:issues.append({'round':number,'parent':parent,'source':name,'guard':expr,'expected':expected})
                            checks.append({'source':name,'guard':expr,'actual_record_count':values})
                    if isinstance(node,ast.Dict):
                        for key,value in zip(node.keys,node.values):
                            if isinstance(key,ast.Constant) and key.value in {'expected_scored_records','existing_actual_official_records','scored_records','original_official_pilot_records_registered'} and isinstance(value,ast.Constant) and isinstance(value.value,int):
                                if value.value!=expected:issues.append({'round':number,'parent':parent,'source':name,'field':key.value,'value':value.value,'expected':expected})
                                checks.append({'source':name,'field':key.value,'actual_record_count':value.value})
            assert len(generated)==8 and len(checks)>=8
            results.append({'round':number,'parent':parent,'expected_scored_records':expected,'actually_compiled_sources':8,'count_controls':checks,
              'generated_source_sha256':{n:hashlib.sha256(t.encode('utf8')).hexdigest() for n,t in generated.items()}})
    create(A/'future132_administrative_count_routes_actual_20261007.json',{
      'status':'passed_actual24_prospective_sources_all_administrative_record_counts' if not issues else 'failed_actual_prospective_count_guards_preserved',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'issues':issues,'controls':results,'input_sha256':{str(p):sha(p) for p in sources},
      'new_quality_scores':0,'test_labels_read':False})
    print({'status':'passed' if not issues else 'failed','actual_compiled_sources':24,'issues':issues},flush=True);assert not issues

if __name__=='__main__':main()

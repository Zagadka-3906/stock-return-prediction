"""Execute producer path expressions and match all actual consumer and generated registry paths."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def expressions(text,name):
    return [node.value for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id==name for target in node.targets)]


def evaluate(node,**context):
    return eval(compile(ast.Expression(body=node),'<actual_output_path>','eval'),{'__builtins__':{},'A':A,'ROOT':ROOT,**context})


def strings(text):
    return [node.value for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Constant) and isinstance(node.value,str)]


def main():
    import prepare_BF16wide40_round135_sources_v4_20261008 as generator
    paths={name:A/(name+'_v4_20261008.py') for name in ('run_BF16wide40_official_comparison','prepare_BF16wide40_selected_candidate',
        'seal_BF16wide40_selected_candidate','run_BF16wide40_round135_full_registration','publish_BF16wide40_evidence','verify_BF16wide40_round135_sources',
        'queue_BF16wide135_complete_pipeline')}
    texts={name:path.read_text(encoding='utf8') for name,path in paths.items()};controls=[]
    scoring=evaluate(expressions(texts['run_BF16wide40_official_comparison'],'OUT')[0])
    release=evaluate(expressions(texts['prepare_BF16wide40_selected_candidate'],'OUT')[0])
    assert scoring==A/'BF16wide40_official_comparison_v1_20261008' and release==A/'BF16wide40_selected_release_v1_20261008'
    publisher=expressions(texts['publish_BF16wide40_evidence'],'out');assert len(publisher)==1
    for phase,consumer in (('controls','run_BF16wide40_official_comparison'),('scores','prepare_BF16wide40_selected_candidate')):
        produced=evaluate(publisher[0],phase=phase);expected=A/f'BF16wide40_{phase}_github_v1_20261008'
        assert produced==expected
        assert (expected.name+'/receipt.json') in strings(texts[consumer])
        controls.append({'producer':'publish_BF16wide40_evidence_v4_20261008','phase':phase,'executed_output_path':str(produced),'consumer':consumer,'exact_receipt_path_matched':True})
    assert 'BF16wide40_official_comparison_v1_20261008' in strings(texts['publish_BF16wide40_evidence'])
    assert 'BF16wide40_official_comparison_v1_20261008/verification.json' in strings(texts['prepare_BF16wide40_selected_candidate'])
    assert 'BF16wide40_selected_release_v1_20261008' in strings(texts['seal_BF16wide40_selected_candidate'])
    expected_receipt=A/'BF16wide40_scores_github_v1_20261008/receipt.json';assert expected_receipt in generator.source_paths()
    for parent in (112,133,134):
        generated=generator.generate(parent);assert len(generated)==8
        for name,text in generated.items():
            compile(text,str(A/name),'exec')
            # A data output's version cannot be inferred from its driver's service version.
            values=strings(text)
            assert not any('github_v3_20261008/receipt.json' in value or 'github_v4_20261008/receipt.json' in value for value in values),name
            assert not any(value.startswith('BF16wide40_official_comparison_v4_20261008/') for value in values),name
            if name.startswith('register_'):
                assert 'BF16wide40_official_comparison_v1_20261008/verification.json' in values
            if name.startswith('publish_'):
                assert 'BF16wide40_official_comparison_v1_20261008' in values
            controls.append({'comparison_parent':parent,'generated_receiver':name,'physical_data_and_receipt_paths_matched':True})
    repair=A/'actual_BF16wide135_producer_consumer_recovery_v6_20261008.json'
    assert read(repair)['actual_retired_lazy_waiters']==8
    sources=[Path(__file__),Path(generator.__file__),repair,*paths.values()]
    create(A/'BF16wide135_actual_output_contract_v4_20261008.json',{'status':'passed_actual135_producer_consumer_output_paths_for_all24_generated_receivers',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},'controls':controls,
        'generated_receivers_checked':24,'actual_producer_expressions_executed':4,'physical_output_version':1,'driver_service_version':4,
        'actual_scoring_and_future_X_not_yet_executed':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('Actual4 producer paths and24 generated consumers match true physical version1 data/receipt outputs.',flush=True)


if __name__=='__main__':main()

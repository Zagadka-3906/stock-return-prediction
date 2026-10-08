"""Follow each sealed registration alias to its original full scientific protocol."""
from pathlib import Path
from copy import deepcopy
from run_dependency_queue_v3_20261006 import read,sha
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'

def resolve(candidate,release,graph,runtime):
    candidate,release=Path(candidate),Path(release);evidence=[];visited=set();protocol=None;protocol_path=None
    origin_graph=read(candidate/'verification.json')['whole_scheme_graph']
    while True:
        assert candidate.resolve() not in visited,candidate;visited.add(candidate.resolve())
        path=release/'protocol.json'
        if path.is_file():
            evidence.append(path);value=read(path)
            if {'future_native_model_sources','future_root_model_sources'}<=value.keys():
                protocol,protocol_path=value,path;break
        matches=[]
        for ready_path in A.glob('*/selected_candidate_ready_for_registration.json'):
            ready=read(ready_path)
            if ready.get('source_candidate')==str(candidate):
                physical_release=Path(ready.get('original_source_release',ready['source_release']))
                path=physical_release/'protocol.json'
                if path.is_file() and {'future_native_model_sources','future_root_model_sources'}<=read(path).keys():
                    matches.append((path,ready_path))
        if matches:
            protocol_path,ready_path=sorted(matches,key=lambda pair:str(pair[0]))[0]
            protocol=read(protocol_path);evidence += [protocol_path,ready_path];break
        alias_path=candidate/'registry_alias_verification.json';alias=read(alias_path)
        original=Path(alias['source_candidate']);manifest=original/'manifest.json';selection_path=candidate/'selection.json';selection=read(selection_path)
        original_selection=original/'selection.json'
        assert sha(manifest)==alias['source_manifest_sha256']
        assert Path(selection['original_frozen_selection_source'])==original_selection
        assert sha(original_selection)==selection['original_frozen_selection_sha256']
        assert read(manifest)['files']['selection.json']['sha256']==sha(original_selection)
        assert read(original/'verification.json')['whole_scheme_graph']==origin_graph
        evidence += [alias_path,manifest,selection_path,original_selection]
        candidate=original;release=A/original.name
    native=runtime.future_native_sources(graph);roots=runtime.root_model_sources(graph)
    for field,actual in [('future_native_model_sources',native),('future_root_model_sources',roots)]:
        for name,info in actual.items():
            assert info['sha256']==protocol[field][name]['sha256'],(field,name)
            assert sha(info['path'])==info['sha256'],(field,name)
    pins={str(path):sha(path) for path in evidence}
    return deepcopy(protocol),pins,{'status':'passed_recursive_sealed_scientific_protocol_core_sources_before_future_features',
      'scientific_protocol_source':str(protocol_path),'input_sha256':pins,'actual_candidate_alias_hops':len(visited)-1,
      'actual_core_native_sources':len(native),'actual_root_sources':len(roots),'new_native_fits':0,'test_labels_read':False}

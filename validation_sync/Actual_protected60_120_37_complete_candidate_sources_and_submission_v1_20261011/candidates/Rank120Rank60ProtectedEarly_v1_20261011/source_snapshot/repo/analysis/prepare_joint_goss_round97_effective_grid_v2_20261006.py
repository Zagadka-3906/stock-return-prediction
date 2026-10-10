"""Preserve the prototype and make disabled top/rest controls explicit."""
from pathlib import Path
import json
import hashlib

A = Path(__file__).resolve().parent

def main():
    old=A/'joint_goss_membership_retention_grid_20261006.py'
    new=A/'joint_goss_membership_retention_grid_v2_20261006.py'
    text=old.read_text(encoding='utf-8')
    before="            for role, enabled in (('top', top), ('rest', rest)):\n                if enabled:\n                    ns.node(cfg)['specs'][role] = deepcopy(top_rest_specs[role])"
    after="            for role, enabled in (('top', top), ('rest', rest)):\n                ns.node(cfg)['specs'][role] = (deepcopy(top_rest_specs[role])\n                    if enabled else {'model': 'none', 'weight': 0.})"
    assert text.count(before)==1
    with new.open('x',encoding='utf-8',newline='\n') as f:f.write(text.replace(before,after))
    for name in ('joint_goss_membership_search_engine_v1_20261006.py','predict_joint_goss_membership_scheme_v1_20261006.py'):
        p=A/name;text=p.read_text(encoding='utf-8')
        assert 'joint_goss_membership_retention_grid_20261006' in text
        text=text.replace('joint_goss_membership_retention_grid_20261006','joint_goss_membership_retention_grid_v2_20261006')
        if name.startswith('joint_goss_membership_search'):
            text=text.replace('joint_membership_retention_scope_20261006/planned_round97.json','joint_membership_retention_scope_20261006/planned_round97_v2.json')
        p.write_text(text,encoding='utf-8',newline='\n')
    plan=A/'joint_membership_retention_scope_20261006/planned_round97.json'
    value=json.loads(plan.read_text(encoding='utf-8'))
    value.update(effective_grid_source=str(new),
        inherited_top_and_rest_disabled_explicitly_for_each_false_combination=True,
        earlier_plan_and_grid_preserved=True, original_plan=str(plan))
    with new.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    value['source_sha256'][str(new)]=digest
    with (plan.parent/'planned_round97_v2.json').open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
    print('Preserved original grid; round97 uses explicit off/on role combinations.',flush=True)

if __name__=='__main__':main()

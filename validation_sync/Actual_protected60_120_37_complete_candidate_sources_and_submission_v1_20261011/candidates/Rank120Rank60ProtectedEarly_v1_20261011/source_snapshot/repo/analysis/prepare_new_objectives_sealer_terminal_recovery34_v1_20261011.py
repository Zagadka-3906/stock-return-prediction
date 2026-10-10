from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read
def main():
 old=A/'prepare_new_objectives_reboot_publication_recovery33_v1_20261011.py';new=A/'prepare_new_objectives_all_publication_and_sealing_recovery34_v1_20261011.py';assert not new.exists()
 s=old.read_text(encoding='utf8').replace('recovery33','recovery34').replace('recovery32','recovery33')
 # Full-registration overrides already exist as frozen33; derive fresh34 files from originals.
 needle=" aliases={k:v.replace('recovery33_','recovery34_')"
 assert needle in s
 insert=""" for name in data['source_factories']:
  m=__import__(name)
  for filename in m.EXTRAS:
   if not filename.startswith('seal_') or not filename.endswith('.py'):continue
   p=A/filename;original=p.read_text(encoding='utf8');lines=original.splitlines();matched=[x for x in lines if x.strip().startswith(\"service=A/'service_owned_workflows_20261006/\")];assert len(matched)==1
   line=matched[0];canonical=line.split('service_owned_workflows_20261006/')[1].rstrip(\"'\");actual=data['service_aliases'][canonical].replace('recovery33_','recovery34_')
   text=original.replace(line,line.replace(canonical,actual));assert 'closed(service.name)' in text
   q=save(A/(p.stem+'_actual_sealer_identity_recovery34.py'),text);overrides[filename]=q.name;paths.extend([p,q])
"""
 s=s.replace(needle,insert+needle,1);compile(s,str(new),'exec');new.write_text(s,encoding='utf8',newline='\n')
 import runpy;runpy.run_path(str(new),run_name='__main__')
if __name__=='__main__':main()

"""Use the actual85 controls list in the existing prospective source harness."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]

def main():
    source=A/'verify_flagged_HGB88_round116_sources_20261007.py'
    text=source.read_text(encoding='utf8')
    before="assert hook['actual_full5635800_controls']==85"
    assert text.count(before)==1
    text=text.replace(before,"assert len(hook['controls'])==85")
    namespace={'__file__':str(Path(__file__)),'__name__':'prospective116_admission_v2'}
    exec(compile(text,str(source),'exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()

"""Remove two whole administrative wait lines without changing loop indentation."""
from pathlib import Path
import runpy
def main():
    a=Path(__file__).resolve().parent
    source=a/'admit_Top10_early171_independent42_and_receipt62_v3_20261010.py'
    text=source.read_text(encoding='utf8')
    old="text.replace(gate,'')"
    assert text.count(old)==1
    text=text.replace(old,"''.join(line for line in text.splitlines(keepends=True) if line.strip()!=gate.strip())")
    driver=a/'admit_Top10_early171_independent42_and_receipt62_v4_20261010.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()

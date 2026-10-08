"""Bounded native whitespace formatting with CPython scalar spellings preserved."""
import json
import os
import msgspec

def native_block(value, depth):
    compact=json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':'))
    pretty=msgspec.json.format(compact,indent=2)
    assert isinstance(pretty,str)
    if depth:pretty=pretty.replace('\n','\n'+'  '*depth)
    return pretty.replace('\n',os.linesep).encode('utf8')

def pieces(report):
    """Stream the large top-level lists one row at a time; preserve insertion order."""
    assert isinstance(report,dict)
    if not report:
        yield b'{}'+os.linesep.encode('ascii');return
    newline=os.linesep.encode('ascii')
    yield b'{'+newline
    keys=list(report)
    for index,key in enumerate(keys):
        value=report[key]
        yield b'  '+json.dumps(key,ensure_ascii=False,allow_nan=False).encode('utf8')+b': '
        if isinstance(value,list) and value:
            yield b'['+newline
            for j,row in enumerate(value):
                yield b'    '+native_block(row,2)
                yield (b',' if j<len(value)-1 else b'')+newline
            yield b'  ]'
        else:yield native_block(value,1)
        yield (b',' if index<len(keys)-1 else b'')+newline
    yield b'}'+newline

if __name__=='__main__':
    values=[{},[],{'中文':'引号"\\换行\n','floats':[0.0,-0.0,1e-7,1e20,1e21,1.2345678901234567],'nested':[{},[],None,True,False]},[1,2,{},[]]]
    for value in values:
        expected=json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2).replace('\n',os.linesep).encode('utf8')
        assert native_block(value,0)==expected
    for report in [{}, {'a':values,'b':{'nested':values}}, {'empty':[],'a':'\r\n'}]:
        expected=(json.dumps(report,ensure_ascii=False,allow_nan=False,indent=2)+'\n').replace('\n',os.linesep).encode('utf8')
        assert b''.join(pieces(report))==expected
    print({'status':'passed','msgspec_version':msgspec.__version__,'scalar_and_nested_reports':7})

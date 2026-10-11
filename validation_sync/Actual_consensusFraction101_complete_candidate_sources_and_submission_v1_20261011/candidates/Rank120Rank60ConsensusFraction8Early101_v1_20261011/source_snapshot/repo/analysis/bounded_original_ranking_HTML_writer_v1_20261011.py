"""Stream the original ranking PAGE with exactly the original compact JSON and substitutions."""
import json,os

def compact_pieces(report):
    assert type(report) is dict
    yield '{'
    for i,(key,value) in enumerate(report.items()):
        if i:yield ','
        yield json.dumps(key,ensure_ascii=False,allow_nan=False,separators=(',',':'))
        yield ':'
        if type(value) is list:
            yield '['
            for j,row in enumerate(value):
                if j:yield ','
                yield json.dumps(row,ensure_ascii=False,allow_nan=False,separators=(',',':'))
            yield ']'
        else:yield json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':'))
    yield '}'

def html_pieces(page,report,banner,stamp,valid_best,count,reference=False):
    assert page.count('__DATA__')==1
    before,after=page.split('__DATA__')
    substitutions=[('__PROVENANCE_BANNER__',banner),('__REPORT_DATE__',stamp),('__VALIDATION_BEST__',f'{valid_best:.9f}'),('__CONNECTED_COUNT__',f'{count:,}')]
    def render(part):
        for marker,value in substitutions:part=part.replace(marker,value)
        return part.replace('\n',os.linesep).encode('utf-8')
    yield render(before)
    pieces=json.JSONEncoder(ensure_ascii=False,allow_nan=False,separators=(',',':')).iterencode(report) if reference else compact_pieces(report)
    for piece in pieces:yield render(piece.replace('</','<\\/'))
    yield render(after)

def write(path,page,report,banner,stamp,valid_best,count):
    with path.open('wb') as stream:
        for piece in html_pieces(page,report,banner,stamp,valid_best,count):stream.write(piece)

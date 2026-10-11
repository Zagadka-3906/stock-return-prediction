"""Candidate packer: consult already interned long strings before re-encoding their chunks."""
def pack_report(report):
    nodes,lookup=[],{}
    def encode(value):
        if isinstance(value,dict):
            items=tuple((key,encode(child)) for key,child in value.items())
            key,node=('object',items),[2,items]
        elif isinstance(value,list):
            items=tuple(encode(child) for child in value)
            key,node=('array',items),[1,items]
        elif isinstance(value,str) and len(value)>512:
            key=('long_string',value)
            if key in lookup:return lookup[key]
            items=tuple(encode(value[offset:offset+256]) for offset in range(0,len(value),256))
            node=[3,items]
        else:
            assert value is None or isinstance(value,(str,int,float,bool))
            key,node=(type(value).__name__,value),[0,value]
        if key not in lookup:
            lookup[key]=len(nodes);nodes.append(node)
        return lookup[key]
    root=encode(report)
    return {'codec':'typed_shared_nodes_and256_character_string_chunks_v1','root':root,'nodes':nodes}

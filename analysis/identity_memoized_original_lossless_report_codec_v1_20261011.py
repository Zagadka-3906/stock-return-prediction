"""Preserve the original codec node order and value keys; memoize stable input containers."""
def pack_report(report):
    nodes,lookup,memo=[],{},{}
    def encode(value):
        container=isinstance(value,(dict,list))
        if container and id(value) in memo:return memo[id(value)]
        if isinstance(value,dict):
            items=tuple((key,encode(child)) for key,child in value.items())
            key,node=('object',items),[2,items]
        elif isinstance(value,list):
            items=tuple(encode(child) for child in value)
            key,node=('array',items),[1,items]
        elif isinstance(value,str) and len(value)>512:
            items=tuple(encode(value[offset:offset+256]) for offset in range(0,len(value),256))
            key,node=('long_string',value),[3,items]
        else:
            assert value is None or isinstance(value,(str,int,float,bool))
            key,node=(type(value).__name__,value),[0,value]
        if key not in lookup:
            lookup[key]=len(nodes);nodes.append(node)
        index=lookup[key]
        if container:memo[id(value)]=index
        return index
    root=encode(report)
    return {'codec':'typed_shared_nodes_and256_character_string_chunks_v1','root':root,'nodes':nodes}

"""Mature-fit stock vocabulary, unknown zero embedding, and numeric interactions."""
def validate_ids(x, vocabulary_size=4651):
    import numpy as np
    ids=x[:,-1]
    assert x.ndim==2 and x.shape[1]==121
    assert np.isfinite(ids).all() and np.equal(ids,np.floor(ids)).all()
    assert np.all((ids>=0)&(ids<vocabulary_size))

def attach(encoded,codes,vocabulary):
    import numpy as np
    assert len(vocabulary)<=4650 and vocabulary==sorted(set(vocabulary))
    assert encoded.ndim==2 and encoded.shape[1]==120 and len(encoded)==len(codes)
    mapping={code:i+1 for i,code in enumerate(vocabulary)}
    ids=np.asarray([mapping.get(str(code),0) for code in codes],dtype=np.float32)
    x=np.column_stack((encoded,ids)).astype(np.float32)
    validate_ids(x)
    return x

def network(features,cfg):
    import torch
    assert features==121 and cfg['stock_embedding_dim']==32 and cfg['stock_vocabulary_size']==4651
    class StockNetwork(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding=torch.nn.Embedding(4651,32,padding_idx=0)
            layers=[];width=120+32
            for hidden in cfg['hidden']:
                layers.extend([torch.nn.Linear(width,hidden),torch.nn.LayerNorm(hidden),torch.nn.SiLU(),torch.nn.Dropout(cfg['dropout'])]);width=hidden
            layers.append(torch.nn.Linear(width,1))
            self.body=torch.nn.Sequential(*layers)
        def forward(self,x):
            value=torch.cat((x[:,:120],self.embedding(x[:,120].long())),dim=1)
            return self.body(value)
    return StockNetwork()

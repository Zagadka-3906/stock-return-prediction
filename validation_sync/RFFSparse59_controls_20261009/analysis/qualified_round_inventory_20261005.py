"""Track every required round and highest qualified score across explicit parents."""


def assess(completed, registered_rounds, published_rounds):
    qualified={number:result for number,result in completed}
    assert qualified
    pending=sorted(set(registered_rounds)-set(qualified))
    latest=max(qualified)
    best_number,best_result=max(completed,key=lambda row:(row[1]['winner']['connected_final_score'],-row[0]))
    prefix=[]
    for number in sorted(set(registered_rounds)):
        if number not in qualified:break
        prefix.append(number)
    return {'latest_qualified_round':latest,'best_round':best_number,'best_result':best_result,
        'pending_rounds':pending,'active_round':pending[0] if pending else latest+1,
        'qualified_rounds':sorted(qualified),'last_contiguous_registered_completed_round':max(prefix,default=None),
        'published_rounds_pending_scoped_completion':sorted(set(published_rounds)-set(qualified))}

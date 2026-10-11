"""Pure route and official-S tie contract for the already frozen157 core drafts."""
from prepare_ReusedNN164Stage_core_v62_20261009 import route
def best_key(row):
    return (-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case'])

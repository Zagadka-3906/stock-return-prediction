"""Fresh prospective routes supporting the declared zero-weight flag ablation."""
from pathlib import Path
import ast

SOURCE=Path(__file__).with_name('prepare_flagged_HGB_small_amplitude88_candidate_sources_20261007.py')


class FreshRoutes(ast.NodeTransformer):
    def visit_Constant(self,node):
        if isinstance(node.value,str):
            node.value=node.value.replace('prepare_flagged_HGB_small_amplitude88_selected_candidate_20261007',
                'prepare_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007').replace(
                'seal_flagged_HGB_small_amplitude88_selected_candidate_20261007',
                'seal_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007').replace(
                'flagged_HGB_small_amplitude88_candidate_source_preparation_20261007',
                'flagged_HGB_small_amplitude88_candidate_source_preparation_v2_20261007')
        return node

    def visit_IfExp(self,node):
        if isinstance(node.test,ast.Constant) and node.test.value is False:return self.visit(node.orelse)
        return self.generic_visit(node)


def main():
    tree=FreshRoutes().visit(ast.parse(SOURCE.read_text(encoding='utf8')))
    body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
    index=next(i for i,n in enumerate(body) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='compile')
    body.insert(index,ast.parse("text=text.replace(\"cfg['weight']>0.\",\"cfg['weight']>=0.\")").body[0])
    tree=ast.fix_missing_locations(tree)
    namespace={'__file__':__file__,'__name__':'fresh_116_candidate_routes_with_zero_ablation'}
    exec(compile(tree,str(SOURCE),'exec'),namespace)
    namespace['main']()


if __name__=='__main__':main()

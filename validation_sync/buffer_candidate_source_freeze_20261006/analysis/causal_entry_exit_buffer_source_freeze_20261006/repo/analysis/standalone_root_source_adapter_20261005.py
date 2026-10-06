"""Apply the existing empty-root contract before looking up candidate files."""


def resolve(graph, original):
    root = graph['root']
    if root['kind'] == 'standalone' or root['configuration'].get('standalone'):
        return {}
    return original(graph)


def install(namespace):
    original = namespace.root_model_sources

    def root_model_sources(graph):
        return resolve(graph, original)

    namespace.root_model_sources = root_model_sources

    def restore():
        assert namespace.root_model_sources is root_model_sources
        namespace.root_model_sources = original

    return restore

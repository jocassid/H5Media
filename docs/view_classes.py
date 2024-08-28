
from graphviz import Digraph


def class_node(graph, class_name, attributes=None, methods=None):
    pieces = [
        '<table>',
        f'<tr><td>{class_name}</td></tr>',
    ]

    if attributes:
        pieces.append('<tr><td>')
        pieces.append(
            "<br/>".join(attributes)
        )
        pieces.append('</td></tr>')

    if methods:
        pieces.append('<tr><td>')
        pieces.append(
            "<br/>".join(methods)
        )
        pieces.append('</td></tr>')

    pieces.append('</table>')
    html = "".join(pieces)
    graph.node(class_name, f'<{html}>', shape='plain')


def inherits_edge(graph, sub_class, super_classes):
    for super_class in super_classes:
        graph.edge(
            super_class,
            sub_class,
            dir='back',
            arrowtail='empty',
        )


def main():
    graph = Digraph(
        name='graphviz1',
        comment='Graph Label',
        format='svg',
        node_attr={
            'shape': 'rectangle',
        },
        graph_attr={
            'splines': 'ortho',
        }
    )

    graph.node('LoginRequiredMixin')
    graph.node('TemplateView')
    graph.node('DetailView')

    graph.node('BaseView')

    class_node(graph, 'PageView', ['page_title_suffix',])
    class_node(graph, 'BasePostView', methods=['post()'])

    inheritance = {
        'BaseView': ('LoginRequiredMixin', 'TemplateView'),
        'BaseDetailView': ('LoginRequiredMixin', 'DetailView'),
        'PageView': ('BaseView',),
        'BasePostView': ('BaseView',)
    }

    for sub_class, super_classes in inheritance.items():
        inherits_edge(graph, sub_class, super_classes)

    graph.render()


if __name__ == '__main__':
    main()


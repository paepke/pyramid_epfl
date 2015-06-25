import solute.epfl as epfl
from solute.epfl.components import RecursiveTree

from componentbase import ComponentContainerBaseTest


class RecursiveTreeTest(ComponentContainerBaseTest):
    component = epfl.components.RecursiveTree

    def test_show_children(self):
        page, transaction = self.bootstrap()

        page.model = True

        with self.assertRaises(AttributeError):
            page.root_node.add_component(RecursiveTree(
                get_data=['some_loader'],
                show_children=True
            ))

        page.root_node.add_component(RecursiveTree(
            get_data=['some_lader']
        ))

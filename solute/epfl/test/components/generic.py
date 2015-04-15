import solute.epfl as epfl
import inspect

from componentbase import ComponentBaseTest, ComponentContainerBaseTest


_globals = globals()

for compo in inspect.getmembers(epfl.components, predicate=inspect.isclass):
    compo_name, compo_class = compo
    sub_class = ComponentBaseTest
    if issubclass(compo_class, epfl.core.epflcomponentbase.ComponentContainerBase):
        sub_class = ComponentContainerBaseTest
    name = compo_name + 'Test'
    cls = type(name, (sub_class, ), {})
    cls.component = compo_class
    globals()[name] = cls

epfl.init_component("{{compo.cid}}",
                        "DroppableComponent",
                        {type: {{ compo.get_valid_types(True)|safe }}});
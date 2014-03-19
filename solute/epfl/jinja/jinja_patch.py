#* coding: utf-8

from jinja2 import environment


def make_module_patch(self, vars=None, shared=False, locals=None):
    env = self.environment.overlay(undefined = NeverFailUndefined)
    ctx = environment.new_context(env, self.name, self.blocks, vars, shared, self.globals, locals)
    return environment.TemplateModule(self, ctx)

environment.Template.make_module = make_module_patch

class NeverFailUndefined(environment.Undefined):
    def __call__(self, *args, **kwargs): return ""
    def __getattr__(self, key): return self

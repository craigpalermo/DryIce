from jinja2 import Template, Environment, FileSystemLoader
import os

def render(path,dic={}):
    env_path = os.path.abspath(os.path.dirname(__file__))
    template_path = os.path.abspath(os.path.join(env_path,"../templates"))
    env = Environment(
            loader=FileSystemLoader(template_path),
            extensions=['pyjade.ext.jinja.PyJadeExtension'],
        )
    tpl = env.get_template(path)
    return tpl.render(dic)

def render_str(string,dic={}):
    tpl = Template(string)
    return tpl.render(dic)

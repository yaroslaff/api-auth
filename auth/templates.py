from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

template_env = Environment(
    # loader=PackageLoader('project', 'templates'),
    loader=FileSystemLoader('templates'),

    autoescape=select_autoescape(['html', 'xml'])
)

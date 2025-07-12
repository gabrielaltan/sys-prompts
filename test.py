import yaml
from jinja2 import Template
from pathlib import Path


def render_yaml_template(template_path):
    """Render YAML template with Jinja2 placeholders"""
    # Read the template file
    template_content = Path(template_path).read_text()

    # Create Jinja2 template
    template = Template(template_content)

    # Render the template (this will resolve all {{placeholder}} references)
    rendered_content = template.render()

    # Parse the rendered YAML
    content = yaml.safe_load(rendered_content)

    return content


# Example usage
if __name__ == "__main__":
    content = render_yaml_template("prompts/blocks/docs.yaml")
    print(content["agents-docs"])

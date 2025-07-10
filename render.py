from pathlib import Path
import re
import logging
from typing import Dict

# Directories
BASE_DIR = Path("prompts")
BLOCKS_DIR = BASE_DIR / "blocks"
TEMPLATES_DIR = BASE_DIR / "templates"
RENDERED_DIR = BASE_DIR / "rendered"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main() -> None:
    """Entry point: load blocks and render templates."""
    blocks = loads_blocks()
    print(blocks)
    render_templates(blocks)


def loads_blocks() -> Dict[str, str]:
    """
    Load all block definitions from markdown files in the blocks directory.
    Returns:
        dict: Mapping of block names to their content.
    Raises:
        ValueError: If a block file is invalid.
    """
    pattern = r"<!(?P<name>[\w\-]+)>\s*(?P<content>.*?)\s*<!/\1>"
    blocks = {}
    for file_path in BLOCKS_DIR.glob("*.md"):
        content = file_path.read_text()
        if not validate_block_file(content):
            raise ValueError(f"Block file {file_path.name} format is invalid.")
        file_blocks = {
            match["name"]: match["content"].strip()
            for match in re.finditer(pattern, content, re.DOTALL)
        }
        blocks.update(file_blocks)
    return blocks


def validate_block_file(content: str) -> bool:
    """
    Validate a block file's content. Logs warnings for format issues.
    Args:
        content: The content of the block file.
    Returns:
        True if valid, False otherwise.
    """
    # Validation for incorrectly formatted blocks
    open_tag_pattern = r"<!([\w\-]+)>"
    close_tag_pattern = r"<!/([\w\-]+)>"

    open_tags = [
        (m.group(1), m.start()) for m in re.finditer(open_tag_pattern, content)
    ]
    close_tags = [
        (m.group(1), m.start()) for m in re.finditer(close_tag_pattern, content)
    ]

    open_tag_names = [name for name, _ in open_tags]
    close_tag_names = [name for name, _ in close_tags]

    is_valid = True

    # Check for tags that are opened but not closed
    for name, pos in open_tags:
        if name not in close_tag_names:
            logging.warning(f"<!{name}> opened at position {pos} but not closed.")
            is_valid = False

    # Check for tags that are closed but not opened
    for name, pos in close_tags:
        if name not in open_tag_names:
            logging.warning(f"<!/{name}> closed at position {pos} but not opened.")
            is_valid = False

    # Check for mismatched tag pairs (order sensitive)
    if len(open_tags) != len(close_tags):
        logging.warning("Number of opening and closing tags does not match.")
        is_valid = False
    else:
        for (open_name, open_pos), (close_name, close_pos) in zip(
            open_tags, close_tags
        ):
            if open_name != close_name:
                logging.warning(
                    f"Tag mismatch: <!{open_name}> at {open_pos} closed by <!/{close_name}> at {close_pos}."
                )
                is_valid = False

    return is_valid


def render_templates(blocks: Dict[str, str]) -> None:
    """
    Render all templates using the provided blocks.
    Args:
        blocks: Mapping of block names to their content.
    """
    for file_path in TEMPLATES_DIR.glob("*.md"):
        content = file_path.read_text()
        rendered = render(content, blocks)
        save_rendered_file(file_path.name, rendered)


def render(content: str, blocks: Dict[str, str]) -> str:
    """
    Render a template by replacing block placeholders with their content.
    Args:
        content: The template content.
        blocks: Mapping of block names to their content.
    Returns:
        The rendered template as a string.
    Raises:
        ValueError: If a block is referenced but not found.
    """

    def replace_block(match):
        key = match.group(1)
        rendered = blocks.get(key, "")
        if not rendered:
            raise ValueError(f"Block {key} not found in blocks.")
        return rendered

    return re.sub(r"\$\{([a-zA-Z0-9_-]+)\}", replace_block, content)


def save_rendered_file(filename: str, content: str) -> None:
    """
    Save a rendered file to the rendered directory.
    Args:
        filename: Name of the file to save.
        content: Content to write.
    """
    RENDERED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RENDERED_DIR / filename
    output_path.write_text(content)
    logging.info(f"Rendered file {filename} saved.")


if __name__ == "__main__":
    main()

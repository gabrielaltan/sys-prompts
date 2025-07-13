from pathlib import Path
import re
import logging
import argparse
import time
from typing import Dict
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directories
BASE_DIR = Path("prompts")
BLOCKS_DIR = BASE_DIR / "blocks"
TEMPLATES_DIR = BASE_DIR / "templates"
RENDERED_DIR = BASE_DIR / "rendered"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class TemplateRenderer:
    """Handles template rendering with caching and file watching."""

    def __init__(self):
        self.blocks_cache = {}
        self.last_blocks_mtime = 0

    def load_blocks(self) -> Dict[str, str]:
        """
        Load all block definitions from YAML files in the blocks directory.
        Returns:
            dict: Mapping of block names to their content.
        Raises:
            ValueError: If a block file is invalid YAML or not a dict of strings.
        """
        # Check if blocks have changed
        current_mtime = max(
            (f.stat().st_mtime for f in BLOCKS_DIR.glob("*.yaml")), default=0
        )

        if current_mtime <= self.last_blocks_mtime and self.blocks_cache:
            return self.blocks_cache

        self.last_blocks_mtime = current_mtime
        blocks = {}

        for file_path in BLOCKS_DIR.glob("*.yaml"):
            try:
                # Use yaml.load with SafeLoader to handle aliases properly
                content = yaml.load(file_path.read_text(), Loader=yaml.SafeLoader)
            except Exception as e:
                raise ValueError(
                    f"Block file {file_path.name} could not be parsed as YAML: {e}"
                )
            if not isinstance(content, dict):
                raise ValueError(
                    f"Block file {file_path.name} does not contain a dictionary at the top level."
                )
            for k, v in content.items():
                if not isinstance(k, str):
                    raise ValueError(
                        f"Block file {file_path.name} contains non-string key: {k}"
                    )
                if isinstance(v, str):
                    blocks[k] = v
                elif isinstance(v, list):
                    blocks[k] = "\n\n".join(str(item) for item in v)
                else:
                    raise ValueError(
                        f"Block file {file_path.name} contains unsupported value type for key {k}: {type(v)}"
                    )

        self.blocks_cache = blocks
        return blocks

    def render_templates(self, blocks: Dict[str, str]) -> None:
        """
        Render all templates using the provided blocks.
        Args:
            blocks: Mapping of block names to their content.
        """
        for file_path in TEMPLATES_DIR.glob("*.md"):
            content = file_path.read_text()
            rendered = self.render(file_path.name, content, blocks)
            self.save_rendered_file(file_path.name, rendered)

    def render(self, filename: str, content: str, blocks: Dict[str, str]) -> str:
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
                raise ValueError(f"Block {key} not found in blocks for {filename}.")
            return rendered

        return re.sub(r"\$\{([a-zA-Z0-9_-]+)\}", replace_block, content)

    def save_rendered_file(self, filename: str, content: str) -> None:
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

    def render_all(self) -> None:
        """Render all templates with current blocks."""
        blocks = self.load_blocks()
        self.render_templates(blocks)


class FileChangeHandler(FileSystemEventHandler):
    """Handles file system events for auto-rendering."""

    def __init__(self, renderer: TemplateRenderer):
        self.renderer = renderer

    def on_modified(self, event):
        if not event.is_directory:
            if event.src_path.endswith(".yaml") or event.src_path.endswith(".md"):
                logging.info(f"File changed: {event.src_path}")
                try:
                    self.renderer.render_all()
                    logging.info("Templates re-rendered successfully")
                except Exception as e:
                    logging.error(f"Error re-rendering templates: {e}")


def main() -> None:
    """Entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Render markdown templates with YAML blocks"
    )
    parser.add_argument(
        "--watch",
        "-w",
        action="store_true",
        help="Watch for file changes and auto-render templates",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    renderer = TemplateRenderer()

    if args.watch:
        logging.info("Starting watch mode...")
        event_handler = FileChangeHandler(renderer)
        observer = Observer()
        observer.schedule(event_handler, str(BLOCKS_DIR), recursive=False)
        observer.schedule(event_handler, str(TEMPLATES_DIR), recursive=False)
        observer.start()

        try:
            # Initial render
            renderer.render_all()
            logging.info("Watch mode active. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            logging.info("Watch mode stopped.")
        observer.join()
    else:
        # Single render
        renderer.render_all()


# Legacy function names for backward compatibility
def loads_blocks() -> Dict[str, str]:
    """Legacy function - use TemplateRenderer.load_blocks() instead."""
    renderer = TemplateRenderer()
    return renderer.load_blocks()


def render_templates(blocks: Dict[str, str]) -> None:
    """Legacy function - use TemplateRenderer.render_templates() instead."""
    renderer = TemplateRenderer()
    renderer.render_templates(blocks)


def render(filename: str, content: str, blocks: Dict[str, str]) -> str:
    """Legacy function - use TemplateRenderer.render() instead."""
    renderer = TemplateRenderer()
    return renderer.render(filename, content, blocks)


def save_rendered_file(filename: str, content: str) -> None:
    """Legacy function - use TemplateRenderer.save_rendered_file() instead."""
    renderer = TemplateRenderer()
    renderer.save_rendered_file(filename, content)


if __name__ == "__main__":
    main()

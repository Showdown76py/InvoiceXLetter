import json, os

from classes.config import *


def load_config(path: str = "config.json") -> tuple[Config, str]:
    with open(path, "r") as f:
        config_data = json.load(f)

    regex = ""
    cfg = Config(
        extraction_type=ExtractionType(config_data["extraction_type"]),
        search_string=config_data["search_string"],
        show_window_border=config_data["show_window_border"],
        use_regex=config_data["use_regex"],
        font=FontConfig(
            name=config_data["font"]["name"],
            size=config_data["font"]["size"],
            color=config_data["font"]["color"],
            path=config_data["font"].get("path"),  # Optional path for custom fonts
        ),
        display=Display(
            margin_top=config_data["display"]["margin_top"],
            margin_right=config_data["display"]["margin_right"],
            width=config_data["display"]["width"],
            height=config_data["display"]["height"],
        ),
    )

    if cfg.use_regex:
        if os.path.exists("regex.txt"):
            with open("regex.txt", "r") as f:
                regex = f.read()
        else:
            with open("regex.txt", "w") as f:
                f.write("")
                regex = ""

    return cfg, regex

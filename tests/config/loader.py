import os
import yaml


def load_settings(config_path=None):
    path = config_path or os.path.join(os.path.dirname(__file__), "settings.yml")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    base_url = os.getenv("BASE_URL", data.get("base_url", "https://example.org"))
    browser = os.getenv("BROWSER", data.get("browser", "chrome"))
    headless_env = os.getenv("HEADLESS")
    if headless_env is not None:
        headless = str(headless_env).lower() == "true"
    else:
        headless = bool(data.get("headless", False))
    return {
        "base_url": base_url,
        "browser": browser,
        "headless": headless,
    }

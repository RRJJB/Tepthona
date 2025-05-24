
import importlib
import os

from pathlib import Path

def load_plugins():
    plugins_dir = Path(__file__).parent / "plugins"
    for file in os.listdir(plugins_dir):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = f"Tepthon.plugins.{file[:-3]}"
            try:
                importlib.import_module(module_name)
                print(f"تم تحميل الإضافة: {file}")
            except Exception as e:
                print(f"فشل في تحميل {file}: {e}")

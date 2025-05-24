import importlib
import os
from pathlib import Path
from typing import Union, List

def load(paths: Union[str, List[str]] = ["plugins"]):
    if isinstance(paths, str):
        paths = [paths]

    for plugins_dir in [Path(__file__).parent / p for p in paths]:
        if not plugins_dir.exists():
            print(f"❌ المسار غير موجود: {plugins_dir}")
            continue

        for file in os.listdir(plugins_dir):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = f"Tepthon.{plugins_dir.name}.{file[:-3]}"
                try:
                    importlib.import_module(module_name)
                    print(f"✅ تم تحميل الإضافة: {module_name}")
                except Exception as e:
                    print(f"❌ فشل في تحميل {module_name}: {e}")

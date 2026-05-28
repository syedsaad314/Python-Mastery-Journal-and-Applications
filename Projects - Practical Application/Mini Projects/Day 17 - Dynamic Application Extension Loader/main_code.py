"""
Mini-Project: Dynamic Application Extension Loader
Description: Loads and registers custom modular application components dynamically at runtime.
Lead Engineer: Syed Saad Bin Irfan
"""

import importlib.util
import os
import sys
from typing import Dict, Protocol

# Enforce clean engineering standards using structural types (SOLID Interface)
class PluginInterface(Protocol):
    @property
    def name(self) -> str: ...
    def transform(self, dataset: dict) -> dict: ...

class KernelCore:
    def __init__(self) -> None:
        self.extensions: Dict[str, PluginInterface] = {}

    def register_extension_file(self, module_id: str, disk_path: str) -> None:
        if not os.path.exists(disk_path):
            return

        # Low-level dynamic import stitching
        spec = importlib.util.spec_from_file_location(module_id, disk_path)
        if spec is None or spec.loader is None:
            return
            
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_id] = mod
        spec.loader.exec_module(mod)

        # Inspect the newly loaded module properties for matching structural blueprints
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if isinstance(attr, type) and hasattr(attr, "name") and hasattr(attr, "transform"):
                instance = attr()
                self.extensions[instance.name] = instance
                print(f"[KERNEL] Dynamically mounted runtime module extension: {instance.name}")

if __name__ == "__main__":
    # Generate a mock plugin script dynamically to verify the registration loop
    mock_script = "plugin_uppercase.py"
    with open(mock_script, "w") as f:
        f.write("\n".join([
            "class UppercaseExtension:",
            "    @property",
            "    def name(self): return 'UPPERCASE_MUTATOR'",
            "    def transform(self, data: dict):",
            "        return {'payload': data.get('val', '').upper()}"
        ]))

    kernel = KernelCore()
    try:
        kernel.register_extension_file("ext_upper", mock_script)
        if "UPPERCASE_MUTATOR" in kernel.extensions:
            res = kernel.extensions["UPPERCASE_MUTATOR"].transform({"val": "saad_bin_irfan"})
            print(f"[PORTFOLIO SHOWCASE] Extension response payload: {res}")
    finally:
        if os.path.exists(mock_script):
            os.remove(mock_script)
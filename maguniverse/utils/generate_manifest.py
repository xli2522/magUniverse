# -*- coding: utf-8 -*-
"""
Generate a manifest mapping exported functions in maguniverse.data submodules

This script traverses all __init__.py files under maguniverse/data, extracts the
symbols listed in each module's __all__, and writes a JSON manifest mapping each
symbol to its fully qualified module:function reference.

Usage
-----
Run this script from the project root:

    python generate_manifest.py [--output PATH]

This will create or overwrite the manifest JSON at the specified output path.
"""

import ast
import json
from pathlib import Path

def main():
    # Root directory of the repository (assumes this script lives at project root)
    # two parents up from utils/generate_manifest.py
    root = Path(__file__).parent.parent.resolve()   
    data_dir = root / 'data'
    manifest = {}

    # Recursively find every __init__.py under maguniverse/data
    for init_path in data_dir.rglob('__init__.py'):
        # Derive the module path, e.g., maguniverse.data.polarization
        rel_path = init_path.relative_to(root)
        module_path = rel_path.with_suffix('').as_posix().replace('/', '.')
        
        # Parse the AST of the __init__.py
        source = init_path.read_text(encoding='utf-8')
        tree = ast.parse(source, filename=str(init_path))

        # Find the assignment to __all__
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == '__all__':
                        # Expect __all__ = [ ... ] or (...)
                        if isinstance(node.value, (ast.List, ast.Tuple)):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                    func_name = elt.value
                                    # Map function name to module:function
                                    manifest[func_name] = f"{module_path}:{func_name}"

    # Write out the manifest.json in the project root
    manifest_path = root.parent / 'docs' / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Generated manifest with {len(manifest)} entries at {manifest_path}")

if __name__ == '__main__':
    main()

import json
import os
import re

filename = os.path.join("../", "MANIFEST.json")
with open(filename) as fp:
    t = json.load(fp)

for taxo in sorted(t['taxonomies'], key=lambda k: k['name']):
    print(f"### {taxo['name']}")
    print()
    print(
        f"[{taxo['name']}](https://github.com/MISP/misp-taxonomies/tree/main/{taxo['name']}) :\n{taxo['description']} [Overview](https://www.misp-project.org/taxonomies.html#_{re.sub(r'-', '_', taxo['name'])})\n"
    )

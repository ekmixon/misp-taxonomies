#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from datetime import datetime

TAXONOMY_ROOT_PATH = Path(__file__).resolve().parent.parent


def fetchTaxonomies():
    taxonomiesFolder = TAXONOMY_ROOT_PATH
    taxonomies = []
    allTaxonomies = sorted(taxonomiesFolder.glob('./*/machinetag.json'))
    for taxonomyFile in allTaxonomies:
        with open(taxonomyFile, 'rb') as f:
            taxonomy = json.load(f)
            taxonomies.append(taxonomy)
    return taxonomies

def generateManifest(taxonomies):
    now = datetime.now()
    manifest = {
        'taxonomies': [],
        'path': 'machinetag.json',
        'url': 'https://raw.githubusercontent.com/MISP/misp-taxonomies/main/',
        'description': 'Manifest file of MISP taxonomies available.',
        'license': 'CC-0',
        'version': '{}{:02}{:02}'.format(now.year, now.month, now.day),
    }

    for taxonomy in taxonomies:
        taxObj = {
            'name': taxonomy['namespace'],
            'description': taxonomy['description'],
            'version': taxonomy['version']
        }
        manifest['taxonomies'].append(taxObj)
    return manifest

def saveManifest(manifest):
    with open(TAXONOMY_ROOT_PATH / 'MANIFEST.json', 'w') as f:
        json.dump(manifest, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write('\n')

def awesomePrint(text):
    print(f'\033[1;32m{text}\033[0;39m')

if __name__ == "__main__":
    taxonomies = fetchTaxonomies()
    manifest = generateManifest(taxonomies)
    saveManifest(manifest)
    awesomePrint('> Manifest saved!')

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

def generateMarkdown(taxonomies):
    markdown_line_array = [
        "# Taxonomies",
        f"- Generation date: {datetime.now().isoformat().split('T')[0]}",
        '- license: CC-0',
        '- description: Manifest file of MISP taxonomies available.',
        "",
        "## Taxonomies",
        "",
    ]

    for taxonomy in taxonomies:
        markdown_line_array.append(f"### {taxonomy['namespace']}")
        markdown_line_array.append(f"- description: {taxonomy['description']}")
        markdown_line_array.append(f"- version: {taxonomy['version']}")
        markdown_line_array.append("- Predicates")
        markdown_line_array = markdown_line_array + ['    - '+p['value'] for p in taxonomy['predicates']]
    return '\n'.join(markdown_line_array)

def saveMarkdown(markdown):
    with open(TAXONOMY_ROOT_PATH / 'summary.md', 'w') as f:
        f.write(markdown)

def awesomePrint(text):
    print(f'\033[1;32m{text}\033[0;39m')

if __name__ == "__main__":
    taxonomies = fetchTaxonomies()
    markdown = generateMarkdown(taxonomies)
    saveMarkdown(markdown)
    awesomePrint('> Markdown saved!')

#!/usr/bin/env python3
"""Validate current documentation links and every archived language entry point."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit

from builder.consts import BUNDLED_VERSIONS, CURRENT_VERSION, VERSION_ARRAY


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and (key == 'id' or (tag == 'a' and key == 'name')):
                self.ids.add(value)
            if value and key in ('href', 'src'):
                self.urls.append(value)


def check(root):
    errors = set()
    count = 0
    parsed = {}
    placeholders = (
        'Comming soon...',
        'The second blog post',
        'Easy documentation with Docsy',
        'Another Great Release',
        'UA-00000000-0',
    )

    def parse(page):
        if page not in parsed:
            parser = Links()
            parser.feed(page.read_text(encoding="utf-8"))
            parsed[page] = parser
        return parsed[page]

    for page in sorted(root.rglob('*.html')):
        relative = page.relative_to(root).as_posix()
        archive = re.match(r'v([0-9]+\.[0-9]+)/', relative)
        if archive and archive[1] not in [CURRENT_VERSION, *BUNDLED_VERSIONS]:
            continue
        # Docsy's print view aggregates content with links relative to original pages.
        if '_print/' in relative:
            continue
        count += 1
        if not archive:
            source = page.read_text(encoding='utf-8')
            for placeholder in placeholders:
                if placeholder in source:
                    errors.add(f'{relative}: template placeholder {placeholder!r}')
        parser = parse(page)
        page_url = 'https://kubeclipper.io/' + relative
        for url in parser.urls:
            target = urlsplit(urljoin(page_url, url))
            if target.scheme not in ('http', 'https') or target.netloc not in ('kubeclipper.io', 'www.kubeclipper.io'):
                continue
            path = root / unquote(target.path).lstrip('/')
            if path.is_dir():
                path = path / 'index.html'
            if not path.is_file():
                errors.add(f'{relative}: {url}')
                continue
            # Fragment checks cover the current release only; archives remain unchanged.
            if (not archive or archive[1] == CURRENT_VERSION) and target.fragment and path.suffix == '.html':
                if unquote(target.fragment) not in parse(path).ids:
                    errors.add(f'{relative}: {url} (missing fragment)')
    for language in ('', 'en/'):
        for section in ('', 'docs/'):
            path = root / language / section / 'index.html'
            if not path.is_file():
                errors.add(f'Missing current entry: {path.relative_to(root)}')
    for version in VERSION_ARRAY:
        for language in ('', 'en/'):
            for section in ('', 'docs/'):
                path = root / ('v' + version) / language / section / 'index.html'
                if not path.is_file():
                    errors.add(f'Missing version entry: {path.relative_to(root)}')
    if errors:
        raise SystemExit('Broken local links or missing version entries:\n' + '\n'.join(sorted(errors)))
    print(f'Checked {count} current/bundled HTML pages and {len(VERSION_ARRAY)} bilingual version entries.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    check(parser.parse_args().directory.resolve())

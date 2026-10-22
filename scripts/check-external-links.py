#!/usr/bin/env python3
"""Check links authored in current documentation; report network failures separately."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import re
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlsplit
from urllib.request import Request, urlopen


def collect(root):
    urls = set()
    for page in list(root.rglob('*.md')) + list(root.rglob('*.html')):
        source = page.read_text(encoding='utf-8')
        links = re.findall(r'\]\((https?://[^\s)]+)', source)
        links += re.findall(r'href=["\'](https?://[^"\']+)', source)
        for raw in links:
            url = urldefrag(raw)[0]
            parts = urlsplit(url)
            if parts.scheme in ('http', 'https') and parts.hostname not in ('kubeclipper.io', 'www.kubeclipper.io', 'example.com'):
                urls.add(url)
    return sorted(urls)


def check(url):
    for method in ('HEAD', 'GET'):
        try:
            request = Request(url, headers={'User-Agent': 'KubeClipperDocsLinkCheck/1.0'}, method=method)
            with urlopen(request, timeout=10) as response:
                return url, 'ok', str(response.status)
        except HTTPError as error:
            if method == 'HEAD' and error.code == 405:
                continue
            return url, ('broken' if error.code in (404, 410) else 'inconclusive'), f'HTTP {error.code}'
        except (TimeoutError, socket.timeout):
            return url, 'timeout', 'timed out'
        except URLError as error:
            reason = error.reason
            if isinstance(reason, (TimeoutError, socket.timeout)):
                return url, 'timeout', str(reason)
            return url, 'inconclusive', str(reason)
    return url, 'inconclusive', 'HEAD and GET unavailable'


def main(root):
    urls = collect(root)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = sorted(pool.map(check, urls))
    counts = {kind: sum(result[1] == kind for result in results)
              for kind in ('ok', 'broken', 'timeout', 'inconclusive')}
    lines = [f"External links: {len(urls)} checked; " + ', '.join(f'{kind}={count}' for kind, count in counts.items())]
    for url, kind, detail in results:
        if kind != 'ok':
            lines.append(f'{kind}: {url} ({detail})')
    report = '\n'.join(lines) + '\n'
    print(report, end='')
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as summary:
            summary.write('## External links\n\n```text\n' + report + '```\n')
    if counts['broken']:
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    main(parser.parse_args().directory.resolve())

#!/usr/bin/env python3
"""
class/method for rendering transcript to HTML. Just fooling around for now...

Sample usage:

    $ seshkit/renderer.py examples/transcripts/obama-romney-town-hall.json > examples/transcripts/obama-romney-town-hall.html

"""
import json
from pathlib import Path
import re
import sys
from typing import Union as typeUnion

from jinja2 import Environment, PackageLoader, select_autoescape

jenv = Environment(
    loader=PackageLoader('seshkit', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

TEMPLATE_BASENAME = 'index.html.jinja'

def simplify(data:typeUnion[dict, str, Path]) -> dict:
    """
    flatten:
        for each segment
        for every item, extract:
            segment_number, start_time, end_time, content, confidence, type, speaker
    """
    if not isinstance(data, dict):
        data = json.loads(Path(data).read_text())


    segs = data['results']['segments']
    labels = data['results']['speaker_labels']['segments']

    fdata = []
    for i, _s in enumerate(segs):
        seg = _s['alternatives'][0]
        speaker = re.search(r'(?<=spk_)\d+', labels[i]['speaker_label']).group()
        fseg = {'transcript': seg['transcript'], 'speaker': speaker, 'items': []}
        for _item in seg['items']:
            fitem = _item.copy()
            fitem['segment_number'] = i
            fitem['speaker'] = speaker
            for k in ('start_time', 'end_time', 'confidence',):
                fitem[k] = float(fitem[k]) if fitem.get(k) else None
            fseg['items'].append(fitem)
        fdata.append(fseg)

    return {
        'job_name': data['jobName'],
        'speaker_count': data['results']['speaker_labels']['speakers'],
        'transcript': data['results']['transcripts'][0]['transcript'],
        'segments': fdata,
    }


def to_html(sdata:typeUnion[dict, str, Path]) -> str:
    """
    sdata: a dict or Path/str of a transcript in simplified format
    """
    if not isinstance(sdata, dict):
        sdata = json.loads(Path(sdata).read_text())

    jtemplate = jenv.get_template(TEMPLATE_BASENAME)
    html = jtemplate.render(segments=sdata['segments'], lstrip_blocks=True, trim_blocks=True)
    return html

if __name__ == '__main__':
    """
    run on original transcript format
    """
    input_path = sys.argv[1]
    sys.stderr.write(f"Opening {input_path=}\n")
    data = simplify(input_path)
    sys.stdout.write(to_html(data))

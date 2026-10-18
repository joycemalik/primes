"""
Finish the two moves Windows refused during the reorganisation ("Access is denied" because
something had files open inside them). Close any editor, terminal or File Explorer window that is
inside simu1 or simu2, stop their dev servers, then run:

    python archive/reorganization/finish_pending_moves.py

Each move is appended to log.json so undo_reorganization.py can reverse it too.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
os.chdir(ROOT)
PENDING = [
    ('simu1', 'other-projects/simu1-fusionflow-and-3d-viewer', 'Separate project: FusionFlow backend and image 3D viewer.'),
    ('simu2', 'other-projects/simu2-workflow-server-and-web', 'Separate project: workflow server with model providers and a web front end.'),
]
log_path = os.path.join(HERE, 'log.json')
log = json.load(open(log_path, encoding='utf-8'))
for src, dst, what in PENDING:
    if not os.path.exists(src):
        print('already moved:', src); continue
    try:
        os.rename(src, dst)
        log['ops'] = [o for o in log['ops'] if not (o['op'] == 'FAILED' and o['from'] == src)]
        log['ops'].append({'op': 'move', 'kind': 'dir', 'from': src, 'to': dst, 'what': what})
        print('moved', src, '->', dst)
    except OSError as e:
        print('still locked:', src, '-', e)
json.dump(log, open(log_path, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

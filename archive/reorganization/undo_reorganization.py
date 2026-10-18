"""
Undo the October 2026 reorganisation of D:\\code\\fun.

Reads log.json (next to this file) and reverses every step in reverse order:
  * removes the header comments that were added to research scripts,
  * reverts the path patches that kept cross-file references working,
  * moves every file and folder back to its original location,
  * recreates the empty learn/ folders that were removed after being emptied.
Modification times are preserved. Run with:  python archive/reorganization/undo_reorganization.py
Add --dry to only print what would happen.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
DRY = '--dry' in sys.argv
os.chdir(ROOT)
ops = json.load(open(os.path.join(HERE, 'log.json'), encoding='utf-8'))['ops']


def keep_time(path, text):
    st = os.stat(path)
    open(path, 'w', encoding='utf-8', errors='surrogateescape', newline='').write(text)
    os.utime(path, (st.st_atime, st.st_mtime))


for op in reversed(ops):
    kind = op['op']
    if kind == 'header' and os.path.exists(op['file']):
        lines = open(op['file'], encoding='utf-8', errors='surrogateescape').read().split('\n')
        for i in range(min(3, len(lines))):
            if lines[i].startswith('# Prime research archive ::'):
                del lines[i - 1:i + 4]
                break
        print('strip header', op['file'])
        if not DRY: keep_time(op['file'], '\n'.join(lines))
    elif kind == 'patch' and os.path.exists(op['file']):
        s = open(op['file'], encoding='utf-8').read().replace(op['new'], op['old'])
        print('revert patch', op['file'])
        if not DRY: keep_time(op['file'], s)
    elif kind == 'rmdir-empty':
        print('recreate', op['dir'])
        if not DRY: os.makedirs(op['dir'], exist_ok=True)
    elif kind == 'move':
        print('move back', op['to'], '->', op['from'])
        if not DRY:
            os.makedirs(os.path.dirname(op['from']) or '.', exist_ok=True)
            os.rename(op['to'], op['from'])
print('dry run only' if DRY else 'undo complete')

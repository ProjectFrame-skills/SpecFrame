"""Create current activation metadata before the first requirements save. No host edits."""
import argparse
import json
from pathlib import Path
import bridge


def bind(root, session, owner, state, slug, server):
    root=root.resolve();state=state.resolve()
    session,owner,slug,server=map(bridge.identifier,(session,owner,slug,server))
    if not state.is_relative_to(root):raise ValueError('State must remain inside selected project')
    if state.exists():
        current=json.loads(state.read_text())
        if not isinstance(current,dict) or current.get('format')!=1 or current.get('owner')!=owner:
            raise ValueError('Existing state is corrupt or belongs to another owner')
    elif owner!=session:
        raise ValueError('Resumed owner requires its existing state; do not invent continuity')
    record={'format':1,'session':session,'owner':owner,'state':str(state.relative_to(root)),'slug':slug,'server':server}
    path=root/'.specframe/agensi'/(session+'.json')
    if not path.resolve().is_relative_to(root):raise ValueError('Binding outside project')
    if path.exists():
        if json.loads(path.read_text())!=record:raise ValueError('Existing activation differs; select the intended current activation explicitly')
        return {'written':False,'path':str(path)}
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:stream.write(json.dumps(record)+'\n')
    return {'written':True,'path':str(path)}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True);p.add_argument('--state',type=Path,required=True)
    for name in ('session','owner','slug','server'):p.add_argument('--'+name,required=True)
    a=p.parse_args();print(json.dumps(bind(a.root,a.session,a.owner,a.state,a.slug,a.server)))

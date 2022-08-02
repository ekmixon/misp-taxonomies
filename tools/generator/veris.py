import json

debug = False
filename = 'verisc-labels.json'
namespace = 'veris'
description = 'Vocabulary for Event Recording and Incident Sharing (VERIS)'

output = {
    'namespace': namespace,
    'description': description,
    'version': 2,
    'predicates': [],
    'values': [],
}

with open(filename) as fp:
    t = json.load(fp)


def lookupPredicate(predicate=False):
    if not predicate:
        return False
    for p in output['predicates']:
        if p['value'] == predicate:
            return True


def lookupValues(predicate=False):
    return (
        next((p for p in output['values'] if p['predicate'] == predicate), {})
        if predicate
        else {}
    )


def machineTag(namespace=False, predicate=False, value=None, expanded=None):

    if namespace is False or predicate is False:
        return None
    if value is None:
        return ('{0}:{1}'.format(namespace, predicate))
    if not lookupPredicate(predicate=predicate):
        x = {'value': predicate}
        output['predicates'].append(x)
    z = {'value': value, 'expanded': expanded}
    if predicate_entries := lookupValues(predicate):
        predicate_entries['entry'].append(z)
    else:
        y = {'predicate': predicate, 'entry': []}
        y['entry'].append(z)
        output['values'].append(y)
    return ('{0}:{1}=\"{2}\"'.format(namespace, predicate, value))


prefix = []
top = []


def flatten(root, prefix_keys=True):
    dicts = [([], root)]
    ret = {}
    seen = set()
    for path, d in dicts:
        if id(d) in seen:
            continue
        seen.add(id(d))
        for k, v in sorted(d.items()):
            new_path = path + [k]
            prefix = ':'.join(new_path) if prefix_keys else k
            if hasattr(v, 'items'):
                dicts.append((new_path, v))
            else:
                p = ':'.join(prefix.rsplit(':')[:-1])
                if debug:
                    print(f"{namespace}:{p}={v}")
                machineTag(namespace=namespace, predicate=p, value=prefix.split(':')[-1], expanded=v)
                ret[prefix] = v
    return ret


flatten(root=t)

print(json.dumps(output))

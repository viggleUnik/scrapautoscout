from datetime import timedelta
import base64
import hashlib


def format_seconds(secs):
    days_hh_mm_ss = str(timedelta(seconds=secs))
    t = days_hh_mm_ss.split(':')

    if secs < 60:
        return f'{secs:.3f}sec'
    elif secs < 60 * 60:
        return f'{t[1]}min {t[2]}sec'
    else:
        return f'{t[0]}hours {t[1]}min {t[2]}sec'


def get_hash_from_string(s: str) -> str:
    md5bytes = hashlib.md5(s.encode()).digest()
    hash_str = base64.urlsafe_b64encode(md5bytes).decode('ascii')
    hash_str = ''.join(c for c in hash_str if c.isalnum())
    return hash_str


def trunc_msg(e, max_chars=300, from_end=True):
    if from_end:
        return (str(e)[:max_chars] + ' ...[truncated]') if len(str(e)) > max_chars else str(e)
    else:
        return ('[truncated]... ' + str(e)[-max_chars:]) if len(str(e)) > max_chars else str(e)


def update_nested_dict(d, u, only_existing_keys=True):
    for k, v in u.items():

        if only_existing_keys and k not in d:
            continue

        if isinstance(v, dict):
            if d.get(k, None) is None or d[k] == {}:
                d[k] = v
            else:
                d[k] = update_nested_dict(d.get(k, {}), v)
        else:
            d[k] = v

    return d


def remove_none_from_dict(d):
    for k, v in list(d.items()):
        if isinstance(v, dict):
            remove_none_from_dict(v)
        elif v is None:
            del d[k]

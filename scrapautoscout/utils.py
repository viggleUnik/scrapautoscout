from datetime import timedelta
import base64
import hashlib


def format_seconds(secs):
    days_hh_mm_ss = str(timedelta(seconds=secs))
    t = days_hh_mm_ss.split(':')

    if secs < 60:
        return f'{secs:.3f}sec'
    elif secs < 60 * 60:
        return f'{t[1]}min {int(t[2])}sec'
    else:
        return f'{t[0]}hours {t[1]}min {int(t[2])}sec'


def get_hash_from_string(s: str) -> str:
    md5bytes = hashlib.md5(s.encode()).digest()
    hash_str = base64.urlsafe_b64encode(md5bytes).decode('ascii')
    hash_str = ''.join(c for c in hash_str if c.isalnum())
    return hash_str


def trunc_error_msg(e, max_chars=300):
    return (str(e)[:max_chars] + '...') if len(str(e)) > max_chars else str(e)

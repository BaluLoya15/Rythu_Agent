import os
import subprocess
import json
import pytest

def load_translation_dict(rel_path: str):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    full_path = os.path.join(root_dir, rel_path).replace("\\", "/")
    script = f"""
    import dictData from 'file:///{full_path}';
    console.log(JSON.stringify(dictData));
    """
    res = subprocess.run(["node", "--input-type=module", "-e", script], capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(res.stdout)

def get_flattened_keys(d, prefix=""):
    keys = {}
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys.update(get_flattened_keys(v, full_key))
        else:
            keys[full_key] = v
    return keys

def test_translation_key_parity():
    """
    Test 28: TRANSLATION PARITY TEST
    en.js, te.js, hi.js keys must be 100% identical.
    Fail if any key is missing, extra, or has an empty translation.
    """
    en_dict = load_translation_dict("frontend/src/i18n/en.js")
    te_dict = load_translation_dict("frontend/src/i18n/te.js")
    hi_dict = load_translation_dict("frontend/src/i18n/hi.js")

    en_flat = get_flattened_keys(en_dict)
    te_flat = get_flattened_keys(te_dict)
    hi_flat = get_flattened_keys(hi_dict)

    en_keys = set(en_flat.keys())
    te_keys = set(te_flat.keys())
    hi_keys = set(hi_flat.keys())

    # 1. Parity between English and Telugu
    missing_in_te = en_keys - te_keys
    extra_in_te = te_keys - en_keys
    assert not missing_in_te, f"Keys missing in te.js: {missing_in_te}"
    assert not extra_in_te, f"Extra keys in te.js: {extra_in_te}"

    # 2. Parity between English and Hindi
    missing_in_hi = en_keys - hi_keys
    extra_in_hi = hi_keys - en_keys
    assert not missing_in_hi, f"Keys missing in hi.js: {missing_in_hi}"
    assert not extra_in_hi, f"Extra keys in hi.js: {extra_in_hi}"

    # 3. No empty translations
    for k, v in en_flat.items():
        assert isinstance(v, str) and v.strip(), f"Empty translation in en.js for key: {k}"
    for k, v in te_flat.items():
        assert isinstance(v, str) and v.strip(), f"Empty translation in te.js for key: {k}"
    for k, v in hi_flat.items():
        assert isinstance(v, str) and v.strip(), f"Empty translation in hi.js for key: {k}"

    # 4. Strict Product Name invariant across all languages
    assert en_dict["appName"] == "RYTHU AGENT"
    assert te_dict["appName"] == "RYTHU AGENT"
    assert hi_dict["appName"] == "RYTHU AGENT"

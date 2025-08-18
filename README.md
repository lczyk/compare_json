# compare_json

![GitHub Tag](https://img.shields.io/github/v/tag/lczyk/compare_json?label=version)
[![Single file](https://img.shields.io/badge/single%20file%20-%20purple)](https://raw.githubusercontent.com/lczyk/compare_json/main/src/compare_json/compare_json.py)
[![test](https://github.com/lczyk/compare_json/actions/workflows/test.yml/badge.svg)](https://github.com/lczyk/compare_json/actions/workflows/test.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Python versions](https://img.shields.io/badge/python-3.9%20~%203.13-blue)

Single-file Micro JSON Comparison Library to use in tests.

Tested in Python 3.9+.

# Usage

```python
from compare_json import compare_json

def test_basket():
    actual = ...
    expected = {
    "basket": {
        "fruit": [
            "apple",
            "banana",
            "cherry",
        ],
        "full": false,
        "capacity: 10,
    }
    compare_json(actual, expected)
}
```

## Install

Just copy the single-module file to your project and import it.

```bash
cp ./src/compare_json/compare_json.py tests/_compare_json.py
```

Or even better, without checking out the repository:

```bash
curl https://raw.githubusercontent.com/lczyk/compare_json/main/src/compare_json/compare_json.py > tests/_compare_json.py
```

Note that like this *you take stewardship of the code* and you are responsible for keeping it up-to-date. If you change it that's fine (keep the license pls). That's the point here. You can also copy the code to your project and modify it as you wish.

If you want you can also build and install it as a package, but then the source lives somewhere else. That might be what you want though. 🤷‍♀️

```bash
pip install flit
flit build
ls dist/*
pip install dist/*.whl
```

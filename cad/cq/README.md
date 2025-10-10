# Experiment with using CodeQuery

## Installation
seems like the easiest way will be to use `pip` and a python `virtualenv`

### Using Requirements.txt
``` shell
pip install -r requirements.txt
```

### Manual
``` shell
pythom -m venv venv
source venv/bin/activate # for bash shell
source venv/bin/activate.fish # for fish shell

# install package
pip install cadquery

# install gui
pip install CQ-editor
```

## Running Editor

``` shell
CQ-editor
```

for details on using the editor see [CQ-Editor pypi](https://pypi.org/project/CQ-editor/).
(specifically for editing in an external editor like emacs).

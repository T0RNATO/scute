**[View the Github](https://github.com/T0RNATO/scute) or [the PyPi listing](https://pypi.org/project/scutemc/)**
## Usage
Install the package by doing the following:
```bash
pip install scutemc
```
Then, use the package:
```python
from scute.function import func
from scute.items import Item
from scute.commands import give

@func("namespace", "name")
def myFunc():
    give("@s", Item.green_dye)
```
(Please note that it is installed with the name `scutemc` but is imported as `scute`)

Recommended reading to start off: `scute.function`, `scute.items`
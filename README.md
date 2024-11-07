# pyconfyg

Python configuration parser library leveraging python abstract-syntax-tree for extensive customization of configurations.

## Key benefits

- Full flexibility in the configuration file
- No mapping between name and objects/functions required
- Explicit references with import

## Usage

For a configuration file `config.py`:
```
digit = 2
key = "a"
value = {
  "a": 12,
  "b": 42,
}[key]
```

### Load configuration
Loaded configuration is a dictionnay whose keys can be accessed as attributes.
```python
from astconfig import Config
config = Config("config.py")
assert config.value == config['value'] == 12
```

### Runtime overwriting parameters
Configuration can be updated both with configuration string and dict.
```python
config.update({'key': 'b'}) # as dict
assert config.value == 42
config.update("key='a'")    # as string
assert config.value == 12
```

### Dumping configuration back to file
Dumping configuration which has been updated at runtime is usefull for later reproducibility.
```python
import datetime
with open(f"config_{datetime.datetime.now().timestamp()}.py", "w") as fd:
    fd.write(str(config))
```

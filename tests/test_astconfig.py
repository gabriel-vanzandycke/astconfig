from astconfig.core import Config, exec_wrapper

def test_parse_strings_single():
    assert exec_wrapper("a=2") == {'a': 2}

def test_exec_wrapper_multiple():
    assert exec_wrapper(";".join(["a=2", "b=4"])) == {'a': 2, 'b': 4}

def test_exec_wrapper_with_env():
    env = {'c': 3}
    assert exec_wrapper(";".join(["a=2", "b=4"]), env=env) == {'a': 2, 'b': 4, 'c': 3}

def test_exec_wrapper_with_env_overwritten():
    env = {'c': 3}
    assert exec_wrapper("c=10", env=env) == {'c': 10}

def test_exec_wrapper4():
    assert exec_wrapper("a=2\nb=5") == {'a': 2, 'b': 5}

def test_config():
    c = Config("a=2\nb=5")
    assert dict(c) == {'a': 2, 'b': 5}
    assert str(c) == "\na = 2\nb = 5\n"

def test_config_update_dict_with_overwrite():
    c = Config("a=2\nb=5")
    c.update({'b': 2})
    assert dict(c) == {'a': 2, 'b': 2}
    assert str(c) == "\na = 2\nb = 2\n"

def test_config_update_dict_with_unoverwritten():
    c = Config("a=2\nb=5")
    c.update({'c': 2})
    assert dict(c) == {'a': 2, 'b': 5, 'c': 2}
    assert str(c) == "\na = 2\nb = 5\nc = 2\n"

def test_config_update_string_with_overwrite():
    c = Config("a=2\nb=5")
    c.update('b=2')
    assert dict(c) == {'a': 2, 'b': 2}
    assert str(c) == "\na = 2\nb = 2\n"

def test_config_update_string_with_unoverwritten():
    c = Config("a=2\nb=5")
    c.update('c=2')
    assert dict(c) == {'a': 2, 'b': 5, 'c': 2}
    assert str(c) == "\na = 2\nb = 5\nc = 2\n"

def test_config_dict_updated_key_as_string():
    c = Config("key = 'a'\nvalue = {'a': 12, 'b': 42}[key]")
    assert c.value == 12
    c.update("key='b'")
    assert c.value == 42

def test_config_dict_updated_key_as_dict():
    c = Config("key = 'a'\nvalue = {'a': 12, 'b': 42}[key]")
    assert c.value == 12
    c.update({'key': 'b'})
    assert c.value == 42

def test_config_or_operator_with_dict():
    c = Config("key = 'a'\nvalue = {'a': 12, 'b': 42}[key]")
    c2 = c | {'key': 'b'}
    assert isinstance(c2, Config)
    assert c2.value == 42

def test_config_or_operator_with_str():
    c = Config("key = 'a'\nvalue = {'a': 12, 'b': 42}[key]")
    c2 = c | "key='b'"
    assert isinstance(c2, Config)
    assert c2.value == 42

def test_config_or_operator_with_config():
    c = Config("key = 'a'\nvalue = {'a': 12, 'b': 42}[key]")
    c2 = c | Config("key='b'")
    assert isinstance(c2, Config)
    assert c2.value == 42

def test_config_product():
    c = Config("key = 'a'\nvalue = {'a': 12, 'b': 42}[key]")
    cs = list(c.product("key=['a','b']"))
    assert len(cs) == 2
    assert isinstance(cs[0], Config)
    assert cs[0].value == 12
    assert isinstance(cs[1], Config)
    assert cs[1].value == 42

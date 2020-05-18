def test_typevar():
  import pytest
  import re
  from typing import TypeVar
  T = TypeVar('T')

  def add(a: T, b: T) -> T:
    return a + b

  assert add(2, 3) == 5
  assert add('a', 'b') == 'ab'
  with pytest.raises(TypeError, match=re.escape("unsupported operand type(s) for +: 'int' and 'str'")):
    add(1, 'a')


def test_typevar_constraint():
  from typing import TypeVar
  T = TypeVar('T', int, float)

  def add(a: T, b: T) -> T:
    return a + b

  assert add(2, 3) == 5
  add('a', 'b') # 报错: Expected type 'T',got str instead
  add('a', 2) # # 报错: Expected type 'T',got str instead
  add(3, 4.1) # 报错: Expected type 'int' (matched generic type 'T'), got 'float' instead

def test_typevar_text_concat():
  from typing import TypeVar
  import pytest
  import re
  T = TypeVar('T', str, bytes)

  def concat(a: T, b: T) -> T:
    return a + b

  concat('a','b')
  concat(b'a',b'b')
  with pytest.raises(TypeError,match=re.escape(" TypeError: can't concat str to bytes")):
    concat(b'a','b') # 报错:  Expected type 'bytes' (matched generic type 'T'), got 'str' instead


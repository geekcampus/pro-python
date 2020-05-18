# coding: utf-8
from unittest.mock import patch

import pytest
from .biz import gen_practice_seq

__author__ = '代码会说话'

def identity_decorator(func):
  return func


def test_gen_practice_seq(mocker):
  with patch('demos.helper.fake_acquire_lock',new=identity_decorator):
    from demos import biz
    import importlib
    importlib.reload(biz)
    from .helper import fake_acquire_lock
    from .biz import  gen_practice_seq
    assert fake_acquire_lock == identity_decorator
    with pytest.raises(Exception):
      gen_practice_seq()


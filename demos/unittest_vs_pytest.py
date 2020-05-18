# coding: utf-8

__author__ = '代码会说话'

import pytest
from typing import NamedTuple

class User(NamedTuple):
  name:str
  is_admin:bool

@pytest.fixture
def t_admin():
  return User(name="管理员",is_admin=True)

def test_admin_user_can_doxx(t_admin):
  assert t_admin.name == "管理员"
  assert t_admin.is_admin


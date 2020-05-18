# coding: utf-8
from . import helper

@helper.fake_acquire_lock
def gen_practice_seq(practice_id):
    raise Exception("PatchDemo")

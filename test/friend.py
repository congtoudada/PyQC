# coding=utf-8
import random

from pkgs.serialize_decorator import ex_serialize
from pkgs.warm_up_decorator import ex_warm_up


@ex_warm_up
@ex_serialize
class Friend(object):
    __slots__ = ('owner', 'version', 'fid', 'show')

    def __init__(self):
        """
        构造函数只做类型声明和简单初始化，耗时操作放到init中
        """
        self.owner = None  # 用于构建环形依赖
        self.version = "v0.1"  # str
        self.fid = 0  # int
        self.show = []  # list[int]
        self.init()

    def init(self):
        self.fid = random.randint(1, 100)  # int
        self.show = [random.randint(10000, 1000000) for _ in range(10)]

    def from_dict(self, state):
        self.version = state['version']
        self.fid = int(state['fid'])
        self.show = []
        for item in state['show']:
            self.show.append(int(item))
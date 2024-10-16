# coding=utf-8
import os
from abc import ABCMeta, abstractmethod
from copy import deepcopy, copy


class CDOMgr(object):
    """
    CDO管理器抽象类
    """
    __metaclass__ = ABCMeta
    __slots__ = ('cdo_pool', 'cdo_folder', 'cdo_suffix')
    WARM_UP_LIST = []  # 预热列表

    def __init__(self, folder="./", suffix=".pkl"):
        self.cdo_pool = {}  # cdo缓存池
        self.cdo_folder = folder  # cdo序列化文件夹
        self.cdo_suffix = suffix  # cdo序列化文件后缀

    def get_cdo_count(self):
        """
        获取CDO个数
        :return:
        """
        return self.cdo_pool.__len__()

    def is_cdo(self, obj):
        """
        是否包含对象的CDO
        :param obj:
        :return:
        """
        if self.cdo_pool.__contains__(type(obj).__name__):
            return id(obj) == id(self.cdo_pool[type(obj).__name__])

    def get_cdo(self, cls):
        """
        根据类型获取cdo
        :param cls:
        :return:
        """
        if self.cdo_pool.__contains__(cls.__name__):
            return self.cdo_pool[cls.__name__]
        else:
            print("[ get_cdo failed ] cdo_pool not found: " + cls.__name__)
            return None

    def refresh_cdo(self, cdo, with_save=True):
        """
        刷新cdo
        :param cdo:
        :param with_save: 是否包括本地cdo文件
        :return:
        """
        self.cdo_pool[type(cdo).__name__] = cdo
        if with_save:
            return self._save_cdo(cdo)

    def release_cdo(self, cls, with_file=False):
        """
        删除cdo
        :param cls:
        :param with_file: 是否包括本地cdo文件
        :return:
        """
        if with_file:
            fullpath = os.path.join(self.cdo_folder, cls.__name__ + self.cdo_suffix)
            if os.path.exists(fullpath):
                os.remove(fullpath)
        if self.cdo_pool.__contains__(cls.__name__):
            self.cdo_pool.pop(cls.__name__)
        return True

    def save_cdo_cls(self, cls):
        """
        序列化cdo_pool存在的cdo对象到本地
        :param cls:
        :return:
        """
        if self.cdo_pool.__contains__(cls.__name__):
            return self._save_cdo(self.cdo_pool[cls.__name__])
        else:
            print("global_cdo_dict not found: " + cls.__name__)
            return False

    def create(self, cls, *args, **kwargs):
        """
        从cdo中clone一个新对象
        :param cls:
        :return:
        """
        # 1.如果存在cdo，直接从cdo快速深拷贝(速度最快)
        if self.cdo_pool.__contains__(cls.__name__):
            return self._clone(self.cdo_pool[cls.__name__])
        # 2.如果不存在cdo，则尝试加载cdo(速度次之)
        cdo = self._load_cdo(cls)
        # 3.如果加载失败，从构造函数初始化，并保存(速度最慢)
        if cdo is None:
            cdo = cls(*args, **kwargs)
            if hasattr(cdo, 'init'):
                cdo.init(*args, **kwargs)
            # ret = self._save_cdo(cdo)
            # if not ret:
            #     return None
        self.cdo_pool[cls.__name__] = cdo
        return self._clone(self.cdo_pool[cls.__name__])

    def warm_up(self):
        """
        cdo预热
        :return:
        """
        for item in CDOMgr.WARM_UP_LIST:
            if isinstance(item, type):
                print('尝试预热CDO: ' + item.__name__)
                cdo = self._load_cdo(item)
                if cdo is None:
                    print('CDO预热失败: ' + item.__name__)
                else:
                    self.cdo_pool[type(cdo).__name__] = cdo
                    print('CDO预热成功: ' + item.__name__)

    def _clone(self, cdo):
        """
        从cdo拷贝对象并返回
        :param cdo:
        :return:
        """
        return deepcopy(cdo)

    @abstractmethod
    def _save_cdo(self, cdo):
        """
        序列化cdo对象到本地
        :param cdo:
        :return: 成功or失败
        """
        pass

    @abstractmethod
    def _load_cdo(self, cls):
        """
        从本地反序列化成cdo对象
        :param cls:
        :return: cdo对象
        """
        pass
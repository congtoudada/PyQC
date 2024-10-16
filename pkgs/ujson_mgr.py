# coding=utf-8
import random
import types
import sys
import os
import ujson

from copy import copy, deepcopy
from pkgs.cdo_mgr import CDOMgr


class UJsonCDOMgr(CDOMgr):
    __instance = None

    @classmethod
    def getinstance(cls):
        if cls.__instance is None:
            cls.__instance = UJsonCDOMgr()
        return cls.__instance

    def __init__(self):
        super(UJsonCDOMgr, self).__init__(suffix=".ujson")

    def _clone(self, cdo):
        """
        利用序列化替代深拷贝
        :param cdo:
        :return:
        """
        # 存在自定义深拷贝函数，则使用自定义深拷贝
        if hasattr(cdo, "__deepcopy__"):
            obj = cdo.__deepcopy__(self)
        else:  # 否则，通过序列化/反序列化完成对象拷贝
            info_dict = cdo.to_dict()
            obj = copy(cdo)
            obj.from_dict(info_dict)
        return obj

    def _save_cdo(self, cdo):
        """
        cdo序列化到本地
        :param cdo:
        :return:
        """
        if not hasattr(cdo, 'to_dict'):
            print("[ _save_cdo failed ] cdo is not serializable, please provide to_dict")
            return False
        fullpath = os.path.join(self.cdo_folder, type(cdo).__name__ + self.cdo_suffix)
        info_dict = cdo.to_dict()
        data = ujson.dumps(info_dict)
        with open(fullpath, 'w') as f:
            f.write(data)
        return True

    def _load_cdo(self, cls):
        """
        从本地反序列化为cdo
        :param cls:
        :return:
        """
        if not hasattr(cls, 'from_dict'):
            print("[ _load_cdo failed ] cdo is not deserializable, please provide from_dict")
            return None
        fullpath = os.path.join(self.cdo_folder, cls.__name__ + self.cdo_suffix)
        if os.path.exists(fullpath):
            with open(fullpath, 'r') as f:
                data = f.read()  # 读取整个文件内容
                info_dict = ujson.loads(data)
                obj = cls()
                obj.from_dict(info_dict)
                return obj
        else:
            print("[ _load_cdo failed ] Can't find cdo: " + fullpath)
            return None

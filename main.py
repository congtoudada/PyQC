# coding=utf-8
from test.player import Player, compareResult
from pkgs.ujson_mgr import UJsonCDOMgr


def test1():
    """
    验证构造函数生成的对象和CDO构建对象的差异
    :return:
    """
    p = Player("cong tou", level=3)  # 构造一个对象
    p.init()  # 数据初始化（耗时操作）

    ujsonMgr = UJsonCDOMgr.getinstance()  # 创建并获取ujson cdo管理类
    ujsonMgr.refresh_cdo(p, with_save=True)  # 使用p刷新cdo及其缓存
    # 通过cdoMgr生成一个对象
    # -- 1.先从cdo找，如果找到会快速拷贝构建
    # -- 2.再从本地找cdo文件，如果找到会序列化构建
    # -- 3.如果以上均未找到，则调用构造函数构建，同时会尝试调用对象上的init函数(不是__init__)
    p1 = ujsonMgr.create(Player)

    compareResult(p, p1)  # 比较二者差异


def test2():
    """
    CDO相关操作演示
    :return:
    """
    ujsonMgr = UJsonCDOMgr.getinstance()  # 创建并获取ujson cdo管理类
    ujsonMgr.warm_up()  # 预热cdo（在程序启动时调用一次即可，会对所有带@ex_warm_up的类进行预热）

    player_cdo = ujsonMgr.get_cdo(Player)
    # 获取cdo，做一些定制化操作
    # ...

    # 更新全局的CDO，如果想覆盖本地缓存，可以将with_save设为True
    ujsonMgr.refresh_cdo(player_cdo, with_save=True)

    # 通过cdo构建对象
    p1 = ujsonMgr.create(Player)

    # 删除全局的CDO，如果也想删除本地缓存，可以将with_file设为True
    ujsonMgr.release_cdo(Player, with_file=False)


if __name__ == '__main__':
    test1()
    test2()

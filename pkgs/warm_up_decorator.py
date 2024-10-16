from pkgs.cdo_mgr import CDOMgr


def ex_warm_up(cls):
    CDOMgr.WARM_UP_LIST.append(cls)
    return cls

import grp
def get_gid_by_name(name):
    try:
        grpinfo = grp.getgrnam(name)
        return grpinfo.gr_gid
    except:
        return 0
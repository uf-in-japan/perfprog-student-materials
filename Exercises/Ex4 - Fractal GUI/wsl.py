import os


def get_wsl_distro():
    # This should be defined for any WSL distro. If it isn't, we aren't in WSL.
    if 'WSL_DISTRO_NAME' in os.environ:
        return os.environ['WSL_DISTRO_NAME']
    elif 'WSLENV' in os.environ:
        return "Unknown"
    else:
        return None


def get_wsl_host():
    # If we aren't in WSL, return none.
    if not get_wsl_distro():
        return None

    result = None
    # If we're in WSL2...
    if 'WSL_INTEROP' in os.environ:
        with open("/etc/resolv.conf", "r") as resolv_file:
            result = resolv_file.readlines()[-1].split(' ')[1].strip()
            resolv_file.close()
        return result
    # Otherwise, we're in WSL1.
    else:
        return "localhost"


def set_display_to_host(major = 0, minor = None):
    if get_wsl_distro():
        os.environ['DISPLAY'] = (get_wsl_host() + ":%d" % major + (".%d" % minor if minor != None else ""))

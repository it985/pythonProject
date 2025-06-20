#!/usr/bin/env python
# __auther__ = "journey.ad"
# __link__ = "https://github.com/journey-ad/hentai-wallpaper"
import codecs
import configparser
import json
import os
import subprocess
import sys
import time
from datetime import datetime

import requests
from PIL import Image

API = "https://api.imjad.cn/pixiv/v1/"
PATH = os.path.split(os.path.realpath(__file__))[0]
conf = {
    "zenra": os.path.join(PATH, "zenra.jpg"),
    "sukusui": os.path.join(PATH, "sukusui.jpg")
}


def blend_image(image_a, image_b, alpha, path):
    background = Image.open(image_a)
    foreground = Image.open(image_b)

    output = Image.blend(background, foreground, alpha)
    print("Blend over, Save as %s" % path)
    output.save(path, "PNG")


def get_alpha(start_time=19, end_time=7):
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    hours = seconds / 3600

    if hours > start_time:
        alpha = 1 - (hours - start_time) / 5
    elif hours < end_time:
        alpha = 0
    else:
        alpha = 1

    return alpha


def get_img_url(illust_id):
    try:
        params = {
            "type": "illust",
            "id": illust_id
        }
        headers = {
            "User-Agent": "hentai-wallpaper"
        }
        r = requests.get(API, headers=headers, params=params, timeout=20)
        resp = json.loads(r.text)
        if resp["status"] != "success":
            print(resp["errors"]["system"]["message"])
            return None

        page_list = []
        if not resp["response"][0]["metadata"]:
            page_list.append(resp["response"][0]["image_urls"]["large"])
        else:
            pages = resp["response"][0]["metadata"]["pages"]
            for page in pages:
                page_list.append(page["image_urls"]["large"])

        return page_list
    except Exception as err:
        print(illust_id)
        raise err


def download(illust_id, file_name, path=PATH):
    headers = {
        "Referer": "https://www.pixiv.net"
    }
    print("Get illust(%s) page list..." % (illust_id))
    page_list = get_img_url(illust_id)
    for url in page_list:
        file_path = os.path.join(path, file_name)
        print("Downloading... Save as %s" % (file_path))
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if os.path.exists(file_path):
                print("Image exists.")
            else:
                with open(file_path, "wb") as file:
                    file.write(requests.get(url, headers=headers, timeout=30).content)
        except Exception as e:
            raise e


# https://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment/21213358#21213358
def get_desktop_environment():
    # From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    if sys.platform in ["win32", "cygwin"]:
        return "windows"
    elif sys.platform == "darwin":
        return "mac"
    else:  # Most likely either a POSIX system or something not much common
        desktop_session = os.environ.get("DESKTOP_SESSION")
        if desktop_session is not None:  # easier to match if we doesn't have  to deal with caracter cases
            desktop_session = desktop_session.lower()
            if desktop_session in [
                    "gnome", "unity", "cinnamon", "mate", "xfce4", "lxde", "fluxbox", "i3",
                    "blackbox", "openbox", "icewm", "jwm", "afterstep", "trinity", "kde"]:
                return desktop_session
            # Special cases #
            # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
            # There is no guarantee that they will not do the same with the other desktop environments.
            elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                return "xfce4"
            elif desktop_session.startswith("ubuntu"):
                return "unity"
            elif desktop_session.startswith("lubuntu"):
                return "lxde"
            elif desktop_session.startswith("kubuntu"):
                return "kde"
            elif desktop_session.startswith("razor"):  # e.g. razorkwin
                return "razor-qt"
            elif desktop_session.startswith("wmaker"):  # e.g. wmaker-common
                return "windowmaker"
        if os.environ.get("KDE_FULL_SESSION") == "true":
            return "kde"
        elif os.environ.get("GNOME_DESKTOP_SESSION_ID"):
            if "deprecated" not in os.environ.get("GNOME_DESKTOP_SESSION_ID"):
                return "gnome2"
        # From http://ubuntuforums.org/showthread.php?t=652320
        elif is_running("xfce-mcs-manage"):
            return "xfce4"
        elif is_running("ksmserver"):
            return "kde"
    return "unknown"


def is_running(process):
    # From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
    # and http://richarddingwall.name/2009/06/18/windows-equivalents-of-ps-and-kill-commands/
    try:  # Linux/Unix
        s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    except:  # Windows
        s = subprocess.Popen(["tasklist", "/v"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if process in str(x):
            return True
    return False


# https://stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python/21213504#21213504
def set_wallpaper(file_loc, first_run):
    # Note: There are two common Linux desktop environments where
    # I have not been able to set the desktop background from
    # command line: KDE, Enlightenment
    desktop_env = get_desktop_environment()
    try:
        if desktop_env in ["gnome", "unity", "cinnamon"]:
            uri = "'file://%s'" % file_loc
            args0 = ["gsettings", "set", "org.gnome.desktop.background", "picture-options", "zoom"]
            args1 = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri]
            subprocess.Popen(args0)
            subprocess.Popen(args1)
        elif desktop_env == "mate":
            try:  # MATE >= 1.6
                # info from http://wiki.mate-desktop.org/docs:gsettings
                args = ["gsettings", "set", "org.mate.background", "picture-filename", "'%s'" % file_loc]
                subprocess.Popen(args)
            except:  # MATE < 1.6
                # From https://bugs.launchpad.net/variety/+bug/1033918
                args = ["mateconftool-2", "-t", "string", "--set", "/desktop/mate/background/picture_filename", '"%s"' % file_loc]
                subprocess.Popen(args)
        elif desktop_env == "gnome2":  # Not tested
            # From https://bugs.launchpad.net/variety/+bug/1033918
            args = ["gconftool-2", "-t", "string", "--set", "/desktop/gnome/background/picture_filename", '"%s"' % file_loc]
            subprocess.Popen(args)
        # KDE4 is difficult
        # see http://blog.zx2c4.com/699 for a solution that might work
        elif desktop_env in ["kde3", "trinity"]:
            # From http://ubuntuforums.org/archive/index.php/t-803417.html
            args = 'dcop kdesktop KBackgroundIface setWallpaper 0 "%s" 6' % file_loc
            subprocess.Popen(args, shell=True)
        elif desktop_env == "xfce4":
            # From http://www.commandlinefu.com/commands/view/2055/change-wallpaper-for-xfce4-4.6.0
            if first_run:
                args0 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace0/last-image", "-s", file_loc]
                args1 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-path", "-s", file_loc]
                args2 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-style", "-s", "3"]
                args3 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-show", "-s", "true"]
                subprocess.Popen(args0)
                subprocess.Popen(args1)
                subprocess.Popen(args2)
                subprocess.Popen(args3)
            args = ["xfdesktop", "--reload"]
            subprocess.Popen(args)
        elif desktop_env == "razor-qt":  # TODO: implement reload of desktop when possible
            if first_run:
                desktop_conf = configparser.ConfigParser()
                # Development version
                desktop_conf_file = os.path.join(get_config_dir("razor"), "desktop.conf")
                if os.path.isfile(desktop_conf_file):
                    config_option = r"screens\1\desktops\1\wallpaper"
                else:
                    desktop_conf_file = os.path.join(get_home_dir(), ".razor/desktop.conf")
                    config_option = r"desktops\1\wallpaper"
                desktop_conf.read(os.path.join(desktop_conf_file))
                try:
                    if desktop_conf.has_option("razor", config_option):  # only replacing a value
                        desktop_conf.set("razor", config_option, file_loc)
                        with codecs.open(desktop_conf_file, "w", encoding="utf-8", errors="replace") as f:
                            desktop_conf.write(f)
                except:
                    pass
            else:
                # TODO: reload desktop when possible
                pass
        elif desktop_env in ["fluxbox", "jwm", "openbox", "afterstep"]:
            # http://fluxbox-wiki.org/index.php/Howto_set_the_background
            # used fbsetbg on jwm too since I am too lazy to edit the XML configuration
            # now where fbsetbg does the job excellent anyway.
            # and I have not figured out how else it can be set on Openbox and AfterSTep
            # but fbsetbg works excellent here too.
            try:
                args = ["fbsetbg", file_loc]
                subprocess.Popen(args)
            except:
                print("ERROR: Failed to set wallpaper with fbsetbg!\n")
                print("Please make sre that You have fbsetbg installed.\n")
        elif desktop_env == "icewm":
            # command found at http://urukrama.wordpress.com/2007/12/05/desktop-backgrounds-in-window-managers/
            args = ["icewmbg", file_loc]
            subprocess.Popen(args)
        elif desktop_env == "blackbox":
            # command found at http://blackboxwm.sourceforge.net/BlackboxDocumentation/BlackboxBackground
            args = ["bsetbg", "-full", file_loc]
            subprocess.Popen(args)
        elif desktop_env == "lxde":
            args = "pcmanfm --set-wallpaper %s --wallpaper-mode=scaled" % file_loc
            subprocess.Popen(args, shell=True)
        elif desktop_env == "windowmaker":
            # From http://www.commandlinefu.com/commands/view/3857/set-wallpaper-on-windowmaker-in-one-line
            args = "wmsetbg -s -u %s" % file_loc
            subprocess.Popen(args, shell=True)
        elif desktop_env == "windows":  # Not tested since I do not run this on Windows
            # From https://stackoverflow.com/questions/1977694/change-desktop-background
            import ctypes
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, file_loc, 0)
        elif desktop_env == "mac":  # work on 10.12 Beta (16A238m)
            # From https://github.com/xyangk/EarthLiveSharp/blob/013a87e0baa07230bd19d2c51fafd64e475cdd48/mac_os_x/wallpaper.py#L105-L114
            try:
                from appscript import app, mactypes
                app("Finder").desktop_picture.set(mactypes.File(file_loc))
            except ImportError:
                SCRIPT = """/usr/bin/osascript<<END
                tell application "System Events"
                    set desktopCount to count of desktops
                    repeat with desktopNumber from 1 to desktopCount
                        tell desktop desktopNumber
                            set picture to "%s"
                        end tell
                    end repeat
                end tell
END"""
                subprocess.Popen(SCRIPT % file_loc, shell=True)
        # NOT TESTED BELOW - don't want to mess things up ##
        elif desktop_env == "enlightenment":  # I have not been able to make it work on e17. On e16 it would have been something in this direction
            args = "enlightenment_remote -desktop-bg-add 0 0 0 0 %s" % file_loc
            subprocess.Popen(args, shell=True)
        elif desktop_env == "i3":
            # https://faq.i3wm.org/question/6/how-can-i-set-a-desktop-background-image-in-i3/#post-id-8
            # you need to install feh manually.
            try:
                args = ["feh", "--bg-scale", file_loc]
                subprocess.Popen(args)
            except:
                print("ERROR: Failed to set wallpaper with feh!\n")
                print("Please make sre that You have feh installed.\n")
        else:
            if first_run:  # don"t spam the user with the same message over and over again
                print("Warning: Failed to set wallpaper. Your desktop environment is not supported.")
                print("You can try manually to set Your wallpaper to %s" % file_loc)
            return False
        print("Done.")
        return True
    except:
        print("ERROR: Failed to set wallpaper. There might be a bug.\n")
        return False


def get_config_dir(app_name):
    if "XDG_CONFIG_HOME" in os.environ:
        confighome = os.environ["XDG_CONFIG_HOME"]
    elif "APPDATA" in os.environ:  # On Windows
        confighome = os.environ["APPDATA"]
    else:
        try:
            from xdg import BaseDirectory
            confighome = BaseDirectory.xdg_config_home
        except ImportError:  # Most likely a Linux/Unix system anyway
            confighome = os.path.join(get_home_dir(), ".config")
    configdir = os.path.join(confighome, app_name)
    return configdir


def get_home_dir():
    if sys.platform == "cygwin":
        home_dir = os.getenv("HOME")
    else:
        home_dir = os.getenv("USERPROFILE") or os.getenv("HOME")
    if home_dir is not None:
        return os.path.normpath(home_dir)
    else:
        raise KeyError("Neither USERPROFILE or HOME environment variables set.")


if __name__ == "__main__":
    first_run = True
    while True:
        if not os.path.exists(conf["zenra"]):
            download(66184094, conf["zenra"])
        if not os.path.exists(conf["sukusui"]):
            download(66183927, conf["sukusui"])
        alpha = get_alpha(19, 7)
        print("Alpha is %s" % alpha)
        path = os.path.join(PATH, "output.png")
        blend_image(conf["zenra"], conf["sukusui"], alpha, path)
        set_wallpaper(path, first_run)
        first_run = False
        time.sleep(120)

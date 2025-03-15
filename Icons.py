"""
A File Icon Installer
"""

import os
import sublime
import sublime_plugin
import urllib.request
import threading

ICONS_PACKAGE = "A File Icon"
PKGCTRL_SETTINGS = "Package Control.sublime-settings"
PKGCTRL_URL = "https://packagecontrol.io/Package Control.sublime-package"
PKGCTRL_PATH = os.path.join(sublime.installed_packages_path(), "Package Control.sublime-package")

THEME_NAME = os.path.splitext(
    os.path.basename(os.path.dirname(__file__))
)[0]

MSG = """\
<div id="afi-installer">
  <style>
    #afi-installer {{
      padding: 1rem;
      line-height: 1.5;
    }}
    #afi-installer code {{
      background-color: color(var(--background) blend(var(--foreground) 80%));
      line-height: 1;
      padding: 0.25rem;
    }}
    #afi-installer a {{
      padding: 0;
      margin: 0;
    }}
  </style>

  {} requires <code>A File Icon</code> package for enhanced<br>support of
  the file-specific icons.
  <br><br>Would you like to install it?<br>
  <br><a href="install">Install</a> <a href="cancel">Cancel</a>
</div>
""".format(THEME_NAME)


def is_installed():
    pkgctrl_settings = sublime.load_settings(PKGCTRL_SETTINGS)
    installed_packages = set(pkgctrl_settings.get("installed_packages", []))
    return ICONS_PACKAGE in installed_packages
    
def install_package_control():
    """Instala Package Control si no está presente."""
    if not os.path.exists(PKGCTRL_PATH):
        print("Package Control not found. Installing...")
        try:
            urllib.request.urlretrieve(PKGCTRL_URL, PKGCTRL_PATH)
            sublime.status_message("Package Control installed. Please restart Sublime Text.")
        except Exception as e:
            sublime.error_message("Failed to install Package Control: {}".format(e))
    else:
        print("Package Control is already installed.")


def install_package():
    """Instala el paquete A File Icon usando Package Control."""
    try:
        from package_control.package_manager import PackageManager
        manager = PackageManager()
        manager.install_package(ICONS_PACKAGE)
        sublime.status_message("{} installed successfully!".format(ICONS_PACKAGE))
    except Exception as e:
        sublime.error_message("Failed to install {}: {}".format(ICONS_PACKAGE, e))


def on_navigate(href):
    if href.startswith("install"):
        install()
    else:
        hide()


def install():
    install_package_control()
    sublime.set_timeout(lambda: install_package(), 1000)
    hide()

def hide():
    sublime.active_window().active_view().hide_popup()


def plugin_loaded():
    from package_control import events

    if events.install(THEME_NAME) and not is_installed():
        window = sublime.active_window()
        view = window.active_view()
        window.focus_view(view)
        row = int(view.rowcol(view.visible_region().a)[0] + 1)
        view.show_popup(
            MSG,
            location=view.text_point(row, 5),
            max_width=800,
            max_height=800,
            on_navigate=on_navigate
        )

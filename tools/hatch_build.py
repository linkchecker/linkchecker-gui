# Copyright (C) 2022-2023 Chris Mayo
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from pathlib import Path
import re
import shutil
import subprocess

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import markdown2

HELP_DIR = ("linkcheck_gui", "data", "help")
RELEASE_PY = ("linkcheck_gui", "_release.py")
HELP_SRC_DIR = ("doc", "html")


class CustomBuildHook(BuildHookInterface):
    def clean(self, versions):
        Path(*RELEASE_PY).unlink(missing_ok=True)
        shutil.rmtree(str(Path(*HELP_DIR)), ignore_errors=True)

    def initialize(self, version, build_data):
        cp = None
        committer_date = committer_year = "unknown"
        try:
            cp = subprocess.run(["git", "log", "-n 1", "HEAD", "--format=%cs"],
                                capture_output=True, check=True, text=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            # support building wheel from sdist
            if Path(*RELEASE_PY).is_file():
                self.app.display_warning("_release.py already exists")
                return

            try:
                git_archival = Path(".git_archival.txt").read_text()
            except FileNotFoundError:
                self.app.display_warning(".git_archival.txt does not exist")
            else:
                rematch = re.search(r"node-date: ((\d{4})-\d{2}-\d{2})", git_archival)
                if rematch:
                    committer_date = rematch.group(1)
                    committer_year = rematch.group(2)
                else:
                    self.app.display_warning("node-date not substituted")
        else:
            if cp and cp.stdout:
                committer_date = cp.stdout.strip()
                committer_year = committer_date[:4]

        Path(*RELEASE_PY).write_text(f"""\
__app_name__ = "{self.metadata.core.raw_name}"
__version__ = "{self.metadata.version}"
__release_date__ = "{committer_date}"
__copyright_year__ = "{committer_year}"
__author__ = "{self.metadata.core.authors[0]['name']}"
__url__ = "{self.metadata.core.urls["Homepage"]}"
""")

        index_html = (Path(*HELP_SRC_DIR, "html.header").read_text()
                      + markdown2.markdown_path(str(Path(*HELP_SRC_DIR, "index.txt")))
                      + Path(*HELP_SRC_DIR, "html.footer").read_text())
        Path(*HELP_SRC_DIR, "index.html").write_text(index_html)

        try:
            cp = subprocess.run(
                ["pkg-config", "--variable=libexecdir", "Qt6Help"],
                capture_output=True, text=True)
            help_exec_dir = cp.stdout.strip()
        except FileNotFoundError:
            self.app.display_warning("pkg-config not installed")
            help_exec_dir = None
        if help_exec_dir:
            help_generator = Path(help_exec_dir, "qhelpgenerator")
        else:
            # Ubuntu 22.04 doesn't provide Qt6Help.pc, 22.10 does but without libexecdir
            # qhelpgenerator found in bin on 22.04, libexec from 22.10
            help_generator = shutil.which(
                "qhelpgenerator",
                path="/usr/lib/qt6/libexec/:/usr/lib64/qt6/libexec/:"
                     "/usr/lib/qt6/bin/:/usr/lib64/qt6/bin/")

        cp = subprocess.run(
            [help_generator, "-c", "lccollection.qhcp", "-o", "lccollection.qhc"],
            cwd=Path(*HELP_SRC_DIR), check=True)

        Path(*HELP_DIR).mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(*HELP_SRC_DIR, "lcdoc.qch"), Path(*HELP_DIR))
        shutil.copy(Path(*HELP_SRC_DIR, "lccollection.qhc"), Path(*HELP_DIR))

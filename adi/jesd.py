# Copyright (C) 2020 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import fs


class jesd:
    """ JESD Monitoring """

    def __init__(self, address, username="root", password="analog"):
        if "ip:" in address:
            address = address[3:]
        self.address = address
        self.username = username
        self.password = password
        self.rootdir = "/sys/bus/platform/devices/"
        # Connect
        self.fs = fs.open_fs(
            "ssh://{}:{}@{}/".format(self.username, self.password, self.address)
        )
        self.find_jesd_dir()

    def find_jesd_dir(self):
        dirs = self.fs.listdir(self.rootdir)
        self.dirs = []
        for dir in dirs:
            if "jesd" in dir:
                self.dirs.append(dir)

    def decode_status(self, status):
        status = status.split("\n")
        link_status = dict()
        for s in status:
            if ":" in s:
                o = s.split(":")
                link_status[o[0]] = o[1].strip()
            if "Link is" in s:
                link_status["enabled"] = s.split(" ")[-1].strip()

        return link_status

    def get_status(self, dir):
        return self.fs.gettext(self.rootdir + dir + "/status")

    def get_all_links_statuses(self):
        statuses = dict()
        for dir in self.dirs:
            # name = dir.split(".")[1]
            statuses[dir] = self.decode_status(self.get_status(dir))
        return statuses
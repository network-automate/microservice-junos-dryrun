# -*- coding: utf-8 -*-

#
# Copyright (c) 2017-2018, Juniper Networks Inc. All rights reserved.
#
# License: Apache 2.0
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# * Neither the name of the Juniper Networks nor the
#   names of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Juniper Networks, Inc. ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Juniper Networks, Inc. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import absolute_import, division, print_function

# Standard library imports
import os.path
import sys

# The module_utils path must be added to sys.path in order to import
# juniper_junos_common. The module_utils path is relative to the path of this
# file.
module_utils_path = os.path.normpath(os.path.dirname(__file__) +
                                     '/../module_utils')
if module_utils_path is not None:
    sys.path.insert(0, module_utils_path)
    import juniper_junos_common
    del sys.path[0]


# Use the custom behavior of JuniperJunosActionModule as the superclass of
# our ActionModule.
class ActionModule(juniper_junos_common.JuniperJunosActionModule):
    """Translates junos_rollback args to juniper_junos_config args.

    This class is a subclass of JuniperJunosActionModule. It exists solely
    for backwards compatibility. It translates the arguments from the old
    junos_rollback module into the arguments on the new
    juniper_junos_config module.
    """
    def run(self, tmp=None, task_vars=None):
        rollback = self._task.args.get('rollback')
        if rollback is None:
            # rollback is mandatory when called as junos_rollback.
            # Mimic this behavior be setting rollback to 'value not specified'.
            self._task.args['rollback'] = 'value not specified'
        # Always commit changes to mimic the previous behavior
        self._task.args['commit_empty_changes'] = True

        # Remaining arguments can be passed through transparently.

        # Call the parent action module.
        return super(ActionModule, self).run(tmp, task_vars)

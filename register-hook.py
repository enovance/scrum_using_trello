#!/usr/bin/env python
#
# Copyright (C) 2014 eNovance SAS <licensing@enovance.com>
#
# Author: Frederic Lepied <frederic.lepied@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
'''

import sys

import trellolib

if len(sys.argv) != 3:
    print('Usage: %s <board name> <url>' % sys.argv[0])
    sys.exit(1)

client = trellolib.init_client()

(board,) = trellolib.lookup_boards(client, sys.argv[1])

print client.create_hook(sys.argv[2], board.id)

# register-hook.py ends here

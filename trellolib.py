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

import os
import re
import sys

import trello

_NAME_REGEXP = re.compile('(\([0-9]+\)\s*)(.*)')


def init_client():
    for key in ('TRELLO_API_KEY', 'TRELLO_TOKEN'):
        if not key in os.environ:
            print('env variable %s not set. Aborting' % key)
            sys.exit(1)

    return trello.TrelloClient(os.environ['TRELLO_API_KEY'],
                               token=os.environ['TRELLO_TOKEN'])


def filter_name(name):
    res = _NAME_REGEXP.search(name)
    if res:
        return res.group(2).split(' ', 2)[0]
    else:
        return name.split(' ', 2)[0]


def lookup_boards(client, *names):
    ret = []
    boards = client.list_boards()
    for name in names:
        for board in boards:
            if board.name == name:
                ret.append(board)
                break
        else:
            ret.append(None)
    return ret


def lookup_checklist(name, card):
    for checklist in card.checklists:
        if checklist.name == name:
            return checklist
    return None


def lookup_list(name, board):
    for lst in board.open_lists():
        if lst.name == name:
            return lst
    return None


def lookup_card_by_url(url, board):
    for card in board.open_cards():
        if card.url == url:
            return card
    return None


def lookup_item(name, checklist):
    for item in checklist.items:
        if item['name'] == name:
            return item
    return None

# trellolib.py ends here

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

import re
import sys

import trellolib

_NAME_REGEXP = re.compile('(\([0-9]+\)\s*)(.*)')


def filter_name(name):
    res = _NAME_REGEXP.search(name)
    if res:
        return res.group(2).split(' ', 2)[0]
    else:
        return name.split(' ', 2)[0]


def process_board(board_name):
    client = trellolib.init_client()
    
    sprint_backlog = None
    sprint_task_lists = []
    
    (board,) = trellolib.lookup_boards(client, board_name)
    
    if not board:
        print('unable to find board "%s"' % board_name)
        sys.exit(1)
    
    for lst in board.open_lists():
        if lst.name == 'User Stories':
            sprint_backlog = lst
        elif lst.name.find('Stories') == -1:
            sprint_task_lists.append(lst)
    
    if not sprint_backlog:
        print('No "User Stories" list. Aborting.')
        sys.exit(1)
    
    stories = {}
    
    for card in sprint_backlog.list_cards():
        card.fetch()
        stories[filter_name(card.name)] = card
    
    for lst in sprint_task_lists:
        for card in lst.list_cards():
            us_name = card.name.split(' ')[0]
            try:
                item = None
                task_list = None
                checked = lst.name in ('Done', 'Rejected')
                task_list = trellolib.lookup_checklist('Tasks',
                                                       stories[us_name])
                if task_list:
                    item = trellolib.lookup_item(card.url, task_list)
                if not item:
                    print('%s not in the Tasks checklist of %s, adding it' %
                          (card.name, us_name))
                    if not task_list:
                        print('Creating the Tasks checklist in %s' % us_name)
                        task_list = stories[us_name].add_checklist('Tasks',
                                                                   [card.url, ])
                    else:
                        task_list.add_checklist_item(card.url)
                    item = trellolib.lookup_item(card.url, task_list)
                if item:
                    if item['checked'] != checked:
                        task_list.set_checklist_item(item['name'], checked)
                        print('Set the checked state of %s to %s' %
                              (card.name, checked))
            except KeyError:
                print('Card "%s" not associated with a User Strory (%s)' %
                      (card.name, card.url))

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: %s <board name>' % sys.argv[0])
        sys.exit(1)

    process_board(sys.argv[1])

# sprintboard.py ends here

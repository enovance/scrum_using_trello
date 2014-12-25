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
    print('Usage: %s <grooming board name> <sprint board name>' % sys.argv[0])
    sys.exit(1)

client = trellolib.init_client()

grooming_board = None
sprint_board = None

grooming_board, sprint_board = trellolib.lookup_boards(client,
                                                       sys.argv[1],
                                                       sys.argv[2])

if not grooming_board:
    print('No grooming board named "%s"' % sys.argv[1])
    sys.exit(1)

if not sprint_board:
    print('No sprint board named "%s"' % sys.argv[2])
    sys.exit(1)

source_list = trellolib.lookup_list('Sprint Ready',
                                    grooming_board)

if not source_list:
    print('No list named "Sprint Ready" in board "%s"' % sys.argv[1])
    sys.exit(1)

target_list = (trellolib.lookup_list('User Stories', sprint_board) or
               sprint_board.add_list('User Stories'))

# cleanup the finished stories

for card in target_list.list_cards():
    card.fetch()
    task_checklist = trellolib.lookup_checklist('Tasks', card)
    if not task_checklist:
        continue
    all_checked = True
    for item in task_checklist.items:
        if not item['checked']:
            all_checked = False
            break
    if all_checked:
        for item in task_checklist.items:
            task_card = trellolib.lookup_card_by_url(item['name'],
                                                     sprint_board)
            if task_card:
                print('Closing %s' % task_card.name)
                task_card.set_closed(True)
        print('Closing %s' % card.name)
        card.set_closed(True)

# move stories

for card in source_list.list_cards():
    card.fetch()
    tasks_checklist = trellolib.lookup_checklist('Tasks', card)
    if tasks_checklist:
        print('Renaming "Tasks" checklist to "Prepared Tasks" ' +
              'in user story "%s"'
              % (card.name, ))
        tasks_checklist.rename('Prepared Tasks')
    print('Moving user story "%s" to board "%s"' % (card.name, sys.argv[2]))
    card.change_board(sprint_board.id, target_list.id)

# create task cards

todo_list = trellolib.lookup_list('To Do', sprint_board)
if todo_list:
    for card in target_list.list_cards():
        card.fetch()
        tasks_checklist = trellolib.lookup_checklist('Prepared Tasks', card)
        if tasks_checklist:
            id = trellolib.filter_name(card.name)
            for item in tasks_checklist.items:
                task_name = id + ' ' + item['name']
                print('Created task card "%s" in "%s" sprint board' %
                      (task_name, sprint_board.name))
                todo_list.add_card(task_name)
            tasks_checklist.delete()
else:
    print('No "To Do" list on the "%s" sprint board' % sprint_board.name)

# groomingboard.py ends here

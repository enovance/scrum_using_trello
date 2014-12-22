===============================
Automate SCRUM boards in Trello
===============================

This is a set of python scripts to automate the management of SCRUM
boards in Trello.

The system is based on the following conventions:

* 2 boards are used: one for grooming the backlog and the other for
  the current sprint.
* The Grooming board must have a ``Sprint Ready`` list where the
  stories for the next sprint stay.
* The Sprint board must have the following lists:

  * An ``User Stories`` list which stores all the user stories.
  * All the other lists are made for managing tasks. The cards
    representing tasks must have the name of the related user story in
    the beginning of their title.
  * The tasks are synchronized with lists in the user stories card
    named ``Tasks``. When a task is moved to a list called ``Done`` or
    ``Rejected``, the corresponding item is checked in the user story
    card else the item is unchecked.
    
* user story and task cards must have an uniq id as the first word of
  the title for the system to manage association between tasks and
  user stories. This id may be preceded by evaluation point for the
  user story between parenthesis to be compatible with
  http://scrumfortrello.com/.

Pre-requesites
**************

The Python scripts are using the py-trello module. Install it by doing:

``pip install 'git+https://github.com/sarumont/py-trello.git#egg=py-trello'``

You also need to set the ``TRELLO_API_KEY`` and ``TRELLO_TOKEN``
environment variables.

Grooming board
**************

You need to run ``./groomingboard.py <Grooming Board name> <Sprint Board name>``
to close the finished stories from the sprint board and move the stories that
are in the ``Sprint Ready`` list of the grooming board.

Sprint board
************

You can run periodically the ``./sprintboard.py <Board name>`` command
to synchronized the user stories Tasks list and the status of the task
cards.

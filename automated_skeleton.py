"""Skeleton for automation script


globals passed are:
`num_cpus` number of available CPUs
`num_ram_pages` number of pages that fit on RAM
`num_swap_pages` number of pages that fit on SWAP


the event type passed are one of the following:
'IO_QUEUE'
'PAGE_NEW'
'PAGE_USE'
'PAGE_SWAP'
'PAGE_FREE'
'PROC_NEW'
'PROC_CPU'
'PROC_STARV'
'PROC_WAIT_IO'
'PROC_WAIT_PAGE'
'PROC_TERM'
'PROC_KILL'

a process is identified by its PID

a memory page are identified by the owner's PID
and an index IDX inside the process
(first page is idx=0, second page is idx=1, etc...)

the game expects a callable `run_os`, that takes as argument
the list of events generated by the game objects (processes, pages, etc...)
and expects another list of action events to be returned

see `src/lib/event_manager.py` for more info on events generated
"""



class RunOs:
    """Object oriented skeleton for automation script

    this implements a `__call__` method that should be exposed
    to the game. This method then routes the events to the handlers.

    The handlers should be in the form of `handle_<EVENT_TYPE>`
    (it's similar to http.server.BaseHTTPRequestHandler).

    The helper functions `move_*` and `do_io` will append events
    to the list that shall be sent back to the game.
    """

    # recommended to keep track of processes
    procs = []
    in_cpu = []
    wait_io = []
    wait_page = []

    # recommended to keep track of pages
    ram_pages = []
    swap_pages = []

    _event_queue = []

    def move_page(self, pid, idx):
        """create a move page event"""
        self._event_queue.append({
            'type': 'page',
            'pid': pid,
            'idx': idx
        })

    def move_process(self, pid):
        """create a move process event"""
        self._event_queue.append({
            'type': 'process',
            'pid': pid
        })

    def do_io(self):
        """create a process io event"""
        self._event_queue.append({
            'type': 'io_queue'
        })

    def __call__(self, events: list):
        """Entrypoint from game

        will dispatch each event to the respective handler,
        collecting action events to send back to the game,
        if a handler doesn't exist, will ignore that event.
        """
        self._event_queue.clear()
        for event in events:
            handler = getattr(self, f"handle_{event.etype}", None)
            if handler is not None:
                handler(event)
        return self._event_queue

    #
    # implement those below
    #

    def handle_IO_QUEUE(self, event):
        """IO Queue has new count

        triggered when the IO count in the IO queue has changed

        event:
            .io_count: number of IO waiting to be dispatched
        """

    def handle_PAGE_NEW(self, event):
        """A new memory page was created

        triggered when a process creats a new page, may be in swap

        event:
            .pid: id of the owner process
            .idx: index of page in process
            .swap: bool, if page is in swap
            .use: bool, if page is in use
        """

    def handle_PAGE_USE(self, event):
        """A page 'use' flag has changed

        triggered when either a page was not is use and is now
        in use
        or the page was in use and is now _not_ in use

        this usually comes from a process being moved into or out of
        the CPU

        event:
            .pid: id of the owner process
            .idx: index of page in process
            .use: bool, if page is in use
        """

    def handle_PAGE_SWAP(self, event):
        """A page was swapped

        this happens mostly as a response from a swap request

        event:
            .pid: id of the owner process
            .idx: index of page in process
            .swap: bool, where it is now
        """

    def handle_PAGE_FREE(self, event):
        """A page is freed

        this is triggered when a process is terminated

        event:
            .pid: id of the owner process
            .idx: index of page in process
        """

    def handle_PROC_NEW(self, event):
        """A new process is created

        this happens mostly as the game goes on,
        the initial starvation level is 1 (it starts at 0)

        event:
            .pid: id of the process
        """

    def handle_PROC_CPU(self, event):
        """A process was moved into or out of a CPU

        this happens mostly as a response from a process
        move action

        event:
            .pid: id of the process
            .cpu: bool, if is in CPU or not
        """

    def handle_PROC_STARV(self, event):
        """A process' starvation level has changed

        this is either increasing because it doesn't have
        processing time,
        or the process was on the CPU

        event:
            .pid: id of the process
            .starvation_level: the new starvation level
        """

    def handle_PROC_WAIT_IO(self, event):
        """A process wait (IO) status has changed

        this happens either randomly (blocking)
        or an IO event has been processed

        event:
            .pid: id of the process
            .waiting_for_io: bool, the new waiting status
        """

    def handle_PROC_WAIT_PAGE(self, event):
        """A process wait (for PAGE) status has changed

        this happens either because the process was scheduled
        and a memory page is in SWAP (a page can be created into SWAP)
        or it is not longer waiting

        event:
            .pid: id of the process
            .waiting_for_page: bool, the new waiting status
        """

    def handle_PROC_TERM(self, event):
        """A process was succesfully terminated

        this happens randomly when a process is in the CPU,

        after being moved from the CPU, the process will disappear

        event:
            .pid: id of the process
        """

    def handle_PROC_KILL(self, event):
        """A process was killed by the user

        this happens if the starvation level is too high (level 5, 0 based)

        the process disappeared from the process list

        event:
            .pid: id of the process
        """


#
# the main entrypoint to run the scheduler
#
# it expects a callable `run_os`
#
# it receives a list of events generated from processes/pages
# see `src/lib/event_manager` for generated events
#
# it should return a list of events to happen
#

run_os = RunOs()

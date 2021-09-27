import os
from abc import ABC, abstractmethod
from collections import defaultdict
from fractions import Fraction


import typing
if typing.TYPE_CHECKING:
    from litemake.compile.graph import CompilationFileNode

from .printer import Color, get_terminal_width
from litemake.compile.status import NodeCompilationStatus


class ProgressPrinter(ABC):

    @abstractmethod
    def register_status(self,
                        node: 'CompilationFileNode',
                        status: 'NodeCompilationStatus',
                        ) -> None:
        """ A method that by the main script after a node has been parsed and
        worked on. """

    @abstractmethod
    def __str__(self) -> str:
        """ Generates a string that is supposed to be printed to the console
        while litemake is compiling a target. This string should provide useful
        information to the user about the recent nodes that have been compiled.
        You can assume that this method is called and the returned string is
        printed to the console after each new node that is compiled. """


class DefaultProgressPrinter(ProgressPrinter):

    def __init__(self,
                 total_nodes: int,
                 outdated_nodes: int,
                 ) -> None:
        self._total = total_nodes
        self._outdates = outdated_nodes
        self._history = dict()
        self._history_order = list()
        self._status_counter = defaultdict(int)

    def register_status(self,
                        node: 'CompilationFileNode',
                        status: 'NodeCompilationStatus',
                        ) -> None:
        self._history[node] = status
        self._history_order.append(node)
        self._status_counter[status] += 1

    def _generate_header(self,) -> str:
        """ Generates and returns a line (string) that contains information
        and counters of all nodes that have been compiled up to this point. """

        s = Color.BOLD  # header should be bold.
        s += ', '.join((
            f'{status.color}{self._status_counter[status]} {status.title.upper()}'
            for status in NodeCompilationStatus.registered_statuses()
        ))
        return s + Color.RESET + '\u001b[K'  # clear line from cursor to end

    def __generate_blocks(self, amount: int) -> str:
        """ A helper method that generates and returns the 'blocks' part of the
        progress bar. """

        blocks_pre_node = Fraction(amount, self._outdates)
        block_space = Fraction()
        block_status = None
        processed_blocks = 0

        s = str()

        for node in self._history_order:
            status: 'NodeCompilationStatus' = self._history[node]

            if not block_status or block_status.priority < status.priority:
                block_status = status

            block_space += blocks_pre_node
            if block_space >= 1:
                blocks = int(block_space)
                processed_blocks += blocks
                block_space -= blocks
                s += block_status.color + ('■' * blocks)
                block_status = None

        s += Color.RESET
        s += '□' * (amount - processed_blocks)
        return s

    def _generate_progress_bar(self,) -> str:
        """ Returns a string that displays a nice progress bar with the current
        progress of the compilation. The progress bar is a single line that fits
        to the width of the terminal. """

        precompiled = self._total - self._outdates
        start_precentage = int(precompiled / self._total * 100)
        start = f'{start_precentage:>3}% '

        proccessed = precompiled + len(self._history)
        current_precentage = int(proccessed / self._total * 100)
        end = f' {current_precentage:>3}%'

        blocks_amount = max((0, get_terminal_width() - len(start + end)))

        blocks = self.__generate_blocks(blocks_amount)
        return start + blocks + end

    def __str__(self) -> str:
        s = str()
        if len(self._history) > 1:
            # If we already printed some data before, to overwrite the previous
            # data, move 2 lines up.
            s += '\u001b[F' * 2

        s += self._generate_header() + '\n'
        s += self._generate_progress_bar()

        return s

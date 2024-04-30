from abc import ABC, abstractmethod

from board import Board


class GameManager(ABC):
    @abstractmethod
    def __init__(self, board: Board) -> None:
        self.board: Board = board

    @abstractmethod
    def reset_board(self) -> None:
        pass

    @abstractmethod
    def make_move(self, move) -> None:
        pass

    @abstractmethod
    def unmake_move(self, move) -> None:
        pass

    @abstractmethod
    def find_legal_moves(self) -> list:
        pass

    @abstractmethod
    def check_win(self) -> int:
        pass


class Adversary:
    def __init__(self, manager: GameManager):
        self.manager: GameManager = manager

    # Возвращает текущую оценку позиции. Чем меньше ходов до победы - тем выше оценка.
    def search(self, depth: int, alpha=float('-infinity'), beta=float('+infinity')) -> float:
        if depth == 0:
            return 0

        win = self.manager.check_win()
        if win:
            return win + depth

        available_moves = self.manager.find_legal_moves()

        if not available_moves:
            return 0

        for cell in available_moves:
            self.manager.make_move(cell)

            evaluation = -self.search(depth - 1, -beta, -alpha)

            self.manager.unmake_move(cell)

            if evaluation >= beta:
                return beta

            if evaluation > alpha:
                alpha = evaluation

        return alpha

    # Возвращает лучший ход для текущего игрока.
    def search_root(self, depth: int) -> int:
        moves: list[int] = self.manager.find_legal_moves()
        best_eval = float('-infinity')
        best_move = None

        for move in moves:
            self.manager.make_move(move)

            evaluation = self.search(depth - 1)

            self.manager.unmake_move(move)

            if evaluation > best_eval:
                best_eval = evaluation
                best_move = move
        return best_move

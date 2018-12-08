import pygame
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_cell_list(self, cell_list: "CellList") -> None:
        x = 0
        y = 0
        for cell in cell_list:
            if cell.is_alive():
                pygame.draw.rect(self.screen, pygame.Color('green'), [x, y, self.cell_size, self.cell_size])
            else:
                pygame.draw.rect(self.screen, pygame.Color('white'), [x, y, self.cell_size, self.cell_size])
            x += self.cell_size
            if x >= self.width:
                y += self.cell_size
                x = 0

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        cell_list = CellList(self.cell_height, self.cell_width, randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(cell_list)
            cell_list.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row: int, col: int, state: bool=False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> bool:
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize: bool=False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self.grid = []
        for i in range(nrows):
            line = []
            for j in range(ncols):
                if randomize:
                    line.append(Cell(i, j, bool(random.choice([0, 1]))))
                else:
                    line.append(Cell(i, j, False))
            self.grid.append(line)

    def get_neighbours(self, cell: Cell) -> list:
        neighbours = []
        col, row = cell.col, cell.row
        for st in range(row - 1, row + 2):
            for elem in range(col - 1, col + 2):
                if st in range(0, self.nrows) and elem in range(0, self.ncols) and (elem != col or st != row):
                    neighbours.append(self.grid[st][elem])
        return neighbours

    def update(self):
        new_clist = deepcopy(self.grid)
        for cell in self:
            n = sum(k.is_alive() for k in self.get_neighbours(cell))
            if n != 2 and n != 3:
                new_clist[cell.row][cell.col].state = False
            elif n == 3:
                new_clist[cell.row][cell.col].state = True
        self.grid = new_clist
        return self

    def __iter__(self):
        self.i, self.j = 0, 0
        return self

    def __next__(self) -> Cell:
        if self.i < self.nrows:
            cell = self.grid[self.i][self.j]
            self.j += 1
            if self.j == self.ncols:
                self.i += 1
                self.j = 0
            return cell
        else:
            raise StopIteration

    def __str__(self) -> str:
        str = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.grid[i][j].state:
                    str += '1'
                else:
                    str += '0'
            str += '\n'
        return str

    @classmethod
    def from_file(cls, filename: str) -> "CellList":
        with open(filename, 'r') as file:
            grid = []
            f = file
            row = 0
            col = 0
            ncol = 0
            for st in f:
                line = []
                for c in st:
                    if c == '0':
                        line.append(Cell(row, col, False))
                    if c == '1':
                        line.append(Cell(row, col, True))
                    col += 1
                ncol = col
                col = 0
                grid.append(line)
            for line in grid:
                for cell in line:
                    cell.row = row
                row += 1

            cell_list = CellList(row, ncol, False)
            cell_list.grid = grid
            return cell_list


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
game.run()
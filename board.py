class Board:
    def __init__(self, rows, cols):
        self._create_grid(rows, cols)

    def _create_grid(self, rows, cols):
        self.grid = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append('"')
            self.grid.append(row)

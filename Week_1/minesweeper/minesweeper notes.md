# Problem - Minesweeper

- Sentences: `{A, B, C, D, ...} = N`: of the cells in the set, N are mines
  - For this problem, each cell is `(i, j)`, representing the row and column of the cell







## Rules

- for any cell whose count is 0, we know that all of the cells are safe
- if `len(cell) == N`, all the cells are mines
- if `set1` is a subset of `set2`, then `set2 - set1 = count2 - count1`
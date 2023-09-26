# conwaylife
Conway's Game of Life with python + curses

Troubleshooting:
Activating the venv:
Error occurs with Windows PowerShell terminal window. Before running the activation script:
`conwaylife/Scripts/Activate.ps1`
Run in the appropriate PowerShell window:
`Set-ExecutionPolicy Unrestricted -Scope Process`


the rules for Life are:

Any live cell with fewer than two live neighbors dies.
Any live cell with two or three live neighbors lives.
Any live cell with more than three live neighbors dies.
Any dead cell with exactly three live neighbors becomes a live cell.
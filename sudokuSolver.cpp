#include <iostream>
#include <vector>
using namespace std;

bool solveSudoku(vector<vector<int>> &board)
{
    // Find an empty cell
    for (int row = 0; row < 9; row++)
    {
        for (int col = 0; col < 9; col++)
        {
            if (board[row][col] == 0)
            {
                // Try numbers 1 to 9
                for (int num = 1; num <= 9; num++)
                {
                    bool valid = true;

                    // Check row
                    for (int j = 0; j < 9; j++)
                    {
                        if (board[row][j] == num)
                        {
                            valid = false;
                            break;
                        }
                    }

                    // Check column
                    for (int i = 0; i < 9 && valid; i++)
                    {
                        if (board[i][col] == num)
                        {
                            valid = false;
                            break;
                        }
                    }

                    // Check 3x3 box
                    int startRow = (row / 3) * 3;
                    int startCol = (col / 3) * 3;

                    for (int i = startRow; i < startRow + 3 && valid; i++)
                    {
                        for (int j = startCol; j < startCol + 3; j++)
                        {
                            if (board[i][j] == num)
                            {
                                valid = false;
                                break;
                            }
                        }
                    }

                    // If number is valid
                    if (valid)
                    {
                        board[row][col] = num;

                        // Recursively solve remaining cells
                        if (solveSudoku(board))
                            return true;

                        // Backtrack
                        board[row][col] = 0;
                    }
                }

                // No number works for this cell
                return false;
            }
        }
    }

    // No empty cells left
    return true;
}

int main()
{
    vector<vector<int>> board(9, vector<int>(9));

    cout << "Enter Sudoku (use 0 for empty cells):\n";

    for (int i = 0; i < 9; i++)
    {
        for (int j = 0; j < 9; j++)
        {
            cin >> board[i][j];
        }
    }

    if (solveSudoku(board))
    {
        cout << "\nSolved Sudoku:\n";

        for (int i = 0; i < 9; i++)
        {
            for (int j = 0; j < 9; j++)
            {
                cout << board[i][j] << " ";
            }
            cout << endl;
        }
    }
    else
    {
        cout << "No solution exists.";
    }

    return 0;
}
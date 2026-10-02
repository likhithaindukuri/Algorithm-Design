#include <bits/stdc++.h>
using namespace std;

int DIRS[4][2] = {
    {-1, 0},
    {1, 0},
    {0, -1},
    {0, 1}};
bool searchWord(vector<vector<char>> &board, int i, int j, int M, int N,
                string word, int cur, vector<vector<bool>> &used)
{
    if (i < 0 || i >= M || j < 0 || j >= N)
    {
        return false;
    }

    if (used[i][j])
    {
        return false;
    }

    if (board[i][j] != word[cur])
    {
        return false;
    }

    if (cur == word.length() - 1)
    {
        return true;
    }

    used[i][j] = true;

    for (int d = 0; d < 4; d++)
    {
        int nextI = i + DIRS[d][0];
        int nextJ = j + DIRS[d][1];

        if (searchWord(board, nextI, nextJ, M, N, word, cur + 1, used))
        {
            return true;
        }
    }

    used[i][j] = false;

    return false;
}

bool findWord(vector<vector<char>> &board, string word)
{
    int M = board.size();
    int N = board[0].size();

    vector<vector<bool>> used(M, vector<bool>(N, false));

    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if (board[i][j] == word[0])
            {
                if (searchWord(board, i, j, M, N, word, 0, used))
                {
                    return true;
                }
            }
        }
    }

    return false;
}

int main()
{
    int M, N;

    cout << "Enter number of rows (M): ";
    cin >> M;
    cout << "Enter number of columns (N): ";
    cin >> N;
    vector<vector<char>> board(M, vector<char>(N));
    cout << "Enter the grid characters row by row: ";

    for (int i = 0; i < M; i++)
    {
        cout << "Row " << i << ": ";

        for (int j = 0; j < N; j++)
        {
            cin >> board[i][j];
        }
    }

    string targetWord;

    cout << "Enter the target word to search for: ";
    cin >> targetWord;

    bool found = findWord(board, targetWord);

    if (found)
    {
        cout << "[Success] Word \"" << targetWord << endl
             << "\" WAS found in the grid!" << endl;
    }
    else
    {
        cout << "[Failed] Word " << targetWord << "WAS NOT found in the grid." << endl;
    }

    return 0;
}
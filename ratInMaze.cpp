#include <iostream>
#include <vector>
using namespace std;

bool ratInMaze(int i, int j, vector<vector<int>> &a, int n, vector<vector<int>> &vis)
{
    // Destination reached
    if (i == n - 1 && j == n - 1)
        return true;

    // Mark current cell
    vis[i][j] = 1;

    // Down
    if (i + 1 < n && !vis[i + 1][j] && a[i + 1][j] == 1)
    {
        if (ratInMaze(i + 1, j, a, n, vis))
            return true;
    }

    // Left
    if (j - 1 >= 0 && !vis[i][j - 1] && a[i][j - 1] == 1)
    {
        if (ratInMaze(i, j - 1, a, n, vis))
            return true;
    }

    // Right
    if (j + 1 < n && !vis[i][j + 1] && a[i][j + 1] == 1)
    {
        if (ratInMaze(i, j + 1, a, n, vis))
            return true;
    }

    // Up
    if (i - 1 >= 0 && !vis[i - 1][j] && a[i - 1][j] == 1)
    {
        if (ratInMaze(i - 1, j, a, n, vis))
            return true;
    }

    // Backtrack
    vis[i][j] = 0;

    return false;
}

int main()
{
    int n;

    cout << "Enter size of maze: ";
    cin >> n;

    vector<vector<int>> maze(n, vector<int>(n));

    cout << "Enter the maze:\n";

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            cin >> maze[i][j];
        }
    }

    vector<vector<int>> vis(n, vector<int>(n, 0));

    bool ans = false;

    if (n > 0 && maze[0][0] == 1 || maze[n - 1][n - 1] == 0)
    {
        ans = ratInMaze(0, 0, maze, n, vis);
    }

    if (ans)
        cout << "Path exists";
    else
        cout << "No path exists";

    return 0;
}
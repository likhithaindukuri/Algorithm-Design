#include <iostream>
#include <vector>
#include <string>
using namespace std;

void genParen(int n, int left, int right, string sol, vector<string> &res)
{
    if (right == n)
    {
        res.push_back(sol);
        return;
    }
    if (left < n)
    {
        genParen(n, left + 1, right, sol + "(", res);
    }
    if (right < left)
    {
        genParen(n, left, right + 1, sol + ")", res);
    }
}
int main()
{
    int n;
    cout << "Enter n: ";
    cin >> n;
    vector<string> res;
    genParen(n, 0, 0, "", res);
    cout << "Valid Parentheses are: " << endl;
    for (string s : res)
    {
        cout << s << endl;
    }
    return 0;
}
#include <iostream>
#include <string>
using namespace std;

void patternMatch(string text, string pattern)
{
    int n = text.length();
    int m = pattern.length();
    bool found = false;

    for (int i = 0; i <= n - m; i++)
    {
        int j = 0;

        while (j < m && text[i + j] == pattern[j])
        {
            j++;
        }

        if (j == m)
        {
            cout << "Pattern found at position " << i << endl;
            found = true;
        }
    }

    if (!found)
    {
        cout << "Pattern not found" << endl;
    }
}

int main()
{
    string text, pattern;

    cout << "Enter the text: ";
    cin >> text;

    cout << "Enter the pattern: ";
    cin >> pattern;

    patternMatch(text, pattern);

    return 0;
}
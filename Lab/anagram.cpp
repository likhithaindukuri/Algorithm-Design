#include <iostream>
#include <string>
using namespace std;

bool areAnagrams(string str1, string str2)
{
    if (str1.length() != str2.length())
        return false;

    int count[26] = {0};

    for (int i = 0; i < str1.length(); i++)
    {
        count[str1[i] - 'a']++;
    }

    for (int i = 0; i < str2.length(); i++)
    {
        count[str2[i] - 'a']--;
    }

    for (int i = 0; i < 26; i++)
    {
        if (count[i] != 0)
            return false;
    }

    return true;
}

int main()
{
    string str1, str2;

    cout << "Enter first string: ";
    cin >> str1;

    cout << "Enter second string: ";
    cin >> str2;

    if (areAnagrams(str1, str2))
        cout << "The strings are anagrams." << endl;
    else
        cout << "The strings are not anagrams." << endl;

    return 0;
}
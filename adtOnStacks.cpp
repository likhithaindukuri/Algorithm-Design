#include <bits/stdc++.h>
using namespace std;

int n, c;
vector<vector<int>> st;
vector<int> top;

void displayStacks()
{
    cout << "\n===== CURRENT STACKS =====" << endl;

    for (int i = 0; i < n; i++)
    {
        cout << "Stack " << i + 1 << ": ";

        if (top[i] == -1)
        {
            cout << "Empty";
        }
        else
        {
            for (int j = 0; j <= top[i]; j++)
            {
                cout << st[i][j] << " ";
            }
        }

        cout << endl;
    }
}

void push(int sNo, int ele)
{
    sNo--;

    if (top[sNo] == c - 1)
    {
        cout << "Stack is full" << endl;
        return;
    }

    top[sNo]++;
    st[sNo][top[sNo]] = ele;

    cout << "Element pushed successfully" << endl;
}

void pop(int sNo)
{
    sNo--;

    if (top[sNo] == -1)
    {
        cout << "Stack is empty" << endl;
        return;
    }

    cout << "Deleted element: " << st[sNo][top[sNo]] << endl;

    top[sNo]--;
}

void isEmpty(int sNo)
{
    sNo--;

    if (top[sNo] == -1)
        cout << "Stack is empty" << endl;
    else
        cout << "Stack is not empty" << endl;
}

void isFull(int sNo)
{
    sNo--;

    if (top[sNo] == c - 1)
        cout << "Stack is full" << endl;
    else
        cout << "Stack is not full" << endl;
}

int main()
{
    cout << "Enter no of stacks: ";
    cin >> n;

    cout << "Enter capacity of stacks: ";
    cin >> c;

    st.resize(n, vector<int>(c));
    top.resize(n, -1);

    int choice;

    do
    {
        cout << "\n1. Push new element" << endl;
        cout << "2. Pop the element" << endl;
        cout << "3. Check isEmpty" << endl;
        cout << "4. Check isFull" << endl;
        cout << "5. Exit" << endl;

        cout << "Enter choice: ";
        cin >> choice;

        int ele, sNo;

        switch (choice)
        {
        case 1:
            cout << "Enter element to add: ";
            cin >> ele;

            cout << "Enter in which stack you want to add that element: ";
            cin >> sNo;

            push(sNo, ele);
            displayStacks();
            break;

        case 2:
            cout << "Enter in which stack you want to delete the element: ";
            cin >> sNo;

            pop(sNo);
            displayStacks();
            break;

        case 3:
            cout << "Enter stack number: ";
            cin >> sNo;

            isEmpty(sNo);
            displayStacks();
            break;

        case 4:
            cout << "Enter stack number: ";
            cin >> sNo;

            isFull(sNo);
            displayStacks();
            break;

        case 5:
            cout << "Exiting..." << endl;
            break;

        default:
            cout << "Invalid choice" << endl;
        }

    } while (choice != 5);

    return 0;
}
#include <iostream>
using namespace std;

struct Node
{
    char data;
    Node *next;
};

Node *insert(Node *head, char ch)
{
    Node *temp = new Node;
    temp->data = ch;
    temp->next = NULL;

    if (head == NULL)
        return temp;

    Node *p = head;

    while (p->next != NULL)
        p = p->next;

    p->next = temp;

    return head;
}

Node *createList(string str)
{
    Node *head = NULL;

    for (int i = 0; i < str.length(); i++)
    {
        head = insert(head, str[i]);
    }

    return head;
}

void display(Node *head)
{
    while (head != NULL)
    {
        cout << head->data;
        head = head->next;
    }

    cout << endl;
}

void stringMatch(Node *text, Node *pattern)
{
    Node *T = text;
    bool found = false;
    int position = 0;

    while (T != NULL)
    {
        Node *A = T;
        Node *B = pattern;

        while (A != NULL && B != NULL && A->data == B->data)
        {
            A = A->next;
            B = B->next;
        }

        if (B == NULL)
        {
            cout << "Pattern found at position " << position << endl;
            found = true;
        }

        T = T->next;
        position++;
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

    Node *textList = createList(text);
    Node *patternList = createList(pattern);

    cout << "Text: ";
    display(textList);

    cout << "Pattern: ";
    display(patternList);

    stringMatch(textList, patternList);

    return 0;
}
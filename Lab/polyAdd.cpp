#include <iostream>
using namespace std;

struct Node
{
    int coeff;
    int power;
    Node *next;
};

Node *insertEnd(Node *head, Node *&tail, int coeff, int power)
{
    Node *temp = new Node;

    temp->coeff = coeff;
    temp->power = power;
    temp->next = NULL;

    if (head == NULL)
    {
        head = temp;
        tail = temp;
    }
    else
    {
        tail->next = temp;
        tail = temp;
    }

    return head;
}

Node *createPolynomial()
{
    Node *head = NULL;
    Node *tail = NULL;

    int n;

    cout << "Enter number of terms: ";
    cin >> n;

    for (int i = 1; i <= n; i++)
    {
        int coeff, power;

        cout << "Enter coefficient: ";
        cin >> coeff;

        cout << "Enter power: ";
        cin >> power;

        head = insertEnd(head, tail, coeff, power);
    }

    return head;
}

void display(Node *head)
{
    while (head != NULL)
    {
        cout << head->coeff << "x^" << head->power;

        if (head->next != NULL)
            cout << " + ";

        head = head->next;
    }

    cout << endl;
}

Node *addPoly(Node *p1, Node *p2)
{
    Node *result = NULL;
    Node *tail = NULL;

    while (p1 != NULL && p2 != NULL)
    {
        if (p1->power == p2->power)
        {
            result = insertEnd(result, tail,
                               p1->coeff + p2->coeff,
                               p1->power);

            p1 = p1->next;
            p2 = p2->next;
        }
        else if (p1->power > p2->power)
        {
            result = insertEnd(result, tail,
                               p1->coeff,
                               p1->power);

            p1 = p1->next;
        }
        else
        {
            result = insertEnd(result, tail,
                               p2->coeff,
                               p2->power);

            p2 = p2->next;
        }
    }

    while (p1 != NULL)
    {
        result = insertEnd(result, tail,
                           p1->coeff,
                           p1->power);

        p1 = p1->next;
    }

    while (p2 != NULL)
    {
        result = insertEnd(result, tail,
                           p2->coeff,
                           p2->power);

        p2 = p2->next;
    }

    return result;
}

int main()
{
    Node *poly1;
    Node *poly2;
    Node *sum;

    cout << "Enter first polynomial\n";
    poly1 = createPolynomial();

    cout << "Polynomial 1: ";
    display(poly1);

    cout << "\nEnter second polynomial\n";
    poly2 = createPolynomial();

    cout << "Polynomial 2: ";
    display(poly2);

    sum = addPoly(poly1, poly2);

    cout << "\nAddition polynomial: ";
    display(sum);

    return 0;
}
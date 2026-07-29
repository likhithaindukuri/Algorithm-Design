#include <iostream>
using namespace std;

struct Node
{
    int coeff;
    int power;
    Node *next;
};

Node *insert(Node *head, int coeff, int power)
{
    Node *temp = new Node;
    temp->coeff = coeff;
    temp->power = power;
    temp->next = NULL;

    if (head == NULL)
        return temp;

    Node *p = head;
    while (p->next != NULL)
        p = p->next;

    p->next = temp;
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

    while (p1 != NULL && p2 != NULL)
    {
        if (p1->power == p2->power)
        {
            result = insert(result, p1->coeff + p2->coeff, p1->power);
            p1 = p1->next;
            p2 = p2->next;
        }
        else if (p1->power > p2->power)
        {
            result = insert(result, p1->coeff, p1->power);
            p1 = p1->next;
        }
        else
        {
            result = insert(result, p2->coeff, p2->power);
            p2 = p2->next;
        }
    }

    while (p1 != NULL)
    {
        result = insert(result, p1->coeff, p1->power);
        p1 = p1->next;
    }

    while (p2 != NULL)
    {
        result = insert(result, p2->coeff, p2->power);
        p2 = p2->next;
    }

    return result;
}

int main()
{
    Node *poly1 = NULL, *poly2 = NULL, *sum = NULL;

    poly1 = insert(poly1, 5, 3);
    poly1 = insert(poly1, 4, 2);
    poly1 = insert(poly1, 2, 0);

    poly2 = insert(poly2, 5, 2);
    poly2 = insert(poly2, 5, 1);
    poly2 = insert(poly2, 5, 0);

    cout << "Polynomial 1: ";
    display(poly1);

    cout << "Polynomial 2: ";
    display(poly2);

    sum = addPoly(poly1, poly2);

    cout << "Sum: ";
    display(sum);

    return 0;
}
#include <iostream>
using namespace std;

#define M 100
#define N 10

int Q[M];
int Front[N], Rear[N];

bool isEmpty(int i)
{
    return (Front[i] == Rear[i]);
}

bool isFull(int i)
{
    int end = (i + 1) * (M / N) - 1;
    return (Rear[i] == end);
}

bool addQ(int x, int i)
{
    if (isFull(i))
        return false;

    Rear[i]++;
    Q[Rear[i]] = x;

    return true;
}

int delQ(int i)
{
    if (isEmpty(i))
    {
        cout << "Queue " << i + 1 << " is Empty\n";
        return -1;
    }

    Front[i]++;
    return Q[Front[i]];
}

int servReq(char req, int i, int x = 0)
{
    if (req == 'A')
        return addQ(x, i);

    if (req == 'D')
        return delQ(i);

    return -1;
}

int main()
{
    for (int i = 0; i < N; i++)
    {
        Front[i] = i * (M / N) - 1;
        Rear[i] = i * (M / N) - 1;
    }

    servReq('A', 0, 10);
    servReq('A', 0, 20);
    servReq('A', 0, 30);

    cout << "Deleted from Queue1 : "
         << servReq('D', 0) << endl;

    cout << "Deleted from Queue1 : "
         << servReq('D', 0) << endl;

    servReq('A', 1, 100);
    servReq('A', 1, 200);

    cout << "Deleted from Queue2 : "
         << servReq('D', 1) << endl;

    return 0;
}
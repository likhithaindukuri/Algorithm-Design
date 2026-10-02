#include <iostream>
#include <vector>
using namespace std;

int knapSack(int i, int W, vector<int> &wt, vector<int> &val)
{
    int n = val.size();
    if (i >= n)
    {
        return 0;
    }
    if (wt[i] > W)
    {
        return knapSack(i + 1, W, wt, val);
    }
    else
    {
        return max((knapSack(i + 1, W, wt, val)), val[i] + (knapSack(i + 1, W - wt[i], wt, val)));
    }
}

int main()
{
    int W;
    cout << "Enter Capacity: ";
    cin >> W;
    int n;
    cout << "Enter size of array: ";
    cin >> n;
    vector<int> val;
    cout << "Enter elements into val: ";
    for (int i = 0; i < n; i++)
    {
        int x;
        cin >> x;
        val.push_back(x);
    }
    vector<int> wt;
    cout << "Enter elements ito wt: ";
    for (int i = 0; i < n; i++)
    {
        int x;
        cin >> x;
        wt.push_back(x);
    }
    int ans = knapSack(0, W, wt, val);
    cout << "Max Profit is: ";
    cout << ans;
    return 0;
}
#include <iostream>
#include <vector>
#include <cmath>

using namespace std;


const int MOD = 998244353;

void solve() {
    int n;
    cin >> n;

    vector<int> p(n), q(n);
    for (int i = 0; i < n; ++i) cin >> p[i];
    for (int i = 0; i < n; ++i) cin >> q[i];

    vector<int> r;
    int a = 0, b = 0;
    int a_val = 0, b_val = 0;

    for (int i = 0; i < n; ++i) {
        if (p[i] > a_val) {
            a_val = p[i];
            a = i;
        }
        if (q[i] > b_val) {
            b_val = q[i];
            b = i;
        }

        int res;
        if (p[a] > q[b] || (p[a] == q[b] && q[i - a] > p[i - b])) {
            res = (int)((1LL << p[a]) + (1LL << q[i - a])) % MOD;
        } else {
            res = (int)((1LL << p[i - b]) + (1LL << q[b])) % MOD;
        }

        r.push_back(res);
    }

    for (int val : r) cout << val << " ";
    cout << endl;

}


int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}
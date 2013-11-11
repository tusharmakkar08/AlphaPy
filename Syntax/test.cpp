// Libraries 

#include <list>
#include <vector>
#include <list>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <stack>
#include <bitset>
#include <algorithm>
#include <functional>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <queue>
#include <ctime>
#include <cassert>
#include <climits>
#include <limits>

// Definitions 

#define pb push_back
#define max(i,j) (i>j?i:j)
#define min(i,j) (i<j?i:j)
#define mod 1000000007
#define s(n)					scanf("%d",&n)
#define sl(n) 					scanf("%lld",&n)
#define sf(n) 					scanf("%lf",&n)
#define ss(n) 					scanf("%s",n)
#define pf printf
#define mset(x,v) memset(x,v,sizeof(x))
#define LL long long int
#define FOR(i,a,b) for(LL i=(LL)(a);i<(LL)(b);i++)
#define REV(i,a,b) for(LL i=(LL)(a);i>=(LL)(b);i--)

using namespace std;

typedef vector < LL > row;
typedef vector < row > matrix;
int arr[]={1,2,3,3,2,2};
// Global Declarations
int findMajorityElement( int size)
{
    int count = 0, i, majorityElement;
    for (i = 0 ; i < size ; i++)
    {
        if (count == 0) {
            majorityElement = arr[i];
            count = 1;
        }
        else
        {
            if(arr[i] == majorityElement)
                count++;
            else
                count--;
        }
    }
	pf("%d\n",majorityElement);
    count = 0;
    for (i = 0; i < size; i++) {
        if (arr[i] == majorityElement) {
            count++;
    }}
    if (count > size/2) {
        return majorityElement;
    }
    else return -1;
}
int main()
{
	LL T;
	findMajorityElement(6);
	return 0;
}


### 알고리즘별 주의사항 ###

1. 완전탐색
    - 조건이 작은 수일 때
    - 완전 탐색했을 때 시간제한이 넘지 않는 경우
2. 그리디
    - 최소한으로~ / 최대한으로~ / 가장 많이~ / 가장 적게~
    - 그리디 문제의 일부를 풀면 나머지도 그리디
    - 특성상 정렬 후 값을 이용하기 때문에 Priority Queue 를 잘 활용한다.
3. 분할정복
    - 문제에서 분할을 알려주는 (4분할~/9분할~/선을 따라 분할~)
    - 수열에서 부분의 무언가를 구할 때 (https://www.acmicpc.net/problem/1725) -> 왼쪽 / 오른쪽 / 가운데로 할 수 있음
    - 재귀함수를 이용
4. DP
    - 전 단계들의 값을 사용하여 다음 단계를 계산하는 경우
    - MIN, MAX가 많이 사용됨
    - 자칫, 그리디처럼 보일 수 있지만 작은 것의 합이 큰 것보다 커질 수 있다는 점을 인지해야함 (https://www.acmicpc.net/problem/12865)
5. 이분탐색
    - 정렬되어 있어야 사용할 수 있음
    - 따라서, 찾는 값 (parametric search시) 이 변함에 따라 결과가 단조 증가/단조 감소하는 경우에 고려해봄직함
    - 논리적 해결이 아니라 구하고자 하는 값을 툭툭찔러서 찾아보는 parametric search임
    - 주어지는 변수의 범위가 10억과 같이 큰 수일 수 
    - 아래 코드가 가장 일반적인 모양새
    ```c++
    int l=0;
    int r=1000000001;
    while (l<r) {
        int mid = (l+r)/2;
        if (num >= answer) {
            l = mid;
        } else {
            r = mid;
        }
        if (r-l == 1) break;
    }
    ```
6. 링크드리스트
    - head 부분 (은 for문 바깥에서 처리하는게 정신건강에 이로움
### 자주하는 실수 ###

- 똑같은 걸 계속 계산하게 두지 말자 (visited 등을 통해 prunning 필요)
- 자료형 범위의 max가 얼마나 될지 파악하자 / 자료형 cast / 함수 반환형 등을 생각하자
- stack 같은 자료구조 쓸 때 top() 쓰기 전에 empty()인지 확인 필수

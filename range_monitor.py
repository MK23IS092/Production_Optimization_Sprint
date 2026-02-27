class RangePerformanceMonitor:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (2 * n)
        
    def update(self, idx: int, val: int):
        """
        Update the value at a specific index.
        Time Complexity: O(log N)
        """
        idx += self.n
        self.tree[idx] = val
        while idx > 1:
            idx //= 2
            self.tree[idx] = max(self.tree[2 * idx], self.tree[2 * idx + 1])
            
    def queryMax(self, left: int, right: int) -> int:
        """
        Query the maximum value in the range [left, right] inclusive.
        Time Complexity: O(log N)
        """
        left += self.n
        right += self.n + 1  # Add 1 to make it inclusive
        res = float('-inf')
        
        while left < right:
            if left % 2 == 1:
                res = max(res, self.tree[left])
                left += 1
            if right % 2 == 1:
                right -= 1
                res = max(res, self.tree[right])
            left //= 2
            right //= 2
                
        return res

if __name__ == "__main__":
    arr = [2, 1, 5, 3, 4]
    st = RangePerformanceMonitor(len(arr))
    for i, val in enumerate(arr):
        st.update(i, val)
        
    print("Max in range 1-3:", st.queryMax(1, 3))
    st.update(2, 10)
    print("After update, max in range 1-3:", st.queryMax(1, 3))

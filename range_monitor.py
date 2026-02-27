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
    monitor = RangePerformanceMonitor(5) # max index 4
    monitor.update(0, 100)
    monitor.update(1, 105)
    monitor.update(2, 95)
    monitor.update(3, 110)
    monitor.update(4, 102)
    
    # Range 0 to 4 max is 110 at index 3
    assert monitor.queryMax(0, 4) == 110
    # Range 0 to 2 max is 105 at index 1
    assert monitor.queryMax(0, 2) == 105
    # Range 3 to 4 max is 110 at index 3
    assert monitor.queryMax(3, 4) == 110
    
    # Update index 2 to 120
    monitor.update(2, 120)
    assert monitor.queryMax(0, 4) == 120
    
    print("Range Performance Monitor: SUCCESS")

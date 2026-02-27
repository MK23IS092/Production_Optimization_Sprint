from collections import deque

class StreamingMax:
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.dq = deque()  # Store tuples of (value, index)
        self.current_idx = 0
        
    def add(self, value: int) -> int:
        """
        Adds a new value and returns the maximum in the current sliding window.
        Time Complexity: Amortized O(1)
        """
        # Remove elements out of the window
        while self.dq and self.dq[0][1] <= self.current_idx - self.window_size:
            self.dq.popleft()
            
        # Remove elements smaller than the current value (monotonic decreasing queue)
        while self.dq and self.dq[-1][0] < value:
            self.dq.pop()
            
        # Add the current value
        self.dq.append((value, self.current_idx))
        
        self.current_idx += 1
        return self.dq[0][0]

if __name__ == "__main__":
    nums = [10, 5, 2, 7, 8, 7]
    k = 3
    stream = StreamingMax(window_size=k)
    res = []
    
    for i, n in enumerate(nums):
        val = stream.add(n)
        if i >= k - 1:
            res.append(val)
            
    print("Sliding window max:", res)

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
    stream = StreamingMax(window_size=3)
    values = [1, 3, -1, -3, 5, 3, 6, 7]
    result = []
    
    # After 3 elements, we start validating max continuously
    # Wait until it has at least `window_size` elements? The problem says "stream", 
    # we return max of window so far. Let's trace it exactly.
    for val in values:
        result.append(stream.add(val))
    
    # 1: window [1] -> max 1
    # 3: window [1, 3] -> max 3
    # -1: window [1, 3, -1] -> max 3
    # -3: window [3, -1, -3] -> max 3
    # 5: window [-1, -3, 5] -> max 5
    # 3: window [-3, 5, 3] -> max 5
    # 6: window [5, 3, 6] -> max 6
    # 7: window [3, 6, 7] -> max 7
    expected = [1, 3, 3, 3, 5, 5, 6, 7]
    assert result == expected
    print("Streaming Max Analytics: SUCCESS")

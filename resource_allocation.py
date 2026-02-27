class ResourceAllocation:
    def __init__(self, cost_matrix):
        """
        cost_matrix[i][j] represents the cost of worker i doing task j.
        N tasks and N workers. Ensure N <= 20.
        """
        self.costs = cost_matrix
        self.N = len(cost_matrix)
        
    def optimal_allocation(self) -> int:
        """
        Finds the minimum total cost to assign exactly one worker to each task.
        Time Complexity: O(2^N * N)
        """
        # dp[mask] represents the minimum cost using the subset of workers represented by `mask` 
        # to perform the first `count_set_bits(mask)` tasks.
        dp = [float('inf')] * (1 << self.N)
        dp[0] = 0
        
        for mask in range(1 << self.N):
            # Compute number of tasks already assigned
            task_idx = 0
            temp = mask
            while temp > 0:
                task_idx += temp & 1
                temp >>= 1
                
            if task_idx >= self.N:
                continue
                
            for worker in range(self.N):
                # If worker is not yet assigned in the current mask
                if not (mask & (1 << worker)):
                    new_mask = mask | (1 << worker)
                    cost = self.costs[worker][task_idx]
                    
                    if dp[mask] + cost < dp[new_mask]:
                        dp[new_mask] = dp[mask] + cost
                        
        return dp[(1 << self.N) - 1]

if __name__ == "__main__":
    cost = [
        [9, 2, 7],
        [6, 4, 3],
        [5, 8, 1]
    ]

    allocator = ResourceAllocation(cost)
    print("Minimum assignment cost:", allocator.optimal_allocation())

# Algorithm Explanations

This document provides a detailed breakdown of the 5 problems solved in this sprint, including the logic, complexity analysis, alternative approaches, and why the chosen approach is optimal.

---

## 1. The "Global Autocomplete" System (Tries)
**File:** `autocomplete.py`

### Question
Build a Trie-based system that stores 1 million strings. Implement a function that returns the top 5 most frequent suggestions for a given prefix. The prefix search must be O(L), where L is the length of the prefix.

### What it Means
When you type a prefix (like "app") into a search bar, the system should instantly return the 5 most popular words starting with that prefix (e.g., "apple", "application"). It needs to be extremely fast, specifically bounded only by the length of the string you typed, not by the 1 million words stored in the dictionary.

### The Logic
We use a **Trie (Prefix Tree)**. Instead of just storing characters at each node, we also store a list of the `top 5` most frequent words that pass through that specific node. 
- **Insertion:** When inserting a word, we traverse down the Trie. At *every single node* we visit, we update its local `top_matches` list to ensure it continually holds the top 5 words.
- **Querying:** When querying for a prefix of length `L`, we simply traverse down `L` steps in the Trie to the node representing the prefix, and instantly return its pre-calculated `top_matches` list.

### Complexity
- **Time Complexity:** 
  - Insertion: `O(K * log(5))` where `K` is the word length (since sorting top 5 takes negligible constant time).
  - Search: `O(L)` where `L` is the length of the prefix. We don't need to recursively search the Trie; the answer is already sitting at the prefix node.
- **Space Complexity:** `O(N * K)` where `N` is the number of words and `K` is the average word length. Since we store up to 5 words at every node, the memory footprint is larger than a standard Trie.

### Alternative Approach
A standard Trie would traverse to the prefix node (O(L)) and then perform a Depth-First Search (DFS) to find all possible child words, sort them by frequency, and return the top 5.
- Time complexity: `O(L + W * log W)` where W is the number of words matching the prefix.

### Why the Chosen Approach is Best
The alternative approach is far too slow for real-time autocomplete on a 1 million word dictionary. If the user types "a", the DFS would literally have to search hundreds of thousands of words. By caching the top 5 at each node, we trade a little bit of RAM (Space) for a phenomenal boost in speed (Time), strictly guaranteeing `O(L)` lookup.

---

## 2. The "Streaming Max" Analytics (Deques/Monotonic Queue)
**File:** `streaming_max.py`

### Question
You are receiving a stream of server latency data. Given a window size K, calculate the maximum latency in every window. You must process each incoming data point in amortized O(1) time.

### What it Means
Imagine a live graph showing the maximum server lag over the last 10 seconds. For every new second of data that comes in, one old second of data expires. You need to instantly know the maximum value in the current active 10-second window.

### The Logic
We use a **Monotonically Decreasing Double-Ended Queue (Deque)**. The deque stores pairs of `(value, index)`.
The core logic relies on two rules when a new value arrives:
1. **Remove Expired:** Remove elements from the `left` (front) of the deque if their index is completely outside the current window.
2. **Remove Useless:** Remove elements from the `right` (back) of the deque if they are *smaller* than the newly arriving value. They are useless because the new value is bigger and will stay in the window *longer* than the old smaller values.

After these cleanups, we append the new value to the right. The maximum element for the current window is always sitting safely at the `left` (front) of the deque!

### Complexity
- **Time Complexity:** Amortized `O(1)` per element. Although there is a `while` loop inside the `add` function, every element is added to the deque exactly once and removed at most once. Therefore, over N elements, it does `2N` operations, averaging `O(1)` per element.
- **Space Complexity:** `O(K)` where `K` is the window size, as the deque will at most hold `K` elements.

### Alternative Approach
Use a Max-Heap (Priority Queue) to store the window. 
- You add to the heap (`O(log K)`) and lazily delete elements when the max is out-of-bounds (`O(log K)`).

### Why the Chosen Approach is Best
A heap requires `O(log K)` time per element stream, which is highly inefficient for high-frequency low-latency server streams. The Monotonic Deque completely outperforms it by dropping the complexity down to `O(1)`.

---

## 3. The "Dynamic Network Vulnerability" (Tarjan's/Graphs)
**File:** `network_vulnerability.py`

### Question
Given a communication network represented as an undirected graph, identify all "Critical Links" (Bridges). A link is critical if its removal disconnects the network. Solve in O(V + E) using a single DFS pass.

### What it Means
In a server farm, edges represent cables. A "Bridge" or "Critical Link" is a single point of failure—a specific cable that, if cut, splits the server farm into two isolated networks that can no longer communicate. You need to find all of these vulnerable cables.

### The Logic
We use **Tarjan's Bridge-Finding Algorithm**. We do a Depth First Search (DFS) while maintaining two tracking arrays for each node:
1. `discovery_time`: The "timestamp" when we first visited the node.
2. `lowest_reachable`: The smallest discovery timestamp a node can reach by taking *at most one back-edge* (an edge that points back up the DFS tree to an ancestor).

During the DFS, if we are at node `U` checking its child `V`, and we discover that `lowest_reachable[V] > discovery_time[U]`, it means the subtree at `V` has absolutely no back-edges pointing to `U` or above `U`. Therefore, the only way `V` connects to the rest of the graph is strictly through the edge `U-V`. Thus, `U-V` is a bridge!

### Complexity
- **Time Complexity:** `O(V + E)`. We visit every Vertex (V) and every Edge (E) exactly once during the single Depth-First Search pass.
- **Space Complexity:** `O(V + E)` to store the adjacency list graph, plus `O(V)` auxiliary arrays for `visited`, `discovery_time`, `lowest_reachable`, etc.

### Alternative Approach
For every single edge in the graph, remove it, run a full BFS/DFS to see if the graph is still fully connected, and then put the edge back.
- Time complexity: `O(E * (V + E))`, which is essentially cubic time for dense graphs.

### Why the Chosen Approach is Best
Tarjan's algorithm does mathematically in one pass what the brute-force approach does in a thousand. It mathematically prevents recalculating graph states and operates flawlessly in standard linear time.

---

## 4. The "Range Performance Monitor" (Segment Trees)
**File:** `range_monitor.py`

### Question
Design a system for a stock exchange that handles two operations: `update(index, value)` for a stock price and `queryMax(L, R)` to find the highest price in a time range. Both operations must be O(log N).

### What it Means
Imagine an array of stock prices changing constantly. You need to do two things instantly: Update the price of a stock at a specific index, and query "What was the highest stock price between hour 5 and hour 10?".

### The Logic
We use a **Segment Tree** (implemented dynamically on a 1D Array for optimal caching). 
A Segment Tree is a binary tree where the leaf nodes represent the actual array elements, and every internal node stores the *Maximum* of its two children. 
- **Updating:** When we update a leaf node, we simply walk straight up its parent chain to the root of the tree, updating the maximum values along the way.
- **Querying:** When asking for a range `[L, R]`, we jump around the tree, grabbing pre-calculated maximum chunks that perfectly fit inside our target range, instead of iterating over the raw data one by one.

### Complexity
- **Time Complexity:** 
  - Update: `O(log N)` because the tree height is `log N`, and we only walk straight up to the root.
  - Query: `O(log N)` because at each level of the tree, we access at most 2 nodes.
- **Space Complexity:** `O(2 * N)` because a fully balanced segment tree for N elements fits perfectly inside an array of size `2N`.

### Alternative Approaches
1. **Raw Array:** Update is `O(1)`, but Range Query is `O(N)` (Scanning the array). 
2. **Prefix Arrays:** Doesn't work well for "Maximum"; prefix arrays are usually for "Sum". And if elements are constantly updating, updating a prefix array takes `O(N)`.

### Why the Chosen Approach is Best
A Segment Tree is the absolute golden standard for situations where the data array both undergoes *heavy mutations* (writes) and *heavy range queries* (reads). It stabilizes both operations perfectly to logarithmic `O(log N)` time.

---

## 5. The "Optimal Resource Allocation" (Bitmask DP)
**File:** `resource_allocation.py`

### Question
You have N tasks and N workers (where N < 20). Each worker has a specific cost for each task. Assign exactly one worker to each task such that the total cost is minimized. Improve upon the O(N!) brute force to O(2^N * N^2) using state compression. *(Note: Our implementation actually achieves `O(2^N * N)` which is even better).*

### What it Means
This is the classic "Assignment Problem". If Worker A is fast at Task 1, but expensive at Task 2, how do you map everyone perfectly so the master company spends the least amount of money?

### The Logic
We use **Dynamic Programming with Bitmasking (State Compression)**.
Because `N < 20`, we can represent the "state of workers currently assigned" as a binary integer!
For example, if N=4 and the mask is `0101` (decimal `5`), it means Worker 0 and Worker 2 are already assigned to tasks. 
- The number of set bits (1s) in the mask tells us *how many tasks* have already been assigned. Let's say `k` bits are set, it means the first `k` tasks are assigned.
- `dp[mask]` represents the minimum cost to assign the first `k` tasks using the subset of workers represented by `mask`.
- We loop through every possible bitmask state from `0` to `2^N - 1`. For the current mask, we try assigning any unassigned worker to the `k-th` task, flipping their bit, calculating the temporary cost, and storing the absolute minimum in `dp[new_mask]`.

### Complexity
- **Time Complexity:** `O(2^N * N)`. There are `2^N` possible bitmask states. From each state, we loop over `N` workers to attempt transitions. (This is slightly better than the requested `2^N * N^2`).
- **Space Complexity:** `O(2^N)` to store the DP table.

### Alternative Approach
1. **Brute Force:** Try every single permutation of worker-to-task mappings. `O(N!)`.
2. **Hungarian Algorithm:** A complex bipartite matching algorithm that solves it in `O(N^3)`.

### Why the Chosen Approach is Best
While the Hungarian Algorithm is technically faster `O(N^3)`, it is vastly more complex to execute perfectly in a short coding sprint. Bitmask DP elegantly crushes the `O(N!)` brute force down to a highly optimized dynamic table, perfectly leveraging the hint that `N < 20` (since `2^20` is roughly 1 million, which a basic array processes in less than a second). It is significantly easier to write bug-free than bipartite matching.

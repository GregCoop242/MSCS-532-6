"""
Stack and Queue - Elementary Data Structures
Both implemented using Python lists (dynamic arrays).
"""


# ── Stack ────────────────────────────────────────────────────────────────────

class Stack:
    """
    LIFO Stack backed by a dynamic array.

    Time Complexities
    -----------------
    push  : O(1) amortized
    pop   : O(1) amortized
    peek  : O(1)
    search: O(n)
    """

    def __init__(self):
        self._data = []

    def push(self, value):
        """Push value onto the top of the stack. O(1) amortized."""
        self._data.append(value)

    def pop(self):
        """Remove and return the top element. O(1) amortized."""
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self._data.pop()

    def peek(self):
        """Return the top element without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("Peek at an empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack(top → {list(reversed(self._data))})"


# ── Queue ────────────────────────────────────────────────────────────────────

class Queue:
    """
    FIFO Queue implemented with a circular buffer (array).

    Using a circular buffer avoids the O(n) dequeue cost that
    occurs when using a plain list with pop(0).

    Time Complexities
    -----------------
    enqueue : O(1) amortized
    dequeue : O(1) amortized
    peek    : O(1)
    """

    def __init__(self, capacity=8):
        self._data     = [None] * capacity
        self._capacity = capacity
        self._head     = 0    # index of front element
        self._size     = 0    # number of elements

    # ── Resize ───────────────────────────────────────────────────────────────

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._head + i) % self._capacity]
        self._data     = new_data
        self._head     = 0
        self._capacity = new_capacity

    # ── Core operations ──────────────────────────────────────────────────────

    def enqueue(self, value):
        """Add value to the rear of the queue. O(1) amortized."""
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        tail = (self._head + self._size) % self._capacity
        self._data[tail] = value
        self._size += 1

    def dequeue(self):
        """Remove and return the front element. O(1) amortized."""
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        value = self._data[self._head]
        self._data[self._head] = None            # help GC
        self._head  = (self._head + 1) % self._capacity
        self._size -= 1
        if self._size > 0 and self._size == self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    def peek(self):
        """Return the front element without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("Peek at an empty queue")
        return self._data[self._head]

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def __repr__(self):
        items = [(self._data[(self._head + i) % self._capacity])
                 for i in range(self._size)]
        return f"Queue(front → {items} ← rear)"


# ── Deque (bonus) ────────────────────────────────────────────────────────────

class Deque:
    """
    Double-ended queue (Deque) using a circular buffer.
    Supports O(1) push/pop at both ends.
    """

    def __init__(self, capacity=8):
        self._data     = [None] * capacity
        self._capacity = capacity
        self._head     = 0
        self._size     = 0

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._head + i) % self._capacity]
        self._data     = new_data
        self._head     = 0
        self._capacity = new_capacity

    def push_front(self, value):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._head = (self._head - 1) % self._capacity
        self._data[self._head] = value
        self._size += 1

    def push_back(self, value):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        tail = (self._head + self._size) % self._capacity
        self._data[tail] = value
        self._size += 1

    def pop_front(self):
        if self.is_empty():
            raise IndexError("Pop from empty deque")
        value = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return value

    def pop_back(self):
        if self.is_empty():
            raise IndexError("Pop from empty deque")
        tail = (self._head + self._size - 1) % self._capacity
        value = self._data[tail]
        self._data[tail] = None
        self._size -= 1
        return value

    def is_empty(self):
        return self._size == 0

    def __repr__(self):
        items = [self._data[(self._head + i) % self._capacity]
                 for i in range(self._size)]
        return f"Deque({items})"


# ── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("Stack Demo")
    print("=" * 50)

    stack = Stack()
    for v in [1, 2, 3, 4, 5]:
        stack.push(v)
        print(f"  push({v}) → {stack}")

    print()
    while not stack.is_empty():
        print(f"  pop() → {stack.pop()}")

    # Practical use: balanced parentheses checker
    print("\nBalanced parentheses checker:")
    def is_balanced(s):
        st = Stack()
        pairs = {')': '(', ']': '[', '}': '{'}
        for ch in s:
            if ch in '([{':
                st.push(ch)
            elif ch in ')]}':
                if st.is_empty() or st.pop() != pairs[ch]:
                    return False
        return st.is_empty()

    for expr in ["(a+b)*[c-{d/e}]", "((a+b)", "([)]"]:
        print(f"  '{expr}' → {'balanced' if is_balanced(expr) else 'NOT balanced'}")

    print("\n" + "=" * 50)
    print("Queue Demo")
    print("=" * 50)

    queue = Queue()
    for v in [10, 20, 30, 40, 50]:
        queue.enqueue(v)
        print(f"  enqueue({v}) → {queue}")

    print()
    while not queue.is_empty():
        print(f"  dequeue() → {queue.dequeue()}")

    print("\n" + "=" * 50)
    print("Deque Demo")
    print("=" * 50)

    dq = Deque()
    dq.push_back(2)
    dq.push_back(3)
    dq.push_front(1)
    dq.push_front(0)
    print(f"  After pushes: {dq}")
    print(f"  pop_front(): {dq.pop_front()}")
    print(f"  pop_back() : {dq.pop_back()}")
    print(f"  Remaining  : {dq}")

"""
Array and Matrix - Elementary Data Structures
Implements basic array and 2D matrix operations from scratch.
"""


# ── Dynamic Array ─────────────────────────────────────────────────────────────

class Array:
    """
    A dynamic array that resizes automatically.

    Time Complexities
    -----------------
    Access   : O(1)
    Search   : O(n)
    Insert   : O(n) — shifts elements; O(1) amortized at end
    Delete   : O(n) — shifts elements
    """

    def __init__(self):
        self._data     = [None] * 4   # internal storage
        self._capacity = 4
        self._size     = 0

    # ── Core properties ───────────────────────────────────────────────────────

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"Array({[self._data[i] for i in range(self._size)]})"

    def _check_index(self, index):
        if not (0 <= index < self._size):
            raise IndexError(f"Index {index} out of range (size={self._size})")

    # ── Resize ────────────────────────────────────────────────────────────────

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data     = new_data
        self._capacity = new_capacity

    # ── Access ────────────────────────────────────────────────────────────────

    def get(self, index):
        """Return the element at index. O(1)."""
        self._check_index(index)
        return self._data[index]

    def set(self, index, value):
        """Set the element at index. O(1)."""
        self._check_index(index)
        self._data[index] = value

    # ── Insert ────────────────────────────────────────────────────────────────

    def append(self, value):
        """Append value at the end. Amortized O(1)."""
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        """Insert value before index. O(n)."""
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range")
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        # Shift elements right
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete(self, index):
        """Remove and return element at index. O(n)."""
        self._check_index(index)
        value = self._data[index]
        # Shift elements left
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        # Shrink if utilisation drops below 25%
        if self._size > 0 and self._size == self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    # ── Search ────────────────────────────────────────────────────────────────

    def search(self, value):
        """Return index of first occurrence of value, or -1. O(n)."""
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1


# ── 2-D Matrix ────────────────────────────────────────────────────────────────

class Matrix:
    """
    A 2-D matrix backed by a flat list.

    Time Complexities
    -----------------
    Access (get/set) : O(1)
    Row/col search   : O(n*m)
    Add / multiply   : O(n*m) / O(n^3)
    """

    def __init__(self, rows, cols, default=0):
        self._rows = rows
        self._cols = cols
        self._data = [default] * (rows * cols)

    def _index(self, r, c):
        if not (0 <= r < self._rows and 0 <= c < self._cols):
            raise IndexError(f"({r},{c}) out of bounds ({self._rows}x{self._cols})")
        return r * self._cols + c

    def get(self, r, c):
        """O(1) element access."""
        return self._data[self._index(r, c)]

    def set(self, r, c, value):
        """O(1) element update."""
        self._data[self._index(r, c)] = value

    def add(self, other):
        """Element-wise addition. O(n*m)."""
        if self._rows != other._rows or self._cols != other._cols:
            raise ValueError("Matrix dimensions must match for addition")
        result = Matrix(self._rows, self._cols)
        for i in range(self._rows * self._cols):
            result._data[i] = self._data[i] + other._data[i]
        return result

    def multiply(self, other):
        """Standard matrix multiplication. O(n^3)."""
        if self._cols != other._rows:
            raise ValueError("Incompatible dimensions for multiplication")
        result = Matrix(self._rows, other._cols)
        for r in range(self._rows):
            for c in range(other._cols):
                total = 0
                for k in range(self._cols):
                    total += self.get(r, k) * other.get(k, c)
                result.set(r, c, total)
        return result

    def __repr__(self):
        lines = []
        for r in range(self._rows):
            row = [self.get(r, c) for c in range(self._cols)]
            lines.append("  " + str(row))
        return "Matrix(\n" + "\n".join(lines) + "\n)"


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("Array Demo")
    print("=" * 50)

    arr = Array()
    for v in [10, 20, 30, 40, 50]:
        arr.append(v)
    print(f"After appends   : {arr}")

    arr.insert(2, 99)
    print(f"Insert 99 at 2  : {arr}")

    removed = arr.delete(2)
    print(f"Delete index 2  : {arr}  (removed {removed})")

    print(f"get(3)          : {arr.get(3)}")
    print(f"search(30)      : index {arr.search(30)}")

    print("\n" + "=" * 50)
    print("Matrix Demo")
    print("=" * 50)

    m1 = Matrix(2, 3)
    m2 = Matrix(2, 3)
    vals1 = [1, 2, 3, 4, 5, 6]
    vals2 = [7, 8, 9, 1, 2, 3]
    for r in range(2):
        for c in range(3):
            m1.set(r, c, vals1[r * 3 + c])
            m2.set(r, c, vals2[r * 3 + c])

    print(f"M1:\n{m1}")
    print(f"M2:\n{m2}")
    print(f"M1 + M2:\n{m1.add(m2)}")

    a = Matrix(2, 3)
    b = Matrix(3, 2)
    for i, v in enumerate([1, 2, 3, 4, 5, 6]):
        a._data[i] = v
    for i, v in enumerate([7, 8, 9, 10, 11, 12]):
        b._data[i] = v
    print(f"A (2x3) * B (3x2):\n{a.multiply(b)}")

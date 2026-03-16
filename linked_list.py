"""
Linked List and Rooted Tree - Elementary Data Structures
Singly linked list with full operations, plus an optional rooted tree.
"""


# ── Node ──────────────────────────────────────────────────────────────────────

class Node:
    """A single node in a singly linked list."""

    def __init__(self, data):
        self.data = data
        self.next = None   # pointer to next node

    def __repr__(self):
        return f"Node({self.data})"


# ── Singly Linked List ───────────────────────────────────────────────────────

class LinkedList:
    """
    Singly Linked List with a tail pointer for O(1) append.

    Time Complexities
    -----------------
    insert_front  : O(1)
    insert_back   : O(1)  ← tail pointer
    insert_at     : O(n)
    delete_front  : O(1)
    delete_back   : O(n)  ← must walk to second-to-last node
    delete_value  : O(n)
    search        : O(n)
    traverse      : O(n)
    length        : O(1)  ← maintained counter
    reverse       : O(n)
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    # ── Properties ──────────────────────────────────────────────────────────

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def __repr__(self):
        nodes, curr = [], self.head
        while curr:
            nodes.append(str(curr.data))
            curr = curr.next
        return " → ".join(nodes) + " → None"

    # ── Insert ───────────────────────────────────────────────────────────────

    def insert_front(self, data):
        """Insert at the head. O(1)."""
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self._size += 1

    def insert_back(self, data):
        """Insert at the tail. O(1)."""
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def insert_at(self, index, data):
        """Insert before index. O(n)."""
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range")
        if index == 0:
            self.insert_front(data)
            return
        if index == self._size:
            self.insert_back(data)
            return
        new_node = Node(data)
        curr = self.head
        for _ in range(index - 1):
            curr = curr.next
        new_node.next = curr.next
        curr.next = new_node
        self._size += 1

    # ── Delete ───────────────────────────────────────────────────────────────

    def delete_front(self):
        """Remove and return the head. O(1)."""
        if self.is_empty():
            raise IndexError("Delete from empty list")
        value = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return value

    def delete_back(self):
        """Remove and return the tail. O(n)."""
        if self.is_empty():
            raise IndexError("Delete from empty list")
        value = self.tail.data
        if self._size == 1:
            self.head = self.tail = None
        else:
            curr = self.head
            while curr.next is not self.tail:
                curr = curr.next
            curr.next = None
            self.tail = curr
        self._size -= 1
        return value

    def delete_value(self, data):
        """Remove the first node whose data equals `data`. O(n)."""
        if self.is_empty():
            raise ValueError(f"{data} not found")
        if self.head.data == data:
            return self.delete_front()
        curr = self.head
        while curr.next and curr.next.data != data:
            curr = curr.next
        if curr.next is None:
            raise ValueError(f"{data} not found")
        removed = curr.next
        if removed is self.tail:
            self.tail = curr
        curr.next = removed.next
        self._size -= 1
        return removed.data

    # ── Search ───────────────────────────────────────────────────────────────

    def search(self, data):
        """Return the index of the first node with value `data`, or -1. O(n)."""
        curr, idx = self.head, 0
        while curr:
            if curr.data == data:
                return idx
            curr = curr.next
            idx += 1
        return -1

    def get(self, index):
        """Return data at index. O(n)."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range")
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.data

    # ── Traversal & Utility ──────────────────────────────────────────────────

    def traverse(self):
        """Return a Python list of all values. O(n)."""
        result, curr = [], self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def reverse(self):
        """Reverse the list in-place. O(n)."""
        prev, curr = None, self.head
        self.tail = self.head
        while curr:
            nxt        = curr.next
            curr.next  = prev
            prev       = curr
            curr       = nxt
        self.head = prev

    def has_cycle(self):
        """Detect a cycle using Floyd's algorithm. O(n), O(1) space."""
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False


# ── Rooted Tree (optional) ───────────────────────────────────────────────────

class TreeNode:
    """
    A node in a rooted tree represented using linked-list style pointers:
      - left_child  : first child
      - right_sibling: next sibling (sibling list)
    This "left-child right-sibling" representation supports trees of
    arbitrary branching factor using only two pointers per node.
    """

    def __init__(self, data):
        self.data          = data
        self.left_child    = None   # first (leftmost) child
        self.right_sibling = None   # next sibling


class RootedTree:
    """
    Rooted tree using the left-child / right-sibling representation.

    Time Complexities
    -----------------
    add_child  : O(k) where k = number of existing children
    height     : O(n)
    size       : O(n)
    BFS        : O(n)
    DFS        : O(n)
    """

    def __init__(self, root_data):
        self.root = TreeNode(root_data)

    def add_child(self, parent_node, child_data):
        """Add a child to parent_node. O(k) where k = number of children."""
        new_child = TreeNode(child_data)
        if parent_node.left_child is None:
            parent_node.left_child = new_child
        else:
            # Walk the sibling list to the last sibling
            sibling = parent_node.left_child
            while sibling.right_sibling:
                sibling = sibling.right_sibling
            sibling.right_sibling = new_child
        return new_child

    def _children(self, node):
        """Yield all children of node."""
        child = node.left_child
        while child:
            yield child
            child = child.right_sibling

    def height(self, node=None):
        """Return the height of the subtree rooted at node. O(n)."""
        if node is None:
            node = self.root
        children = list(self._children(node))
        if not children:
            return 0
        return 1 + max(self.height(c) for c in children)

    def size(self, node=None):
        """Return the number of nodes in the subtree. O(n)."""
        if node is None:
            node = self.root
        count = 1
        for child in self._children(node):
            count += self.size(child)
        return count

    def bfs(self):
        """Breadth-first traversal. Returns list of node data. O(n)."""
        if not self.root:
            return []
        result = []
        queue  = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.data)
            for child in self._children(node):
                queue.append(child)
        return result

    def dfs(self, node=None, result=None):
        """Depth-first (pre-order) traversal. Returns list of node data. O(n)."""
        if node is None:
            node = self.root
        if result is None:
            result = []
        result.append(node.data)
        for child in self._children(node):
            self.dfs(child, result)
        return result


# ── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("Linked List Demo")
    print("=" * 50)

    ll = LinkedList()
    for v in [10, 20, 30, 40, 50]:
        ll.insert_back(v)
    print(f"After inserts  : {ll}")

    ll.insert_front(5)
    print(f"insert_front(5): {ll}")

    ll.insert_at(3, 25)
    print(f"insert_at(3,25): {ll}")

    ll.delete_front()
    print(f"delete_front() : {ll}")

    ll.delete_back()
    print(f"delete_back()  : {ll}")

    ll.delete_value(25)
    print(f"delete_value(25): {ll}")

    print(f"search(30)     : index {ll.search(30)}")
    print(f"get(2)         : {ll.get(2)}")
    print(f"traverse()     : {ll.traverse()}")

    ll.reverse()
    print(f"After reverse  : {ll}")

    print(f"has_cycle()    : {ll.has_cycle()}")

    print("\n" + "=" * 50)
    print("Rooted Tree Demo")
    print("=" * 50)
    #
    #         A
    #       / | \
    #      B  C  D
    #     / \    |
    #    E   F   G
    #
    tree = RootedTree("A")
    b = tree.add_child(tree.root, "B")
    c = tree.add_child(tree.root, "C")
    d = tree.add_child(tree.root, "D")
    tree.add_child(b, "E")
    tree.add_child(b, "F")
    tree.add_child(d, "G")

    print(f"BFS order : {tree.bfs()}")
    print(f"DFS order : {tree.dfs()}")
    print(f"Height    : {tree.height()}")
    print(f"Size      : {tree.size()}")

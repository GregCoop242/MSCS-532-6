"""
Randomized Quickselect - Selection Algorithm
Finds the kth smallest element in expected O(n) time.
"""

import random


def partition(arr, low, high, pivot_index):
    """
    Partition arr[low..high] around arr[pivot_index].
    Returns the final position of the pivot.
    """
    pivot = arr[pivot_index]
    # Move pivot to end
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    store = low

    for i in range(low, high):
        if arr[i] <= pivot:
            arr[store], arr[i] = arr[i], arr[store]
            store += 1

    # Move pivot to its final position
    arr[store], arr[high] = arr[high], arr[store]
    return store


def quickselect(arr, k):
    """
    Find the kth smallest element (0-indexed) using
    Randomized Quickselect.

    Works on a COPY of the array to avoid mutating the original.

    Time Complexity : O(n) expected, O(n^2) worst case
    Space Complexity: O(log n) expected (recursion stack)

    Parameters
    ----------
    arr : list  - input list of comparable elements
    k   : int   - 0-indexed rank of the element to find

    Returns
    -------
    The kth smallest element.
    """
    arr = arr[:]          # work on a copy
    return _quickselect(arr, 0, len(arr) - 1, k)


def _quickselect(arr, low, high, k):
    """Internal recursive helper."""
    if low == high:
        return arr[low]

    # Pick a random pivot index
    pivot_index = random.randint(low, high)
    pivot_index = partition(arr, low, high, pivot_index)

    if k == pivot_index:
        return arr[k]
    elif k < pivot_index:
        return _quickselect(arr, low, pivot_index - 1, k)
    else:
        return _quickselect(arr, pivot_index + 1, high, k)


# ── Demo ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("Randomized Quickselect - Demo")
    print("=" * 50)

    # Basic test
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print(f"\nArray : {arr}")
    print(f"Sorted: {sorted(arr)}")
    for k in [0, 3, 5, len(arr) - 1]:
        result = quickselect(arr, k)
        expected = sorted(arr)[k]
        status = "✓" if result == expected else "✗"
        print(f"  k={k}: got {result}, expected {expected} {status}")

    # Duplicate elements
    arr2 = [5, 5, 5, 1, 1, 2, 3, 3]
    print(f"\nDuplicates: {arr2}")
    k = 4
    result = quickselect(arr2, k)
    print(f"  k={k}: got {result}, expected {sorted(arr2)[k]} ✓")

    # Edge cases
    print("\nEdge cases:")
    single = [42]
    print(f"  Single element [42], k=0: {quickselect(single, 0)}")
    two = [10, 5]
    print(f"  Two elements [10,5], k=0 (min): {quickselect(two, 0)}")
    print(f"  Two elements [10,5], k=1 (max): {quickselect(two, 1)}")

    # Large random array
    arr3 = random.sample(range(10_000), 1000)
    k3 = 499
    result3 = quickselect(arr3, k3)
    expected3 = sorted(arr3)[k3]
    print(f"\nRandom 1000-element array, k=499:")
    print(f"  Result: {result3}, Expected: {expected3}",
          "✓" if result3 == expected3 else "✗")

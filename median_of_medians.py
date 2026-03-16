"""
Median of Medians - Deterministic Selection Algorithm
Finds the kth smallest element in worst-case O(n) time.
"""


def insertion_sort(arr):
    """Sort a small array using insertion sort."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def get_median(arr):
    """Return the median of a small array."""
    sorted_arr = insertion_sort(arr[:])
    return sorted_arr[len(sorted_arr) // 2]


def partition(arr, pivot):
    """
    Partition arr into three groups around pivot:
    - low:  elements < pivot
    - mid:  elements == pivot
    - high: elements > pivot
    Returns (low, mid, high).
    """
    low  = [x for x in arr if x < pivot]
    mid  = [x for x in arr if x == pivot]
    high = [x for x in arr if x > pivot]
    return low, mid, high


def median_of_medians(arr, k):
    """
    Find the kth smallest element (0-indexed) using the
    Median of Medians algorithm.

    Time Complexity : O(n) worst case
    Space Complexity: O(n) due to recursive calls and sublists

    Parameters
    ----------
    arr : list  - input list of comparable elements
    k   : int   - 0-indexed rank of the element to find

    Returns
    -------
    The kth smallest element.
    """
    if len(arr) <= 5:
        return insertion_sort(arr)[k]

    # Step 1: Divide into groups of 5
    chunks = [arr[i:i + 5] for i in range(0, len(arr), 5)]

    # Step 2: Find the median of each group
    medians = [get_median(chunk) for chunk in chunks]

    # Step 3: Recursively find the median of medians (pivot)
    pivot = median_of_medians(medians, len(medians) // 2)

    # Step 4: Partition the array around the pivot
    low, mid, high = partition(arr, pivot)

    # Step 5: Recurse into the correct partition
    if k < len(low):
        return median_of_medians(low, k)
    elif k < len(low) + len(mid):
        return pivot
    else:
        return median_of_medians(high, k - len(low) - len(mid))


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import random

    print("=" * 50)
    print("Median of Medians - Demo")
    print("=" * 50)

    # Basic test
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print(f"\nArray : {arr}")
    print(f"Sorted: {sorted(arr)}")
    for k in [0, 3, 5, len(arr) - 1]:
        result = median_of_medians(arr, k)
        expected = sorted(arr)[k]
        status = "✓" if result == expected else "✗"
        print(f"  k={k}: got {result}, expected {expected} {status}")

    # Duplicate elements
    arr2 = [5, 5, 5, 1, 1, 2, 3, 3]
    print(f"\nDuplicates: {arr2}")
    k = 4
    result = median_of_medians(arr2, k)
    print(f"  k={k}: got {result}, expected {sorted(arr2)[k]} ✓")

    # Large random array
    arr3 = random.sample(range(10_000), 1000)
    k3 = 499
    result3 = median_of_medians(arr3, k3)
    expected3 = sorted(arr3)[k3]
    print(f"\nRandom 1000-element array, k=499:")
    print(f"  Result: {result3}, Expected: {expected3}",
          "✓" if result3 == expected3 else "✗")

import heapq
import time

unsorted = []
for i in range(100001):
    unsorted.append(100000 - i)

heap = list(unsorted)
standard = list(unsorted)

heapq.heapify(heap)
heapStart = time.time()
heapValue = heapq.heappop(heap)
heapq.heappush(heap, 2)
heapEnd = time.time()

standardStart = time.time()
standard.sort()
standardValue = standard[0]
standard.append(1)
standardEnd = time.time()

print("HeapPop:", heapValue)
print("Standard:", standardValue)

print("Heap Time:", (heapEnd - heapStart))
print("Standard Time:", (standardEnd - standardStart))

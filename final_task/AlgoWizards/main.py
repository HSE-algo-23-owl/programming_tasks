class HeapSort:
    @staticmethod
    def sort(lst):
        HeapSort.create_heap(lst)
        for i in range(1, len(lst)):
            lst[0], lst[len(lst)-i] = lst[len(lst)-i], lst[0]
            HeapSort.sift_down(lst, len(lst)-i, 0)

    @staticmethod
    def create_heap(lst):
        n = len(lst)
        for i in range(n // 2 - 1, -1, -1):
            HeapSort.sift_down(lst, len(lst), i)

    @staticmethod
    def sift_down(lst, n, i):
        left = 2*i + 1
        right = 2*i + 2

        max_idx = left

        if left >= n:
            return

        if right < n and lst[max_idx] < lst[right]:
            max_idx = right

        if lst[i] < lst[max_idx]:
            lst[i], lst[max_idx] = lst[max_idx], lst[i]
            HeapSort.sift_down(lst, n, max_idx)




def main():
    lst = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    HeapSort.sort(lst)
    print(lst)


if __name__ == '__main__':
    main()

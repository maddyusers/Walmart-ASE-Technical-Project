import java.util.ArrayList;
import java.util.NoSuchElementException;

public class PowerOfTwoMaxHeap {
    private ArrayList<Integer> heap;
    private int exponent; // This is the x in 2^x children per node
    private int childrenCount; // This is 2^x

    public PowerOfTwoMaxHeap(int exponent) {
        if (exponent < 0) throw new IllegalArgumentException("Exponent must be non-negative.");
        this.exponent = exponent;
        this.childrenCount = (int) Math.pow(2, exponent);
        this.heap = new ArrayList<>();
    }

    public void insert(int value) {
        heap.add(value);
        siftUp(heap.size() - 1);
    }

    public int popMax() {
        if (heap.isEmpty()) {
            throw new NoSuchElementException("Heap is empty.");
        }

        int maxValue = heap.get(0);
        int lastValue = heap.remove(heap.size() - 1);

        if (!heap.isEmpty()) {
            heap.set(0, lastValue);
            siftDown(0);
        }

        return maxValue;
    }

    private void siftUp(int index) {
        while (index > 0) {
            int parentIndex = getParentIndex(index);
            if (heap.get(index) > heap.get(parentIndex)) {
                swap(index, parentIndex);
                index = parentIndex;
            } else {
                break;
            }
        }
    }

    private void siftDown(int index) {
        while (true) {
            int maxIndex = index;
            for (int i = 1; i <= childrenCount; i++) {
                int childIndex = getChildIndex(index, i);
                if (childIndex < heap.size() && heap.get(childIndex) > heap.get(maxIndex)) {
                    maxIndex = childIndex;
                }
            }
            if (maxIndex == index) {
                break;
            }
            swap(index, maxIndex);
            index = maxIndex;
        }
    }

    private int getParentIndex(int childIndex) {
        return (childIndex - 1) / childrenCount;
    }

    private int getChildIndex(int parentIndex, int childNumber) {
        return childrenCount * parentIndex + childNumber;
    }

    private void swap(int i, int j) {
        int temp = heap.get(i);
        heap.set(i, heap.get(j));
        heap.set(j, temp);
    }

    public static void main(String[] args) {
        testHeapWithExponent(0);
        testHeapWithExponent(1);
        testHeapWithExponent(2);
        testEdgeCases();
    }

    private static void testHeapWithExponent(int exponent) {
        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(exponent);
        System.out.println("Testing heap with exponent " + exponent);

        int[] values = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
        for (int value : values) {
            heap.insert(value);
        }

        System.out.println("Inserted values: " + java.util.Arrays.toString(values));
        
        for (int i = values.length - 1; i >= 0; i--) {
            int max = heap.popMax();
            System.out.println("Expected max: " + values[i] + ", Actual max: " + max);
            assert max == values[i] : "Heap property violated!";
        }

        System.out.println("Heap with exponent " + exponent + " passed all tests.");
        System.out.println();
    }

    private static void testEdgeCases() {
        System.out.println("Testing edge cases");

        PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(1);

        try {
            heap.popMax();
        } catch (NoSuchElementException e) {
            System.out.println("Caught expected exception when popping from empty heap: " + e.getMessage());
        }

        heap.insert(42);
        int max = heap.popMax();
        System.out.println("Expected max: 42, Actual max: " + max);
        assert max == 42 : "Heap property violated for single element!";

        try {
            heap.popMax();
        } catch (NoSuchElementException e) {
            System.out.println("Caught expected exception when popping from empty heap: " + e.getMessage());
        }

        System.out.println("Edge cases passed all tests.");
    }
}

package arrays.com;

import java.util.Arrays;
import java.util.Random;

/**
 * Class implements the following tools:
 * Initialize array of integers,
 * Sort array,
 * Calculates time taken for sorting,
 */
public class ArrayUtils {
    private int[] arrOfIntegers;
    private Random random = new Random();

    public ArrayUtils(int arrayLength, int randomRange) {
        arrOfIntegers = new int[arrayLength];
        for (int i = 0; i < arrOfIntegers.length; i++) {
            arrOfIntegers[i] = random.nextInt(randomRange);
        }
    }///:~

    public int[] getArrayOfints() {
        return arrOfIntegers;
    }

    /**
     * Method implements a "SHAKER" sort or a quick sort
     *
     * @initialArray - array that needs to be sorted;
     * @begin - points to the beginning of an array;
     * @end - points  to the end of array;
     * pivot - number of the array that we will to sort;
     */
    public void shakerSort(int[] initialArray, int begin, int end) {

        int i = begin, j = end;
        int pivot = initialArray[end];
        while (i <= j) {
            while (initialArray[i] < pivot) i++;
            while (initialArray[j] > pivot) j--;
            if (i <= j) {
                exchange(i, j, initialArray);
                i++;
                j--;
            }
        }
        if (begin < j)
            shakerSort(initialArray, begin, j);
        if (i < end)
            shakerSort(initialArray, i, end);

    }  ///:~

    /**
     * Method swap elements in the array
     *
     * @i- value that will be swapped with greater value (j);
     * @j - value that will be swapped with lesser value (i);
     */
    private void exchange(int i, int j, int[] initialArray) {
        int temp = initialArray[i];
        initialArray[i] = initialArray[j];
        initialArray[j] = temp;
    }///:~

    /**
     * Method sort array
     *
     * @arrayOfints- array that needs to be sorted;
     * @sortType - sort type;
     */
    public void sortArray(int[] arrayOfints, SortType sortType) {

        switch (sortType) {
            case BUBBLE:
                int[] arrayOfBubbleSortedints = (int[]) arrayOfints.clone();
                long startBubbleSort = System.currentTimeMillis();
                for (int prevVal = 0; prevVal < arrayOfBubbleSortedints.length; prevVal++) {
                    for (int nextVal = prevVal + 1; nextVal < arrayOfBubbleSortedints.length; nextVal++) {
                        if (arrayOfBubbleSortedints[prevVal] > arrayOfBubbleSortedints[nextVal]) {
                            exchange(prevVal, nextVal, arrayOfBubbleSortedints);
                        }
                    }
                }
                long endBubbleSort = System.currentTimeMillis();
                System.out.println("Time taken : " + (endBubbleSort - startBubbleSort) + " ms for sort of type " + sortType);
                System.out.println(Arrays.toString(arrayOfBubbleSortedints));
                break;

            case SHAKER:
                int[] arrayOfShakerSortedints = arrayOfints.clone();
                long startShakerSort = System.currentTimeMillis();
                shakerSort(arrayOfShakerSortedints, 0, arrayOfShakerSortedints.length - 1);
                long endShakerSort = System.currentTimeMillis();
                System.out.println("Time taken : " + (endShakerSort - startShakerSort) + " ms for sort of type " + sortType);
                System.out.println(Arrays.toString(arrayOfShakerSortedints));
                break;

            default:
                Arrays.sort(arrayOfints);
                System.out.println(Arrays.toString(arrayOfints));
                break;
        }

    } ///:~

}    ///:~ End of Class

package arrays.com;


/**
 * Class for tests
 */
public class Main {


    public static void main(String[] args) {
        ArrayUtils arrayUtils = new ArrayUtils(10, 99);

      arrayUtils.sortArray(arrayUtils.getArrayOfints(), SortType.SHAKER);

    }
}

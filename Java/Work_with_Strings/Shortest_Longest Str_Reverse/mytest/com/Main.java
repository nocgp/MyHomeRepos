package mytest.com;

import java.io.IOException;

/**
 * Class for tests
 */
public class Main {
    public static void main(String[] args)  {
        StringArrInitializer stringArrInitializer = new StringArrInitializer();
        StringsUtil stringsUtil = new StringsUtil();
        try{
            stringArrInitializer.initializeStringArr();
            stringsUtil.compareStrings(stringArrInitializer.getStringArrayList());
            stringsUtil.reverseStrings(stringArrInitializer.getStringArrayList());
            System.out.println(stringsUtil);
        } catch (NullPointerException e){
            System.out.println("\nStrings are empty. Nothing to calculate.. ");
        }

    }
}

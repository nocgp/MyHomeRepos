package mytest.com;

import java.util.ArrayList;

/**
 * Class implements tools for finding the shortest and  the longest  string,
 * View Strings and their length
 * Reverse Strings,
 */
public class StringsUtil {
    private String shortestString;
    private String longestString;
    private int shortestLength;
    private int longestLength;
    private ArrayList<String> reversedArr;

    /**
     * Method for comparing Strings in String array
     *
     * @arrayOfStrings - String array
     */
    public void compareStrings(ArrayList<String> arrayOfStrings) {
        shortestString = arrayOfStrings.get(0);
        shortestLength = arrayOfStrings.get(0).length();

        longestLength = arrayOfStrings.get(0).length();
        longestString = arrayOfStrings.get(0);

        for (String row : arrayOfStrings) {
            if (row.length() > longestLength) {
                longestLength = row.length();
                longestString = row;
            }
            if (row.length() < shortestLength) {
                shortestLength = row.length();
                shortestString = row;
            }

        }
    }      ///:~

    /**
     * Method for reversing original Strings in String array
     *
     * @arrayOfStrings - String array
     */
    public void reverseStrings(ArrayList<String> arrayOfStrings) {
        reversedArr = new ArrayList<String>(arrayOfStrings.size());
        for (String str : arrayOfStrings) {
            reversedArr.add(new StringBuffer(str).reverse().toString());
        }

    }   ///:~

    @Override
    public String toString() {
        return "StringsUtil{" + "\n" +
                "Shortest String='" + shortestString + '\'' +
                ", \nLongest String='" + longestString + '\'' +
                ", \nShortest Length=" + shortestLength +
                ", \nLongest Length=" + longestLength +
                "\n" + "Reversed Strings=" + reversedArr.toString() + "\n" +
                '}';
    } ///:~


} ///:~ End of CLass

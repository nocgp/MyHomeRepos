package mytest.com;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

/**
 * From command line user gives a natural integer n[1..10].
 * Enter n Strings from console, find the shortest and  the longest  string,
 * Reverse Strings,
 * View the result
 */
public class StringArrInitializer {
    private ArrayList<String> stringArrayList;


    /**
     * Method for initializing new ArrayList stringArrayList of Strings,
     * Ask user to give numbers and enter n numbers of Strings
     */
    public void initializeStringArr() {
        System.out.println("Please enter N natural number of Strings :");
        BufferedReader input = new BufferedReader(new InputStreamReader(System.in));

        try {
            String line = input.readLine();
            if (line.isEmpty() || line == null) {
                System.out.println("Dear User! \nYou did not specify number of Strings ");
            } else {
                int numberOfString = Integer.parseInt(line);
                if (numberOfString <= 1 || numberOfString > 10) {
                    System.out.println("Number of Strings greater then 10 \n" + "Or number of Strings less(equals) then 1");
                } else {
                    stringArrayList = new ArrayList<String>(numberOfString);
                    for (int i = 0; i < numberOfString; i++) {
                        System.out.println("Please enter your string :");
                        BufferedReader newStr = new BufferedReader(new InputStreamReader(System.in));
                        stringArrayList.add(newStr.readLine());
                    }
                }

            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (NumberFormatException e) {
            System.out.println("Dear User! \nYour number contains characters or white spaces");
        }

    }    ///:~

    public ArrayList<String> getStringArrayList() {
        return stringArrayList;
    } ///:~

} ///:~ End of Class

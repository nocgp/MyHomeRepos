package Fibonachchi;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 * Class implements tool for finding elements of Fibonacci
 */
public class Fibonacci {


    public static void main(String[] args) {

        String userNum = null;
        System.out.println("How many Fibonachchi elements should I display : ");
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        try {
            userNum = in.readLine();
            if (userNum.isEmpty()) {
                System.out.println("Dear User! Empty line \nis not acceptable number");
            } else {
                int numOfElements = Integer.parseInt(userNum);
                for (int count = 1; count <= numOfElements; count++) {
                    System.out.print("Fib number = " + fubonacciFunc(count) + " ");
                }

            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (NumberFormatException e) {
            System.out.println("Dear User!" + "\nGiven number " + userNum + " is not acceptable number");
        }


    }   ///:~


    public static long fubonacciFunc(long n) {
        if (n == 1) {
            return n;
        } else {
            return fubonacciFunc(n - 1) + fubonacciFunc(n - 2);
        }


    }///:~


}

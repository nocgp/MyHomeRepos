package com.terminal;

import java.math.BigDecimal;
import java.text.NumberFormat;
import java.util.Map;
import java.util.HashMap;
import java.util.Arrays;
import java.util.Locale;
import java.util.regex.Pattern;


/**
 * Класс, реализующий функциональность "Терминала".
 * Основные обязанности: запрос и обработка набора покупок (ввод с клавиатуры),
 * Подсчет общей суммы элементов покупки, вывод суммы с учетом валюты
 */
public class PointOfSaleTerminal {
    private char[] userData;
    private Map<Character, Integer> mapCounter;
    private BigDecimal sumInTotal;


    /**
     * Запросить ввод набора покупок с клавиатуры.
     * Пользователь должен ввести свой набор покупок (A, B, C or D), не разделяя их пробелами.
     * Метод проверяет корректность ввода и записывает набор во внутренний массив userData типа char[]
     * Однотипные элементы набора суммируются, записываются в массив mapCounter типа HashMap<Character, Integer> ()
     *
     * @param userInput - набор покупок пользователя
     */
    public void scanUserInput(String userInput) {

        if (userInput != null && Pattern.matches("[A-B-C-D][^0-9]+", userInput.toUpperCase())) {
            userData = userInput.toUpperCase().toCharArray();
            mapCounter = new HashMap<Character, Integer>();

            for (int i = 0; i < userData.length; i++) {
                if (!mapCounter.containsKey(userData[i])) {
                    mapCounter.put(userData[i], 1);
                } else {
                    mapCounter.put(userData[i], mapCounter.get(userData[i]) + 1);
                }
            }
        } else {
            System.out.println("******************");
            System.out.println("Oops!");
            System.out.println("Please check given items : " + userInput.toUpperCase() + " , One from the following is TRUE :");
            System.out.println("1) You have not entered any items;");
            System.out.println("2) Or your items are not one of the a-b-c-d;");
            System.out.println("3) Or items contain digits like 0-9;");
            System.out.println("******************");
        }
    } ///:~


    /**
     * Подсчет общей суммы покупки.
     *
     * @return sumInTotal  - общая сумма покупки с учетом акций для элементов из набора.
     */
    public BigDecimal calculateTotal() {
        sumInTotal = BigDecimal.valueOf(0.0);
        try {
            for (Map.Entry<Character, Integer> entry : mapCounter.entrySet()) {
                if (entry.getKey() == 'A') {
                    sumInTotal = sumInTotal.add((entry.getValue() % 3 == 0) ? BigDecimal.valueOf(entry.getValue() / 3 * 3) : BigDecimal.valueOf((entry.getValue() / 3 * 3) +
                            (entry.getValue() % 3) * 1.25));
                }
                if (entry.getKey() == 'B') {
                    sumInTotal = sumInTotal.add(BigDecimal.valueOf(entry.getValue() * 4.25));
                }
                if (entry.getKey() == 'C') {
                    sumInTotal = sumInTotal.add((entry.getValue() % 6 == 0) ? BigDecimal.valueOf(entry.getValue() / 6 * 5) : BigDecimal.valueOf((entry.getValue() / 6 * 5) +
                            (entry.getValue() % 6) * 1));
                }
                if (entry.getKey() == 'D') {
                    sumInTotal = sumInTotal.add(BigDecimal.valueOf(entry.getValue() * 0.75));
                }
            }
            return sumInTotal;
        } catch (NullPointerException npe) {
            return BigDecimal.valueOf(0.0);
        }
    } ///:~

    /**
     * Вывод общей суммы на экран с учетом валюты,
     * Вывод элементов набора покупок в последовательности, заданной пользователем
     * Есть несколько вариантов вывода результата на экран:
     *
     * @Override toString(), новый метод vieResult(), форматированный вывод результата в предыдущем методе calculateTotal()
     * Я воспользовалась методом toString() для вывода результата, чтобы не создавать пользовательский метод viewResult()
     */
    @Override
    public String toString() {
        NumberFormat numberFormat = NumberFormat.getCurrencyInstance(Locale.US);
        System.out.println();
        return "Scan these items in the given order: " +
                Arrays.toString(userData) +
                "; Verify the total price is " + numberFormat.format(sumInTotal);

    }///:~


} ///:~ End of PointOfSaleTerminal Class



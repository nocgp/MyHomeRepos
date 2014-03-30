package com.terminal;

import org.junit.Test;
import java.math.BigDecimal;

/**
 * Тестируем Терминал
 */
public class PointOfSaleTerminalJUnitTest{
    PointOfSaleTerminal terminal = new PointOfSaleTerminal();

    @Test
    public void runPo() {
        /**
         * Предоставте набор покупок
         */
        terminal.scanUserInput("ccccccc");

        /**
         * Считаем сумму,
         * Выводим результат
         */
        terminal.calculateTotal();
        BigDecimal result = terminal.calculateTotal();
        System.out.println(terminal + "\n" + result);

    }


}




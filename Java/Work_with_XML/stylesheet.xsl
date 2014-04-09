<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <h1>KF Phone Book</h1>

            <body>

                <table ALIGN="left" BORDER="1" CELLPADDING="4">

                    <tr>

                        <th ALIGN="center">Employee Name</th>
                        <th ALIGN="center">Phone Number</th>
                    </tr>
                    <xsl:for-each select="contactsList/Contact">
                        <tr>

                            <td ALIGN="left">
                                <xsl:value-of select="employeeName"/>
                            </td>
                            <td ALIGN="center">
                                <xsl:value-of select="phoneNumber"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
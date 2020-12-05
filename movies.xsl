<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  version="2.0">
        <xsl:template match="/imdb">
        <html>
            <body>
                <table>
                <tr>
                    <th>Title</th>
                    <th>Genres</th>
                    <th>Year</th>
                </tr>
                <xsl:for-each select="movie">
                    <tr>
                        <td><xsl:value-of select="title"/></td>
                        <td>
                            <xsl:for-each select="genres">
                                <xsl:value-of select="genre"/>
                            </xsl:for-each>
                        </td>
                        <td><xsl:value-of select="year"/></td>
                    </tr>
                </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
        <!--<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">-->

<!--</xsl:stylesheet>-->

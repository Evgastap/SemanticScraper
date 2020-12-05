<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/imdb">
<html>
<body>
<tr>
<th>Title</th>
</tr>
<xsl:for-each select="movie">
<tr>
<xsl:value-of select="year"/>
<xsl:choose>
    <xsl:when test="year = 2020">
     <td>
        <xsl:value-of select="title"/>
     </td>
     </xsl:when>
</xsl:choose>
</tr>
</xsl:for-each>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
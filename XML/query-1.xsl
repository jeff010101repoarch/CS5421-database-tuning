<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
    <h1>Warehouses in Singapore</h1>
    <xsl:for-each select="/warehouses/warehouse[address/country = 'Singapore']">
      <h3>Warehouse name: <xsl:value-of select="name"/></h3>
      <table border="1">
        <tr>
          <td>Item Name</td>
          <td>Item quantity</td>
        </tr>
        <xsl:for-each select="items/item[qty>975]">
            <tr>
              <td><xsl:value-of select="name"/></td>
              <td><xsl:value-of select="qty"/></td>
            </tr>
        </xsl:for-each>
      </table>
    </xsl:for-each>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
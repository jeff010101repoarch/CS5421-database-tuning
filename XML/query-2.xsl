<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
    <h1>Warehouses in Singapore</h1>
      <table border="1">
        <tr>
          <td>Warehouse Name</td>
          <td>Largest quantity item</td>
        </tr>
        <xsl:for-each select="/warehouses/warehouse[address/country = 'Singapore' or address/country ='Malaysia']">
          <tr>
            <td><xsl:value-of select="name"/></td>
            <td><xsl:value-of select="items/item[not(../item/qty > qty)]/name"/></td>
          </tr>
        </xsl:for-each>
      </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
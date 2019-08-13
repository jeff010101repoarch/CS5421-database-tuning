<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
    <h1>Total quantity of Sunscreen in Indonesia</h1>
    <p><xsl:value-of select="sum(/warehouses/warehouse[address/country ='Indonesia']/items/item[name='Sunscreen']/qty/text())"/></p>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
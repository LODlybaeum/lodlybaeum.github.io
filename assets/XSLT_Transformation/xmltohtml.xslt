<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
    
<xsl:output method="html" indent="yes"/>
    
    <!-- Match TEI elements and transform them to HTML -->
    <xsl:template match="/">
        <html>
            <head>
            <link rel="stylesheet" type="text/css" href="style.css" />
                <title>
                    <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
                </title>
            </head>
             <body>
                <h1>
                    <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
                </h1>
                <h3>
                    <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:respStmt/tei:resp"/>:  <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:respStmt/tei:name"/>, <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:publisher"/>
                </h3>
                <table>
                    <tr>
                        <th>Publication Place:</th>
                        <td><xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:pubPlace"/></td>
                    </tr>
                    <tr>
                        <th>Publication Date:</th>
                        <td class='k'><xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:date"/></td>
                    </tr>
                    <tr>
                        <th>Journal:</th>
                        <td><xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:seriesStmt/tei:title"/></td>
                    </tr>
                    <tr>
                        <th>Volume:</th>
                        <td class='k'><xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:seriesStmt/tei:biblScope[@unit='volume']"/></td>
                    </tr>
                    <tr>
                        <th>Pages:</th>
                        <td>
                            <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:seriesStmt/tei:biblScope[@unit='page']/@from"/>-
                            <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:seriesStmt/tei:biblScope[@unit='page']/@to"/>
                        </td>
                    </tr>
                    <tr>
                        <th>ISSN:</th>
                        <td class='k'><xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:seriesStmt/tei:idno"/></td>
                    </tr>
                </table>
                <xsl:apply-templates select="tei:TEI/tei:text/tei:body"/>
            </body>
        </html>
    </xsl:template>
    
    <!-- Match paragraph elements -->
    <xsl:template match="tei:p">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    <!-- Match citations -->
    <xsl:template match="tei:cit">
        <blockquote>
            <xsl:apply-templates/>
        </blockquote>
    </xsl:template>
    
	<!-- Match q's -->
    <xsl:template match="tei:q">
        "<xsl:apply-templates/>"
    </xsl:template>
	
    <!-- Match quotes -->
    <xsl:template match="tei:quote">
        <q>
            <xsl:apply-templates/>
        </q>
    </xsl:template>
    
    <!-- Match titles -->
    <xsl:template match="tei:title">
        <h3>
            <xsl:apply-templates/>
        </h3>
    </xsl:template>
    
    <!-- Match emphasis -->
    <xsl:template match="tei:emph">
        <i>
            <xsl:apply-templates/>
        </i>
    </xsl:template>
    
    <!-- Match bibliographic references -->
    <xsl:template match="tei:bibl">
        <xsl:text>[</xsl:text>
        <i>
            <xsl:apply-templates/>
        </i>
        <xsl:text>]</xsl:text>
    </xsl:template>
    
</xsl:stylesheet>

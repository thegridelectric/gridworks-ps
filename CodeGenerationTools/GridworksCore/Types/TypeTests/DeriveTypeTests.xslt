<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl" xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xsl:output method="xml" indent="yes" />
    <xsl:param name="root" />
    <xsl:param name="codee-root" />
    <xsl:include href="../CommonXsltTemplates.xslt"/>
    <xsl:param name="exclude-collections" select="'false'" />
    <xsl:param name="relationship-suffix" select="''" />
    <xsl:variable name="airtable" select="/" />
    <xsl:variable name="squot">'</xsl:variable>
    <xsl:variable name="init-space">             </xsl:variable>
    <xsl:include href="GnfCommon.xslt"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>

    <xsl:template match="/">
        <FileSet>
            <FileSetFiles>
                <xsl:for-each select="$airtable//ProtocolTypes/ProtocolType[(normalize-space(ProtocolName) ='gwprice')]">
                <xsl:variable name="versioned-type-id" select="VersionedType"/>
                <xsl:for-each select="$airtable//VersionedTypes/VersionedType[(VersionedTypeId = $versioned-type-id)  and (Status = 'Active' or Status = 'Pending') and (ProtocolCategory = 'Json' or ProtocolCategory = 'GwAlgoSerial')]">
                <xsl:variable name="type-name" select="TypeName"/>
                <xsl:variable name="class-name">
                    <xsl:choose>
                    <xsl:when test="normalize-space(PythonClassName)=''">
                    <xsl:call-template name="nt-case">
                        <xsl:with-param name="type-name-text" select="$type-name" />
                    </xsl:call-template>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="PythonClassName" />
                    </xsl:otherwise>

                    </xsl:choose>
                </xsl:variable>
                <xsl:variable name="overwrite-mode">

                    <xsl:if test="not (Status = 'Pending')">
                    <xsl:text>Never</xsl:text>
                    </xsl:if>
                    <xsl:if test="(Status = 'Pending')">
                    <xsl:text>Always</xsl:text>
                    </xsl:if>
                    </xsl:variable>
                <FileSetFile>
                            <xsl:element name="RelativePath"><xsl:text>../../../../tests/types/test_</xsl:text>
                            <xsl:value-of select="translate($type-name,'.','_')"/><xsl:text>.py</xsl:text></xsl:element>

                    <OverwriteMode><xsl:value-of select="$overwrite-mode"/></OverwriteMode>
                    <xsl:element name="FileContents">

<xsl:text>"""Tests </xsl:text><xsl:value-of select="$type-name"/><xsl:text> type, version </xsl:text>
<xsl:value-of select="Version"/>
<xsl:text>"""
</xsl:text>
<xsl:for-each select="$airtable//GtEnums//GtEnum[normalize-space(Name) !='']">
<xsl:sort select="Name" data-type="text"/>

<xsl:variable name="base-name" select="LocalName"/>
<xsl:variable name="enum-local-name">
<xsl:call-template name="nt-case">
    <xsl:with-param name="type-name-text" select="LocalName" />
</xsl:call-template>
</xsl:variable>
<xsl:if test="count($airtable//TypeAttributes/TypeAttribute[(VersionedType = $versioned-type-id) and (EnumLocalName[text() = $base-name])])>0">

<xsl:text>
from gwprice.enums import </xsl:text>
<xsl:value-of select="$enum-local-name"/>

</xsl:if>

</xsl:for-each>

<xsl:choose>
<xsl:when test="(NotInInit='true')">
<xsl:text>
from gwprice.types.</xsl:text><xsl:value-of select="translate($type-name,'.','_')"/>
<xsl:text> import </xsl:text><xsl:value-of select="$class-name"/>
</xsl:when>

<xsl:otherwise>
<xsl:text>
from gwprice.types import </xsl:text><xsl:value-of select="$class-name"/>
</xsl:otherwise>

</xsl:choose>

<xsl:text>


def test_</xsl:text><xsl:value-of select="translate($type-name,'.','_')"/>
<xsl:text>_generated() -> None:
    t = </xsl:text><xsl:value-of select="$class-name"/><xsl:text>(</xsl:text>
                <xsl:for-each select="$airtable//TypeAttributes/TypeAttribute[(VersionedType = $versioned-type-id)]">
        <xsl:sort select="Idx" data-type="number"/>
        <xsl:variable name = "attribute-name">
        <xsl:call-template name="python-case">
            <xsl:with-param name="camel-case-text" select="Value"/>
        </xsl:call-template>

        <!-- If attribute is associated to a data class, add Id to the Attribute name-->
        <xsl:if test="not(normalize-space(SubTypeDataClass) = '') and not(IsList='true')">
        <xsl:text>_id</xsl:text>
        </xsl:if>
        </xsl:variable>
        <xsl:text>&#10;        </xsl:text>
        <xsl:value-of select="$attribute-name"  />
        <xsl:text>=</xsl:text>
        <xsl:if test="not(IsEnum='true')">
        <xsl:value-of select="normalize-space(TestValue)"/>
        </xsl:if>
         <xsl:if test="(IsEnum='true') and not(IsList='true')">
        <xsl:call-template name="nt-case">
                <xsl:with-param name="type-name-text" select="EnumLocalName" />
        </xsl:call-template>
         <xsl:text>.</xsl:text>
        <xsl:value-of select="EnumTestTranslation"/>
        </xsl:if>
        <xsl:if test="(IsEnum='true') and (IsList='true')">
        <xsl:value-of select="EnumTestTranslation"/>
        </xsl:if>

        <xsl:text>,</xsl:text>
        </xsl:for-each>

    <xsl:text>
    )

    d = {</xsl:text>
        <xsl:for-each select="$airtable//TypeAttributes/TypeAttribute[(VersionedType = $versioned-type-id)]">
        <xsl:sort select="Idx" data-type="number"/>
        <xsl:variable name = "attribute-name">
        <xsl:value-of select="Value"/>
        <!-- If attribute is associated to a data class, add Id to the Attribute name-->
        <xsl:if test="not(normalize-space(SubTypeDataClass) = '') and not(IsList='true')">
        <xsl:text>Id</xsl:text>
        </xsl:if>
        </xsl:variable>

        <xsl:if test="(not (IsEnum = 'true')) or (IsList = 'true')">
        <xsl:text>
        "</xsl:text><xsl:value-of select="$attribute-name"  />
        <xsl:text>": </xsl:text>
        <xsl:value-of select="normalize-space(TestValue)"/>
        <xsl:text>,</xsl:text>
        </xsl:if>

        <xsl:if test="(IsEnum = 'true') and not (IsList = 'true')">
        <xsl:text>
        "</xsl:text><xsl:value-of select="Value"  />
        <xsl:text>": "</xsl:text>
        <xsl:value-of select="normalize-space(EnumTestTranslation)"/>
            <xsl:text>",</xsl:text>
        </xsl:if>



        </xsl:for-each>
    <xsl:text>
        "TypeName": "</xsl:text><xsl:value-of select="$type-name"/><xsl:text>",
        "Version": "</xsl:text><xsl:value-of select="Version"/><xsl:text>",
    }

    assert t.to_dict() == d
    assert t == </xsl:text><xsl:value-of select="$class-name"/><xsl:text>.from_dict(d)</xsl:text>
    <xsl:if test="count($airtable//TypeAttributes/TypeAttribute[(VersionedType = $versioned-type-id) and (IsEnum='true')]) > 0">
    <xsl:text>

    d2 = d.copy()</xsl:text>
    <xsl:for-each select="$airtable//TypeAttributes/TypeAttribute[(VersionedType = $versioned-type-id) and (IsEnum='true')]">
    <xsl:if test="not (IsList = 'true')">
    <xsl:text>
    del d2["</xsl:text><xsl:value-of select="Value"/><xsl:text>"]
    d2["</xsl:text><xsl:value-of select="Value"/><xsl:text>GtEnumSymbol"] = </xsl:text>
    </xsl:if>
    <xsl:if test="(IsList='true')">
    <xsl:text>
    d2["</xsl:text><xsl:value-of select="Value"/><xsl:text>"] = </xsl:text>
    </xsl:if>
    <xsl:value-of select="normalize-space(TestValue)"/>
    <xsl:text></xsl:text>
    </xsl:for-each>
    <xsl:text>
    assert t == </xsl:text><xsl:value-of select="$class-name"/><xsl:text>.from_dict(d2)</xsl:text>
    </xsl:if>
    <xsl:text>

    </xsl:text>
    <xsl:if test="count($airtable//TypeAttributes/TypeAttribute[(VersionedType = $versioned-type-id) and (IsEnum = 'true') and not (IsList = 'true')]) >0">
    <xsl:text>

    ######################################
    # Behavior on unknown enum values: sends to default
    ######################################</xsl:text>
    <xsl:for-each select="$airtable//TypeAttributes/TypeAttribute[(VersionedType = $versioned-type-id) and (IsEnum = 'true') and not (IsList = 'true')]">
    <xsl:sort select="Idx" data-type="number"/>
    <xsl:variable name="attribute"><xsl:value-of select="Value"/></xsl:variable>
    <xsl:text>

    d2 = dict(d, </xsl:text>
    <xsl:value-of select="Value"/>
    <xsl:text>="unknown_enum_thing")
    assert </xsl:text>
   <xsl:value-of select="$class-name"/>
    <xsl:text>.from_dict(d2).</xsl:text>
    <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="Value"/>
    </xsl:call-template>
    <xsl:text> == </xsl:text>
    <xsl:call-template name="nt-case">
        <xsl:with-param name="type-name-text" select="EnumLocalName" />
    </xsl:call-template>
    <xsl:text>.default()</xsl:text>


    </xsl:for-each>
    </xsl:if>

<xsl:text>&#10;</xsl:text>

                        </xsl:element>
                     </FileSetFile>
                </xsl:for-each>
                </xsl:for-each>
            </FileSetFiles>
        </FileSet>
    </xsl:template>



</xsl:stylesheet>

<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
 <html><head>
<title>InfoINI Status</title><style type="text/css">
html,body,div,span,applet,object,iframe,h1,h2,h3,h4,h5,h6,p,blockquote,pre,a,abbr,acronym,address,big,cite,code,del,dfn,em,font,img,ins,kbd,q,s,samp,small,strike,strong,sub,sup,tt,var,b,u,i,center,dl,dt,dd,ol,ul,li,fieldset,form,label,legend,table,caption,tbody,tfoot,thead,tr,th,td{margin:0;padding:0;border:0;outline:0;font-size:100%;vertical-align:baseline;background:transparent}body{line-height:1}ol,ul{list-style:none}blockquote,q{quotes:none}blockquote:before,blockquote:after,q:before,q:after{content:'';content:none}:focus{outline:0}ins{text-decoration:none}del{text-decoration:line-through}table{border-collapse:collapse;border-spacing:0}
body{font:13px/1.5 'Helvetica Neue',Arial,'Liberation Sans',FreeSans,sans-serif}a:focus{outline:1px dotted}hr{border:0 #ccc solid;border-top-width:1px;clear:both;height:0}h1{font-size:25px}h2{font-size:23px}h3{font-size:21px}h4{font-size:19px}h5{font-size:17px}h6{font-size:15px}ol{list-style:decimal}ul{list-style:disc}li{margin-left:30px}p,dl,hr,h1,h2,h3,h4,h5,h6,ol,ul,pre,table,address,fieldset{margin-bottom:20px}

body{background-color: #232323; color: #fff;font-size:1.4em;margin:1em;}
.block {
        color: #fff !important; text-align: center; margin: auto;
        background: #343434;
color:black;
-moz-border-radius:15px;
-webkit-border-radius:15px;
border-radius:15px;
/*IE DOES NOT SUPPORT BORDER RADIUS*/
-moz-box-shadow:0px 0px 1px #000000;
-webkit-box-shadow:0px 0px 1px #000000;
box-shadow:0px 0px 1px #000000;
/*IE DOES NOT SUPPORT BLUR PROPERTY OF SHADOWS*/
padding: 1em;
margin-bottom: 1em;
color: black;
}
h1 {font-size:1.3em;}
h2 {font-size:1.2em;}
</style>
 </head><body>
    <h1>InfoINI-Status</h1>
    <div class="block">
        <h2>Tür</h2>
        <xsl:if test="infoini/door[@isOpen='true']">
            <div class="tuer open"> Tür offen </div>
        </xsl:if>
        <xsl:if test="infoini/door[@isOpen='false']">
            <div class="tuer closed"> Tür geschlossen </div>
        </xsl:if>
    </div>
    <div class="block">
        <h2>Kaffeekannen</h2>
        <xsl:for-each select="/infoini/cafe/pot">
        <div class="pot">
            <div style="float:right;"><xsl:value-of select="level"/>%</div>
            <p><xsl:value-of select="status"/></p>
        </div>
        </xsl:for-each>
    </div>
 </body></html>
</xsl:template>
</xsl:stylesheet>

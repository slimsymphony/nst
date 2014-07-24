<xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
      <head runat="server">
        <META http-equiv="Content-Type" content="text/html; charset=UTF-8"></META>
        <title>NTS WEB SERVER</title>
        <style type="text/css">
          body {
          font:normal 100% verdana,arial,helvetica;
          color:#000000;
          }
          table tr td, table tr th {
          font-size: 80%;
          }
          table.details tr th{
          font-weight: bold;
          text-align:left;
          background:#a6caf0;
          }
          table.details tr td{
          background:#eeeee0;
          }

          p {
          line-height:1.5em;
          margin-top:0.5em; margin-bottom:1.0em;
          }
          h1 {
          margin: 0px 0px 5px; font: 165% verdana,arial,helvetica
          }
          h2 {
          margin-top: 1em; margin-bottom: 0.5em; font: bold 125% verdana,arial,helvetica
          }
          h3 {
          margin-bottom: 0.5em; font: bold 115% verdana,arial,helvetica
          }
          h4 {
          margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
          }
          h5 {
          margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
          }
          h6 {
          margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
          }
          .Error {
          font-weight:bold; color:red;
          }
          .Failure {
          font-weight:bold; color:purple;
          }
          .Properties {
          text-align:right;
          }
        </style>
        <script language="JavaScript">
          var TestCases = new Array();
          var cur;
        </script>
        <script language="JavaScript">
          <![CDATA[
            showFullMessage = function(id){
              document.getElementById(id).style.display='none';
              document.getElementById(id+'-full').style.display='inline';
            }
          ]]>
        </script>
      </head>
      <body>
        <a name="top"></a>
        <h1>
          NST MTBF Test Crash View [<xsl:value-of select="root/DeviceInfo/DeviceID"/> - <xsl:value-of select="root/DeviceInfo/TestPlan"/>]
        </h1>
        <table class="details" width="100%" id="logdg" >
          <thead>
            <tr>
              <th field="process" width="20%">
                Process
              </th>
              <th field="time" width="20%">
                Last Throw Time
              </th>
              <th field="type" width="20%">
                Type
              </th>
              <th field="count" align="center" width="10%">
                Count
              </th>
              <th field="build" width="30%">
                Message
              </th>
            </tr>
          </thead>
          <xsl:for-each select="/root/CrashGeneralList/CrashGeneral">
            <tr>
              <td>
                <xsl:value-of select="Process"/>
              </td>
              <td>
                <xsl:value-of select="LastThrowTime"/>
              </td>
              <td>
                <xsl:value-of select="Type"/>
              </td>
              <td>
                <xsl:value-of select="Count"/>
              </td>
              <td>
                <span>
                  <xsl:attribute name="id"><xsl:value-of select="ID"/></xsl:attribute>
                  <xsl:value-of select="substring(Message,0,50)"/>
                  <a href="javascript:void(0)">
                    <xsl:attribute name="onclick">showFullMessage('<xsl:value-of select="ID"/>')</xsl:attribute>
                    ( More ...)
                  </a>
                </span>
                <span style="display:none;">
                  <xsl:attribute name="id"><xsl:value-of select="ID"/>-full</xsl:attribute>
                  <xsl:value-of select="Message"/>
                </span>
              </td>
            </tr>
            <tr>
              <td colspan="5" style=" padding-left:50px">
                <table width="100%" class="details">
                  <tr>
                    <th width="10%">
                      Date Time
                    </th>
                    <th width="40%">
                      Case
                    </th>
                    <th width="10%">
                      Process
                    </th>
                    <th width="30%">
                      Build
                    </th>
                    <th width="10%">
                      ADB Log
                    </th>
                  </tr>
                  <xsl:variable name="GeneraID" select="ID"></xsl:variable>
                  <xsl:for-each select="/root/CrashDetailList/CrashDetail[GeneraID = $GeneraID]">
                    <tr>
                      <td>
                        <xsl:value-of select="DateTime"/>
                      </td>
                      <td>
                        <a target="_blank">
                          <xsl:attribute name="href">
                            <xsl:value-of select="Case"/>
                          </xsl:attribute>
                          <xsl:value-of select="Case"/>
                        </a>
                      </td>
                      <td>
                        <xsl:value-of select="Process"/>
                      </td>
                      <td>
                        <xsl:value-of select="Build"/>
                      </td>
                      <td>
                        <xsl:variable name="title" select="Title"></xsl:variable>
                        
                        <xsl:for-each select="LogType">
                          <a target="_blank">
                            <xsl:attribute name="href"><xsl:value-of select="$title"/>/<xsl:value-of select="Value"/>.1.adb.xml</xsl:attribute>
                            <xsl:value-of select="Value"/>
                          </a>
                          <br/>
                        </xsl:for-each>
                      </td>
                    </tr>
                  </xsl:for-each>
                </table>
              </td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
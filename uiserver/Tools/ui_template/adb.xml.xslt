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
          NST ADB LOG
        </h1>
        <table>
          <tr>
            <td width="100px">
              <xsl:if test="/root/ADBLogList/ADBLog[1]/Page > 1">
                <a>
                  <xsl:attribute name="href">
                    <xsl:value-of select="/root/ADBLogList/ADBLog[1]/LogType"/>.<xsl:value-of select="/root/ADBLogList/ADBLog[1]/Page - 1"/>.adb.xml
                  </xsl:attribute>
                  Previous
                </a>
              </xsl:if>
            </td>
            <td  width="100px">
              <a>
                <xsl:attribute name="href">
                  <xsl:value-of select="/root/ADBLogList/ADBLog[1]/LogType"/>.<xsl:value-of select="/root/ADBLogList/ADBLog[1]/Page + 1"/>.adb.xml
                </xsl:attribute>
                Next
              </a>
            </td>
          </tr>
        </table>

        <h2>
          <xsl:value-of select="/root/ADBLogList/ADBLog[1]/LogType"/>
        </h2>

        <table class="details" width="100%" id="logdg" >
          <thead>
            <tr>
              <th field="process" width="20%">
                Date Time
              </th>
              <th field="time" width="80%">
                Message
              </th>
            </tr>
          </thead>
          <xsl:for-each select="/root/ADBLogList/ADBLog">
            <tr>
              <td>
                <xsl:value-of select="DateTime"/>
              </td>
              <td>
                <xsl:value-of select="Content"/>
              </td>
            </tr>
          </xsl:for-each>
        </table>

        <table>
          <tr>
            <td width="100px">
              <xsl:if test="/root/ADBLogList/ADBLog[1]/Page > 1">
                <a>
                  <xsl:attribute name="href">
                    <xsl:value-of select="/root/ADBLogList/ADBLog[1]/LogType"/>.<xsl:value-of select="/root/ADBLogList/ADBLog[1]/Page - 1"/>.adb.xml
                  </xsl:attribute>
                  Previous
                </a>
              </xsl:if>
            </td>
            <td  width="100px">
              <a>
                <xsl:attribute name="href">
                  <xsl:value-of select="/root/ADBLogList/ADBLog[1]/LogType"/>.<xsl:value-of select="/root/ADBLogList/ADBLog[1]/Page + 1"/>.adb.xml
                </xsl:attribute>
                Next
              </a>
            </td>
          </tr>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
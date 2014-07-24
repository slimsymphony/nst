<xsl:stylesheet	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" indent="yes"/>
<xsl:decimal-format decimal-separator="." grouping-separator="," />

<xsl:template match="testsuites">
	<HTML>
		<HEAD>
    <style type="text/css">
      body {
      	font:normal 68% verdana,arial,helvetica;
      	color:#000000;
      }
      table tr td, table tr th {
          font-size: 68%;
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
        <xsl:for-each select="./testsuite">      
            <xsl:apply-templates select="properties"/>
        </xsl:for-each>

       </script>
       <script language="JavaScript"><![CDATA[
        function displayProperties (name) {
          var win = window.open('','JUnitSystemProperties','scrollbars=1,resizable=1');
          var doc = win.document.open();
          doc.write("<html><head><title>Properties of " + name + "</title>");
          doc.write("<style>")
          doc.write("body {font:normal 68% verdana,arial,helvetica;	color:#000000; }");
          doc.write("table tr td, table tr th { font-size: 68%; }");
          doc.write("table.properties { border-collapse:collapse; border-left:solid 1 #cccccc; border-top:solid 1 #cccccc; padding:5px; }");
          doc.write("table.properties th { text-align:left; border-right:solid 1 #cccccc; border-bottom:solid 1 #cccccc; background-color:#eeeeee; }");
          doc.write("table.properties td { font:normal; text-align:left; border-right:solid 1 #cccccc; border-bottom:solid 1 #cccccc; background-color:#fffffff; }");
          doc.write("h3 { margin-bottom: 0.5em; font: bold 115% verdana,arial,helvetica }");
          doc.write("</style>");
          doc.write("</head><body>");
          doc.write("<h3>Properties of " + name + "</h3>");
          doc.write("<div align=\"right\"><a href=\"javascript:window.close();\">Close</a></div>");
          doc.write("<table class='properties'>");
          doc.write("<tr><th>Name</th><th>Value</th></tr>");
          for (prop in TestCases[name]) {
            doc.write("<tr><th>" + prop + "</th><td>" + TestCases[name][prop] + "</td></tr>");
          }
          doc.write("</table>");
          doc.write("</body></html>");
          doc.close();
          win.focus();
        }
      ]]>  
      </script>
		</HEAD>
		<body>
			<a name="top"></a>
			<xsl:call-template name="pageHeader"/>	
			
			<!-- Summary part -->
			<xsl:call-template name="summary"/>
			<hr size="1" width="95%" align="left"/>
			
			<!-- Task List part -->
			<xsl:call-template name="testtasklist"/>
			<hr size="1" width="95%" align="left"/>
			
			<!-- For each class create the  part -->
			<xsl:call-template name="classes"/>
			
		</body>
	</HTML>
</xsl:template>
	
	
	
	<!-- ================================================================== -->
	<!-- Write a list of all task with an hyperlink to the anchor of    -->
	<!-- of the test task name.                                               -->
	<!-- ================================================================== -->
	<xsl:template name="testtasklist">	
		<h2>Test tasks</h2>
		Note: Test tasks statistics are not computed recursively, they only sum up all of its tasks numbers.
		<table class="details" border="0" cellpadding="13" cellspacing="2" width="95%">
			<xsl:call-template name="testsuite.test.header"/>
			<!-- list all test tasks recursively -->
			<xsl:for-each select="./testsuite[not(./@name = preceding-sibling::testsuite/@name)]">
				<xsl:variable name="testsuites-in-task" select="/testsuites/testsuite[./@name = current()/@name]"/>
				<xsl:variable name="testCount" select="sum($testsuites-in-task/@tests)"/>
				<xsl:variable name="errorCount" select="sum($testsuites-in-task/@errors)"/>
				<xsl:variable name="failureCount" select="sum($testsuites-in-task/@failures)"/>
				<xsl:variable name="timeCount" select="sum($testsuites-in-task/@time) div 60 div 60"/>
				<xsl:variable name="systemTombstoneCount" select="sum($testsuites-in-task/@systemTombstone)"/>
				<xsl:variable name="systemAppCrashCount" select="sum($testsuites-in-task/@systemAppCrash)"/>
				<xsl:variable name="systemAppAnrCount" select="sum($testsuites-in-task/@systemAppAnr)"/>
				<xsl:variable name="dataAppCrashCount" select="sum($testsuites-in-task/@dataAppCrash)"/>
				<xsl:variable name="dataAppAnrCount" select="sum($testsuites-in-task/@dataAppAnr)"/>
				<xsl:variable name="systemServerCrashCount" select="sum($testsuites-in-task/@systemServerCrash)"/>
				<xsl:variable name="systemServerWatchdogCount" select="sum($testsuites-in-task/@systemServerWatchdog)"/>
				<xsl:variable name="systemRestartCount" select="sum($testsuites-in-task/@systemRestart)"/>
				<xsl:variable name="systemServerLowmemCount" select="sum($testsuites-in-task/@systemServerLowmem)"/>
                <xsl:variable name="freezeCount" select="sum($testsuites-in-task/@freeze)"/>
                <xsl:variable name="ramdumpCount" select="sum($testsuites-in-task/@ramdump)"/>
                <xsl:variable name="outofmemCount" select="sum($testsuites-in-task/@outofmemory)"/>
                <xsl:variable name="successRate" select="(@tests - @failures) div @tests"/>
				
				<!-- write a summary for the test task -->
				<tr valign="top">
					<!-- set a nice color depending if there is an error/failure -->
					<xsl:attribute name="class">
						<xsl:choose>
							<xsl:when test="$failureCount &gt; 0">Failure</xsl:when>
							<xsl:when test="$errorCount &gt; 0">Error</xsl:when>
						</xsl:choose>
					</xsl:attribute>
					<td><a href="#{@name}"><xsl:value-of select="@name"/></a></td>
					<td><xsl:value-of select="$testCount"/></td>
					<td><xsl:call-template name="display-percent">
						<xsl:with-param name="value" select="$successRate"/>
					</xsl:call-template></td>
					<td><xsl:value-of select="$systemTombstoneCount"/></td>
					<td><xsl:value-of select="$systemAppCrashCount"/></td>
					<td><xsl:value-of select="$systemAppAnrCount"/></td>
					<td><xsl:value-of select="$dataAppCrashCount"/></td>
					<td><xsl:value-of select="$dataAppAnrCount"/></td>
					<td><xsl:value-of select="$systemServerCrashCount"/></td>
					<td><xsl:value-of select="$systemServerWatchdogCount"/></td>
					<td><xsl:value-of select="$systemRestartCount"/></td>
					<td><xsl:value-of select="$systemServerLowmemCount"/></td>
                    <td><xsl:value-of select="$freezeCount"/></td>
                    <!--<td>
                        <xsl:value-of select="$ramdumpCount"/>
                    </td>
                    <td>
                        <xsl:value-of select="$outofmemCount"/>
                    </td>-->
                    <td>
					<xsl:call-template name="display-time">
						<xsl:with-param name="value" select="$timeCount"/>
					</xsl:call-template>H
					</td>
				</tr>
			</xsl:for-each>
		</table>		
	</xsl:template>
	
	
	<!-- ================================================================== -->
	<!-- Write a package level report                                       -->
	<!-- It creates a table with values from the document:                  -->
	<!-- Name | Tests | Errors | Failures | Time                            -->
	<!-- ================================================================== -->
	
	<xsl:template name="classes">
		<xsl:for-each select="testsuite">
			<!-- create an anchor to this class name -->
			<a name="{@name}"></a>
			<h3><xsl:value-of select="@name"/></h3>
			
			<table class="details" border="0" cellpadding="6" cellspacing="2" width="95%">
			  <xsl:call-template name="testcase.test.header"/>
			  <!--
			  test can even not be started at all (failure to load the class)
			  so report the error directly
			  -->
				<xsl:if test="./error">
					<tr class="Error">
						<td colspan="4"><xsl:apply-templates select="./error"/></td>
					</tr>
				</xsl:if>
				<xsl:apply-templates select="./testcase" mode="print.test"/>
			</table>
			<p/>
			
			<a href="#top">Back to top</a>
		</xsl:for-each>
	</xsl:template>
	
	<xsl:template name="summary">
		<h2>Summary</h2>
		<xsl:variable name="testCount" select="sum(testsuite/@tests)"/>
		<xsl:variable name="systemTombstoneCount" select="sum(testsuite/@systemTombstone)"/>
		<xsl:variable name="systemAppCrashCount" select="sum(testsuite/@systemAppCrash)"/>
		<xsl:variable name="systemAppAnrCount" select="sum(testsuite/@systemAppAnr)"/>
		<xsl:variable name="dataAppCrashCount" select="sum(testsuite/@dataAppCrash)"/>
		<xsl:variable name="dataAppAnrCount" select="sum(testsuite/@dataAppAnr)"/>
		<xsl:variable name="systemServerCrashCount" select="sum(testsuite/@systemServerCrash)"/>
		<xsl:variable name="systemServerWatchdogCount" select="sum(testsuite/@systemServerWatchdog)"/>
		<xsl:variable name="systemRestartCount" select="sum(testsuite/@systemRestart)"/>
		<xsl:variable name="systemServerLowmemCount" select="sum(testsuite/@systemServerLowmem)"/>
		<xsl:variable name="freezeCount" select="sum(testsuite/@freeze)"/>
        <xsl:variable name="ramdumpCount" select="sum(testsuite/@ramdump)"/>
        <xsl:variable name="outofmemCount" select="sum(testsuite/@outofmemory)"/>
        <xsl:variable name="errorCount" select="sum(testsuite/@errors)"/>
		<xsl:variable name="failureCount" select="sum(testsuite/@failures)"/>
		<xsl:variable name="timeCount" select="sum(testsuite/@time) div 60 div 60"/>
		<xsl:variable name="successRate" select="($testCount - $failureCount) div $testCount"/>
		<table class="details" border="0" cellpadding="15" cellspacing="2" width="95%">
		<tr valign="top">
			<th>Tests</th>
			<th>SYS_TOMBSTONE</th>
			<th>sys_app_crash</th>
			<th>sys_app_anr</th>
			<th>data_app_crash</th>
			<th>data_app_anr</th>
			<th>sys_server_crash</th>
			<th>sys_server_watchdog</th>
			<th>SYS_RESTART</th>
			<th>sys_server_lowmem</th>
            <th>freeze</th>
            <!--<th>memory_dump</th>
            <th>out_of_memory</th>-->
            <th>Success rate</th>
			<th>Time</th>
		</tr>
		<tr valign="top">
			<xsl:attribute name="class">
				<xsl:choose>
					<xsl:when test="$failureCount &gt; 0">Failure</xsl:when>
					<xsl:when test="$errorCount &gt; 0">Error</xsl:when>
				</xsl:choose>
			</xsl:attribute>
			<td><xsl:value-of select="$testCount"/></td>
			<td><xsl:value-of select="$systemTombstoneCount"/></td>
			<td><xsl:value-of select="$systemAppCrashCount"/></td>
			<td><xsl:value-of select="$systemAppAnrCount"/></td>
			<td><xsl:value-of select="$dataAppCrashCount"/></td>
			<td><xsl:value-of select="$dataAppAnrCount"/></td>
			<td><xsl:value-of select="$systemServerCrashCount"/></td>
			<td><xsl:value-of select="$systemServerWatchdogCount"/></td>
			<td><xsl:value-of select="$systemRestartCount"/></td>
			<td><xsl:value-of select="$systemServerLowmemCount"/></td>
			<td><xsl:value-of select="$freezeCount"/></td>
            <!--<td>
                <xsl:value-of select="$ramdumpCount"/>
            </td>
            <td>
                <xsl:value-of select="$outofmemCount"/>
            </td>-->
            <td>
				<xsl:call-template name="display-percent">
					<xsl:with-param name="value" select="$successRate"/>
				</xsl:call-template>
			</td>
			<td>
				<xsl:call-template name="display-time">
					<xsl:with-param name="value" select="$timeCount"/>
				</xsl:call-template> H
			</td>

		</tr>
		</table>
		<table border="0" width="95%">
		<tr>
		<td	style="text-align: justify;">
		Note: <i>failures</i> are anticipated and checked for with assertions while <i>errors</i> are unanticipated.
		</td>
		</tr>
		</table>
	</xsl:template>
	
  <!--
   Write properties into a JavaScript data structure.
   This is based on the original idea by Erik Hatcher (erik@hatcher.net)
   -->
  <xsl:template match="properties">
    cur = TestCases['<xsl:value-of select="../@name"/>.<xsl:value-of select="../@name"/>'] = new Array();
  	<xsl:for-each select="property">
    <xsl:sort select="@name"/>
        cur['<xsl:value-of select="@name"/>'] = '<xsl:call-template name="JS-escape"><xsl:with-param name="string" select="@value"/></xsl:call-template>';
  	</xsl:for-each>
  </xsl:template>
	
<!-- Page HEADER -->
<xsl:template name="pageHeader">
	<h1>NST MTBF Test Result [<xsl:value-of select="/testsuites/@deviceID"/>] </h1>
	<table width="100%">
	<tr>
		<td align="left"></td>
		<td align="right">Designed for use with <a href='#'>NST</a> and <a href='#'>NTA</a>.</td>
	</tr>
	</table>
	<hr size="1"/>
</xsl:template>

<xsl:template match="testsuite" mode="header">
	<tr valign="top">
		<th width="80%">Name</th>
		<th>Tests</th>
		<th>Errors</th>
		<th>Failures</th>
		<th nowrap="nowrap">Time(s)</th>
	</tr>
</xsl:template>

<!-- class header -->
<xsl:template name="testsuite.test.header">
	<tr valign="top">
		<th width="10%">Name</th>
		<th>Tests</th>
		<th>Success rate</th>
		<th>SYS_TOMBSTONE</th>
		<th>sys_app_crash</th>
		<th>sys_app_anr</th>
		<th>data_app_crash</th>
		<th>data_app_anr</th>
		<th>sys_server_crash</th>
		<th>sys_server_watchdog</th>
		<th>SYS_RESTART</th>
		<th>sys_server_lowmem</th>
        <th>freeze</th>
        <!--<th>memory_dump</th>
        <th>out_of_memory</th>-->
        <th nowrap="nowrap">Time(s)</th>
	</tr>
</xsl:template>

<!-- method header -->
<xsl:template name="testcase.test.header">
	<tr valign="top">
		<th>No.</th>
		<th>Script</th>
		<th>Start Time</th>
		<th nowrap="nowrap">Time(s)</th>
		<th>Status</th>
		<th>Log</th>
		<th>Errors</th>
	</tr>
</xsl:template>


<!-- class information -->
<xsl:template match="testsuite" mode="print.test">
	<tr valign="top">
		<!-- set a nice color depending if there is an error/failure -->
		<xsl:attribute name="class">
			<xsl:choose>
				<xsl:when test="@failures[.&gt; 0]">Failure</xsl:when>
				<xsl:when test="@errors[.&gt; 0]">Error</xsl:when>
			</xsl:choose>
		</xsl:attribute>
		<!-- print testsuite information -->
		<td><a href="#{@name}"><xsl:value-of select="@name"/></a></td>
		<td><xsl:value-of select="@tests"/></td>
		<td><xsl:value-of select="@errors"/></td>
		<td><xsl:value-of select="@failures"/></td>
		<td>
			<xsl:call-template name="display-time">
				<xsl:with-param name="value" select="@time"/>
			</xsl:call-template>
		</td>
	</tr>
</xsl:template>

<xsl:template match="testcase" mode="print.test">
	
	<tr valign="top">
		<xsl:attribute name="class">
			<xsl:choose>
				<xsl:when test="SYSTEM_TOMBSTONE | system_app_crash | system_app_anr | data_app_crash | data_app_anr | system_server_crash | system_server_watchdog | SYSTEM_RESTART | system_server_lowmem | freeze | memory_dump | out_of_memory">Error</xsl:when>
			</xsl:choose>
		</xsl:attribute>
		<td width="8%"><a href="{@resultUrl}"><xsl:value-of select="@no"/></a></td>
		<td width="42%">
			<a href="{@location}"><xsl:value-of select="@location"/></a>
		</td>
		<td width="7%">
			<xsl:value-of select="@startTime"/>
		</td>
		<td width="7%">
			<xsl:call-template name="display-time">
				<xsl:with-param name="value" select="@time"/>
			</xsl:call-template>
			s
		</td>
		<td width="6%">
			<xsl:value-of select="@status"/>
		</td>
		<td width="6%">
			<a href="{@testcaseLogUrl}">nst</a>
		</td>
		<td width="30%">
		<a href="{@logUrl}">
		<xsl:choose>
			<xsl:when test="SYSTEM_TOMBSTONE">
				SYSTEM_TOMBSTONE,
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="system_app_crash">
				system_app_crash,
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="system_app_anr">
				system_app_anr,
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="data_app_crash">
				data_app_crash,
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="data_app_anr">
				data_app_anr,
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="system_server_crash">
				system_server_crash,
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="system_server_watchdog">
				system_server_watchdog,
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="SYSTEM_RESTART">
				SYSTEM_RESTART,
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="system_server_lowmem">
				system_server_lowmem,
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="freeze">
				freeze,
			</xsl:when>
		</xsl:choose>
        </a>
            <xsl:if test="@adbLogUrl">
                <a href="{@adbLogUrl}">
                    ADBLog,
                </a>
            </xsl:if>
            <xsl:if test="@dmesgLogUrl">
                <a href="{@dmesgLogUrl}">
                    DMSG,
                </a>
            </xsl:if>
            <xsl:if test="@memdumpLogUrl">
                <a href="{@memdumpLogUrl}">
                    MemDump,
                </a>
            </xsl:if>
            <xsl:if test="@outofmemLogUrl">
                <a href="{@outofmemLogUrl}">
                    OOM,
                </a>
            </xsl:if>
        </td>
	</tr>
</xsl:template>


<xsl:template match="failure">
	<xsl:call-template name="display-failures"/>
</xsl:template>

<xsl:template match="error">
	
</xsl:template>

<!-- Style for the error and failure in the tescase template -->
<xsl:template name="display-failures">
	<xsl:choose>
		<xsl:when test="not(@message)">N/A</xsl:when>
		<xsl:otherwise>
			<xsl:value-of select="@message"/>
		</xsl:otherwise>
	</xsl:choose>
	<!-- display the stacktrace -->
	<code>
		<p/>
		<xsl:call-template name="br-replace">
			<xsl:with-param name="word" select="."/>
		</xsl:call-template>
	</code>
	<!-- the later is better but might be problematic for non-21" monitors... -->
	<!--pre><xsl:value-of select="."/></pre-->
</xsl:template>

<xsl:template name="JS-escape">
	<xsl:param name="string"/>
	<xsl:choose><!-- something isn't right here, basically all single quotes need to be replaced with backslash-single-quote
		<xsl:when test="contains($string,'&apos;')">
			<xsl:value-of select="substring-before($string,'&apos;')"/>
			\&apos;
			<xsl:call-template name="JS-escape">
				<xsl:with-param name="string" select="substring-after($string,'&apos;')"/>
			</xsl:call-template>
		</xsl:when> -->
		<xsl:when test="contains($string,'\')">
			<xsl:value-of select="substring-before($string,'\')"/>\\<xsl:call-template name="JS-escape">
				<xsl:with-param name="string" select="substring-after($string,'\')"/>
			</xsl:call-template>
		</xsl:when>
		<xsl:otherwise>
			<xsl:value-of select="$string"/>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


<!--
	template that will convert a carriage return into a br tag
	@param word the text from which to convert CR to BR tag
-->
<xsl:template name="br-replace">
	<xsl:param name="word"/>
	<xsl:choose>
		<xsl:when test="contains($word,'&#xA;')">
			<xsl:value-of select="substring-before($word,'&#xA;')"/>
			<br/>
			<xsl:call-template name="br-replace">
				<xsl:with-param name="word" select="substring-after($word,'&#xA;')"/>
			</xsl:call-template>
		</xsl:when>
		<xsl:otherwise>
			<xsl:value-of select="$word"/>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="display-time">
	<xsl:param name="value"/>
	<xsl:value-of select="format-number($value,'0.000')"/>
</xsl:template>

<xsl:template name="display-percent">
	<xsl:param name="value"/>
	<xsl:value-of select="format-number($value,'0.00%')"/>
</xsl:template>

</xsl:stylesheet>

use Tours_DB;

--import to xml

create Procedure IMPORT_COUNTRIES_TO_XML @path NVARCHAR(MAX)
AS
Begin
select * from COUNTRY for xml raw('COUNTRY'), root('COUNTRIES');

DECLARE @cmd1 VARCHAR(4000)='bcp "use Tours_DB; select * from COUNTRY for xml raw(''COUNTRY''), root(''COUNTRIES'');" queryout "'+ @path +'" -T -c -S'

EXECUTE master..xp_cmdshell @cmd1;
End


--EXEC IMPORT_COUNTRIES_TO_XML @path = 'D:/countries.xml';
--drop Procedure IMPORT_COUNTRIES_TO_XML;

--export from xml 

DECLARE @xml XML;

SELECT @xml = CONVERT(xml, BulkColumn, 2) FROM OPENROWSET(BULK 'D:/countries.xml', SINGLE_BLOB) AS x

INSERT INTO  COUNTRY(COUNTRY_NAME, COUNTRY_LANGUAGE, COUNTRY_CURRENCY)
SELECT 
	t.x.value('@COUNTRY_NAME', 'nvarchar(50)') AS COUNTRY_NAME,
	t.x.value('@COUNTRY_LANGUAGE', 'nvarchar(50)') AS COUNTRY_LANGUAGE,
	t.x.value('@COUNTRY_CURRENCY', 'nvarchar(50)') AS COUNTRY_CURRENCY
FROM @xml.nodes('//COUNTRIES/COUNTRY') t(x)


--if not work
-------------------------------------------------------------------------------------
----EXEC sp_configure 'show advanced options', 1
----GO
------ To update the currently configured value for advanced options.
----RECONFIGURE
----GO
------ To enable the feature.
----EXEC sp_configure 'xp_cmdshell', 1
----GO
------ To update the currently configured value for this feature.
----RECONFIGURE
----GO
--------------------------------------------------------------------------------------
USE [mdn_silver]
GO

/****** Object:  StoredProcedure [wd_hcm].[usp_update_licenses]    Script Date: 2/24/2026 5:53:15 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




/*******************************************************************************************************************
 Created_Date	: 2024-08-14
 Created_By		: Sharon Armstrong
 Decription		: ETL Script to Load wd_hcm.usp_update_licenses  table in the Silver Layer from
                wd_hcm.int_105 in the Bronze Layer
 Logging      : SELECT * FROM mdn_ops..SystemAppLog WHERE BatchNumber = (SELECT MAX(BatchNumber) FROM mdn_ops..SystemAppLog) ORDER BY SystemAppLogID

  Logging        : 
 
                  SELECT * FROM [mdn_ops].[dbo].[fn_get_last_system_app_log]('int105_BRNZ_TO_SLVR') ORDER BY system_app_log_id

                                
                  SELECT COUNT(1)
				    FROM mdn_bronze.wd_hcm.int_105


                  SELECT *
				    FROM mdn_silver.wd_hcm.int_105
 

			      TRUNCATE TABLE mdn_silver.wd_hcm.int_105


				  SELECT *
				    FROM mdn_bronze.wd_hcm.int_105
				   WHERE system_app_file_log_id = 207


				  UPDATE [mdn_ops].[dbo].[system_app_file_log]
				     SET [load_start_date] = NULL,
					     [load_end_date] = NULL,
                         [load_elapsed] = NULL,
                         [load_count] = NULL,
                         [status_message] = 'Imported'
				   WHERE [system_app_file_log_id] = 207



				  SELECT * FROM [mdn_ops].[dbo].[system_app_file_log] WHERE [system_app_file_log_id] = 207

				  SELECT [mdn_ops].[dbo].[fn_get_system_app_id]('int105_FILE_TO_BRONZE')

*******************************************************************************************************************/
CREATE     PROCEDURE [wd_hcm].[usp_update_licenses] 
@system_app_file_log_id BIGINT
AS

BEGIN
	SET NOCOUNT ON;

    DECLARE
		@ProcessName                VARCHAR(120) = 'INT105 from Bronze to Silver',   
	    @ProcessDate                DATETIME = GETDATE(),
		@target_file                CHAR(6) = 'INT105',
		@bronze_to_silver_mnemonic      VARCHAR(60) = 'INT105_BRNZ_TO_SLVR',
		@file_to_bronze_mnemonic        VARCHAR(60) = 'INT105_FILE_TO_BRONZE',
		@error                          INT = 0,
		@area                           VARCHAR(255),
		@message                        VARCHAR(2000),
		@elapsed                        VARCHAR(20),
		@count                          INT = 0,
		@crlf                           CHAR(2) = CHAR(13) + CHAR(10),
		@tab                            CHAR(1) = CHAR(9),
		@start_datetime                 DATETIME,
		@end_datetime                   DATETIME,
		@bronze_to_silver_batch_number  BIGINT,
		@current_user                   SYSNAME = SUSER_SNAME(),
		@insert_count                   INT,
		@update_count                   INT,
		@previous_count                 INT,
		@load_start_date                DATETIME,
		@load_end_date                  DATETIME,
		@load_count						INT,
		@load_status         VARCHAR(8) = 'Success';

	DROP TABLE IF EXISTS #temp_source
	DROP TABLE IF EXISTS #temp_target

	SET @load_start_date = @ProcessDate

-- Begin Logging
    EXEC @bronze_to_silver_batch_number = mdn_ops.dbo.usp_system_app_log_start @bronze_to_silver_mnemonic,NULL;


	SET @message = 'System App File Log ID = ' + CONVERT(VARCHAR(20),@system_app_file_log_id);
  	EXEC mdn_ops.dbo.usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;


	BEGIN TRY

		/*******************************************************************************************************************/
		/* There are files to process                                                                                      */
		/*******************************************************************************************************************/

		BEGIN TRANSACTION;
			SET @area = 'Retrieve Process Information';

			SET @start_datetime = GETDATE();
			SET @message = @area + ' Starting...';
			EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;



        -- How many rows were inserted into Bronze?
        SET @previous_count = (SELECT COUNT(*) FROM mdn_bronze.wd_hcm.int_105 WHERE system_app_file_log_id = @system_app_file_log_id);
		
		SET @message = '# of Rows that were loaded into bronze = ' + CONVERT(VARCHAR(20),ISNULL(@previous_count,0));
  	    EXEC mdn_ops.dbo.usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;

		--PRINT '@system_app_file_log_id ' +  CAST (@system_app_file_log_id AS VARCHAR);

-- Get the newly inserted records from the previous layer
-- Always include the IDENTITY SK column and the key column(s)
SELECT
	id                                  AS source_sk,
	mdn_ops.dbo.fn_trim([c00_employee_id])					AS employee_id,
	mdn_ops.dbo.fn_trim([c01_worker_name])					AS worker_name,
	mdn_ops.dbo.fn_trim([c02_location_id])					AS location_id,
	mdn_ops.dbo.fn_trim([c03_company_id])					AS company_id,
	mdn_ops.dbo.fn_trim([c04_job_id])						AS job_id,
	try_convert(datetime,LEFT([c05_hire_date], CHARINDEX('-', [c05_hire_date], 9) - 1)	)					AS hire_date,
	try_convert(datetime,LEFT([c06_term_date], CHARINDEX('-', [c06_term_date], 9) - 1)	)					AS term_date,
	mdn_ops.dbo.fn_trim([c07_license_id_type])				AS license_id_type,
	mdn_ops.dbo.fn_trim([c08_license_class])					AS license_class,
	mdn_ops.dbo.fn_trim([c9_issued_by_country])				AS issued_by_country,
	mdn_ops.dbo.fn_trim([c10_issued_by_country_region])		AS issued_by_country_region,
	mdn_ops.dbo.fn_trim([c11_issued_by_authority])			AS issued_by_authority,
	mdn_ops.dbo.fn_trim([c12_license_number])				AS license_number,
	try_convert(datetime,LEFT([c13_issued_date], CHARINDEX('-', [c13_issued_date], 9) - 1)	)				AS issued_date,
	try_convert(datetime,LEFT([c14_expiration_date], CHARINDEX('-', [c14_expiration_date], 9) - 1)	)			AS expiration_date,
	try_convert(datetime,LEFT([c15_verification_date], CHARINDEX('-', [c15_verification_date], 9) - 1) )				AS verification_date,
	mdn_ops.dbo.fn_trim([c16_verified_by])					AS verified_by,
	CAST(HASHBYTES('MD5',
            CONCAT(
					   [c01_worker_name]
					  ,[c02_location_id]
					  ,[c03_company_id]
					  ,[c04_job_id]
					  ,[c05_hire_date]
					  ,[c06_term_date]
					  ,[c08_license_class]
					  ,[c9_issued_by_country]
					  ,[c10_issued_by_country_region]
					  ,[c11_issued_by_authority]
					  ,[c14_expiration_date]
					  ,[c15_verification_date]
					  ,[c16_verified_by]
				   )
             ) AS BINARY(16))                           AS source_hash,
		CAST(HASHBYTES('MD5',
            CONCAT(
					[c00_employee_id],
					[c07_license_id_type],
					[c12_license_number],
					[c13_issued_date]
				   )
             ) AS BINARY(16))                           AS source_key_hash
INTO
	#temp_source
FROM
	mdn_bronze.wd_hcm.int_105
WHERE
	system_app_file_log_id = @system_app_file_log_id;

--Index should include the sk column, the key column(s), and the hash column.
CREATE NONCLUSTERED INDEX IX_#temp_source_source_sk_source_key_hash_source_hash
	ON #temp_source(source_sk,source_key_hash,source_hash);

-- Now get the SK column, the key column(s), and the hash columns into a temp table
SELECT	
	[licenses_sk]					AS target_sk,
	dw_md5_hash                     AS target_hash,
	CAST(HASHBYTES('MD5',
            CONCAT(
					[employee_id],
					[license_id_type],
					[license_number],
					[issued_date]
				   )
             ) AS BINARY(16))                           AS target_key_hash
INTO
	#temp_target
FROM
	mdn_silver.[wd_hcm].[licenses];

--Index should include the SK column, the key column(s), and the hash column.
CREATE NONCLUSTERED INDEX IX_#temp_target_target_sk_target_key_hash_target_hash
	ON #temp_target(target_sk,target_key_hash,target_hash);

--Put an index on all key columns as well as the SK column from bronze.
-- Insert any new (key columns that do not exist in target) rows from source.
SET @area = 'Insertion of New Records';

SET @start_datetime = GETDATE();
SET @message = @area + ' Starting...';
EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;


INSERT INTO mdn_silver.[wd_hcm].[licenses]
(
	employee_id,
	worker_name,
	location_id,
	company_id,
	job_id,
	hire_date,
	term_date,
	license_id_type,
	license_class,
	issued_by_country,
	issued_by_country_region,
	issued_by_authority,
	license_number,
	issued_date,
	expiration_date,
	verification_date,
	verified_by,
	system_app_file_log_id,
	batch_number,
	dw_md5_hash
)
SELECT
	temp_source.employee_id,
	temp_source.worker_name,
	temp_source.location_id,
	temp_source.company_id,
	temp_source.job_id,
	temp_source.hire_date as hire_date,
	temp_source.term_date as term_date,
	temp_source.license_id_type,
	temp_source.license_class,
	temp_source.issued_by_country,
	temp_source.issued_by_country_region,
	temp_source.issued_by_authority,
	temp_source.license_number,
	temp_source.issued_date as issued_date,
	temp_source.expiration_date as expiration_date,
	temp_source.verification_date as verification_date,
	temp_source.verified_by ,         
	@system_app_file_log_id                         AS system_app_file_log_id,
	@bronze_to_silver_batch_number                      AS batch_number, -- These rows are tied to the previous batch_number so from file to gold, all processes share the same batch_number.
	temp_source.source_hash                     AS dw_md5_hash								
FROM 
	#temp_source temp_source
INNER JOIN mdn_bronze.wd_hcm.int_105 AS brnz_source
    ON temp_source.source_sk = brnz_source.id
LEFT JOIN #temp_target AS temp_target
    ON temp_source.source_key_hash = temp_target.target_key_hash
LEFT JOIN mdn_silver.[wd_hcm].[licenses] AS slvr_target
    ON temp_target.target_sk = slvr_target.licenses_sk
WHERE
    slvr_target.licenses_sk IS NULL; 


	SET @count = @@ROWCOUNT;
    SET @insert_count = @count;
	SET @end_datetime = GETDATE();
    SET @elapsed = mdn_ops.dbo.fn_elapsed(@start_datetime,@end_datetime);

	SET @message = @area + ' Completed... Count = ' + CONVERT(VARCHAR(20),@count) + '. Elapsed Time = ' + @elapsed
	EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;

		/*******************************************************************************************************************/
		/* Update of Existing Records                                                                                      */
		/*******************************************************************************************************************/
    -- Update records where the key columns already exist
	SET @area = 'Update of Existing Records';

	SET @start_datetime = GETDATE();
	SET @message = @area + ' Starting...';
	 EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;

UPDATE mdn_silver.[wd_hcm].[licenses]
SET
	worker_name					= temp_source.worker_name,
	location_id					= temp_source.location_id,
	company_id					= temp_source.company_id,
	job_id						= temp_source.job_id,
	hire_date					= temp_source.hire_date,
	term_date					= temp_source.term_date,
	license_class				= temp_source.license_class,
	issued_by_country			= temp_source.issued_by_country,
	issued_by_country_region	= temp_source.issued_by_country_region,
	issued_by_authority			= temp_source.issued_by_authority,
	expiration_date				= temp_source.verification_date,
	verification_date			= temp_source.verification_date,
	verified_by					= temp_source.verified_by, 
	dw_updated_at				= @ProcessDate,
	dw_updated_by				= @current_user,
	dw_md5_hash					= temp_source.source_hash, -- Just in case the hash is not available in the bronze.
	batch_number				= @bronze_to_silver_batch_number
FROM
	mdn_bronze.wd_hcm.int_105 AS brnz_source
	
	INNER JOIN #temp_source AS temp_source
	ON temp_source.source_sk = brnz_source.id
	
	INNER JOIN #temp_target AS temp_target -- Inner Join should be okay here since we already know that these joins will always succeed.
	ON temp_source.source_key_hash = temp_target.target_key_hash
	AND temp_source.source_hash <> temp_target.target_hash
	
	INNER JOIN mdn_silver.[wd_hcm].[licenses] AS slvr_target
    ON temp_target.target_sk = slvr_target.licenses_sk
WHERE
    1 = 1


        SET @count = @@ROWCOUNT;
        SET @update_count = @count;
	    SET @end_datetime = GETDATE();
        SET @elapsed = mdn_ops.dbo.fn_elapsed(@start_datetime,@end_datetime);

		SET @message = @area + ' Completed. Count = ' + CONVERT(VARCHAR(20),@count) + '. Elapsed Time = ' + @elapsed
	    EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;


		SET @load_count = @insert_count + @update_count
		
		SET @load_end_date = GETDATE()


	EXEC mdn_ops.dbo.usp_update_system_app_file_log_load @system_app_file_log_id, 'mdn_silver', 
                @load_start_date, @load_end_date, @load_count, @load_status

        COMMIT TRANSACTION;
      END TRY  

      BEGIN CATCH 
        ROLLBACK TRANSACTION;

	      SET @error = ERROR_NUMBER();
		  SET @load_status = 'Error';
		  SET @message = mdn_ops.dbo.fn_FormatErrorMessage(ERROR_NUMBER(),ERROR_SEVERITY(),ERROR_STATE(),
                                                         ERROR_PROCEDURE(),ERROR_LINE(),ERROR_MESSAGE());

	      SET @message = N'Error occurred during ' + @Area + '. ' + N' System Message = ' + @message
	      EXEC mdn_ops.dbo.usp_system_app_log @bronze_to_silver_mnemonic,NULL,@Message,@bronze_to_silver_batch_number,'E'

	      GOTO PROCESSEND          
      END CATCH

PROCESSEND:	
/*******************************************************************************************************************/
/* Almost done...cleanup                                                                                           */
/*******************************************************************************************************************/

	EXEC mdn_ops.dbo.usp_update_system_app_file_log_load @system_app_file_log_id, 'mdn_silver', 
				@load_start_date, @load_end_date, @load_count, @load_status

      /* And...we're DONE! */
	EXEC mdn_ops.dbo.usp_system_app_log_end @bronze_to_silver_mnemonic,@ProcessName,@bronze_to_silver_batch_number

/*******************************************************************************************************************/
/* If there errors bubble them up                                                                                  */
/*******************************************************************************************************************/

      IF @error <> 0
	      RAISERROR (@message, 15, 1);

	/***** Needed for Mercury *****/
	  SELECT @bronze_to_silver_batch_number AS batch_number

  END;

GO



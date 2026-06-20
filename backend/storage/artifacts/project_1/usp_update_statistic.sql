USE [mdn_silver]
GO

/****** Object:  StoredProcedure [wd_fin].[usp_update_statistic]    Script Date: 4/7/2026 3:05:15 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




/*
USE [mdn_silver]
GO

IF OBJECT_ID('wd_fin.usp_update_statistic') IS NOT NULL
  BEGIN
    PRINT 'Proc Exists so dropping it...';
	  DROP PROCEDURE wd_fin.usp_update_statistic;
  END
ELSE
  PRINT 'Proc did not exist so nothing to drop...';
GO
*/


CREATE PROCEDURE [wd_fin].[usp_update_statistic] 
@system_app_file_log_id BIGINT
AS
/*******************************************************************************************************************
 Created_Date	: 2025-01-27	
 Created_By		: ?
 Decription		: Update mdn_silver Statistic data
--------------------------------------------------------------------------------------------------------------------
 Example        : EXEC [wd_fin].[usp_update_statistic] 2029


                  SELECT * FROM [mdn_ops].[dbo].[fn_get_last_system_app_log]('RAAS_STATISTIC_BRNZ_TO_SLVR') ORDER BY system_app_log_id


				  SELECT * FROM [mdn_ops_dev].[dbo].[system_app_file_log] WHERE [system_app_file_log_id] = 1998

				  
				  SELECT * FROM [mdn_ops_dev].[dbo].system_app WHERE mnemonic = 'RAAS_STATISTIC_BRNZ_TO_SLVR'
                                
                  SELECT *
				    FROM mdn_bronze.wd_fin.RAAS_payor
				   WHERE [system_app_file_log_id] = 1998


                  SELECT *
				    FROM mdn_silver.wd_fin.statistic
 

			      TRUNCATE TABLE mdn_silver.wd_fin.statistic


				  SELECT *
				    FROM mdn_silver.wd_fin.payor
				   WHERE system_app_file_log_id = 221


				  UPDATE [mdn_ops].[dbo].[system_app_file_log]
				     SET [load_start_date] = NULL,
					     [load_end_date] = NULL,
                         [load_elapsed] = NULL,
                         [load_count] = NULL,
                         [status_message] = 'Imported'
				   WHERE [system_app_file_log_id] = 1998


--------------------------------------------------------------------------------------------------------------------
 Modified_Date	Modified_By		Decription
 2025-01-27		?				Initial
********************************************************************************************************************/
BEGIN

    SET NOCOUNT ON;

    DECLARE
      @ProcessName                    VARCHAR(120),   
	  @ProcessDate                    DATETIME = GETDATE(),
      @target_file                    VARCHAR(14) = 'RAAS_statistic',
      @bronze_to_silver_mnemonic       VARCHAR(60) = 'RAAS_STATISTIC_BRNZ_TO_SLVR',
	  --@file_to_bronze_mnemonic        VARCHAR(60),
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
	  --@file_to_bronze_batch_number    BIGINT,
	  --@executed_status                VARCHAR(1000),
	  --@file_status_message            VARCHAR(2000),
	  --@system_app_file_log_id         BIGINT,
	  --@successful_execution_status    VARCHAR(7) = 'Success',
	  --@successful_import_status       VARCHAR(8) = 'Imported',
	  @current_user                   SYSNAME = SUSER_SNAME(),
	  @insert_count                   INT,
	  @update_count                   INT,
	  @previous_count                 INT,
	  @load_start_date                DATETIME,
	  @load_end_date                  DATETIME,
	  @load_count					  INT,
	  --@successful_load_status         VARCHAR(8) = 'Success';
	  @load_status                    VARCHAR(8) = 'Success';


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

		SET @area = 'Retrieve Process Information';

	    SET @start_datetime = GETDATE();
	    SET @message = @area + ' Starting...';
	    EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;

        -- How many rows were inserted into Bronze?
        SET @previous_count = (SELECT COUNT(*) FROM mdn_bronze.wd_fin.raas_job_family WHERE system_app_file_log_id = @system_app_file_log_id);

        SET @message = '# of Rows that were loaded into bronze = ' + CONVERT(VARCHAR(20),ISNULL(@previous_count,0));
  	    EXEC mdn_ops.dbo.usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;


        -- Get the newly inserted records from the previous layer
	    SELECT
               id                                             AS source_sk,
               CAST(mdn_ops.dbo.fn_trim(c01_account_set) AS VARCHAR)		          AS source_key_1,
		       CAST(mdn_ops.dbo.fn_trim(c02_ledger_account) AS VARCHAR)		      AS source_key_2,
		       CAST(mdn_ops.dbo.fn_trim(c04_identifier) AS INT)					  AS statistic_id,
		       CAST(mdn_ops.dbo.fn_trim(c01_account_set) AS VARCHAR)				  AS statistic_account_set,
		       CAST(mdn_ops.dbo.fn_trim(c02_ledger_account) AS VARCHAR)			  AS statistic_ledger_account,
		       CASE 
		           WHEN LOWER(mdn_ops.dbo.fn_trim(c03_retired)) = '1' THEN 1 
		           ELSE 0 
		       END AS is_retired,
		       mdn_ops.dbo.fn_trim(c05_account_name)					 AS statistic_account_name,
		       mdn_ops.dbo.fn_trim(c06_ledger_account_type)			 AS statistic_ledger_account_type,
		       mdn_ops.dbo.fn_trim(c07_level_1)						 AS statistic_level_1,
		       mdn_ops.dbo.fn_trim(c08_level_2)						 AS statistic_level_2,
		       mdn_ops.dbo.fn_trim(c09_level_3)						 AS statistic_level_3,
		       mdn_ops.dbo.fn_trim(c10_level_4)						 AS statistic_level_4,
		       mdn_ops.dbo.fn_trim(c11_level_5)						 AS statistic_level_5,
		       mdn_ops.dbo.fn_trim(c12_level_6)						 AS statistic_level_6,
		       mdn_ops.dbo.fn_trim(c13_stats_level_1)					 AS statistic_stats_level_1,
		       mdn_ops.dbo.fn_trim(c14_stats_level_2)					 AS statistic_stats_level_2,
		       mdn_ops.dbo.fn_trim(c15_stats_level_3)					 AS statistic_stats_level_3,
		       mdn_ops.dbo.fn_trim(c16_stats_level_4)					 AS statistic_stats_level_4,
		       mdn_ops.dbo.fn_trim(c17_stats_level_5)					 AS statistic_stats_level_5,
		       mdn_ops.dbo.fn_trim(c18_stats_level_6)					 AS statistic_stats_level_6,
               CONVERT(BINARY(16), HASHBYTES('MD5', 
				        CONCAT(
				              c05_account_name, 
				              c06_ledger_account_type,
				              c07_level_1, 
				              c08_level_2, 
				              c09_level_3, 
				              c10_level_4,
				              c11_level_5, 
				              c12_level_6,
				              c13_stats_level_1,
				              c14_stats_level_2,
				              c15_stats_level_3,
				              c16_stats_level_4,
				              c17_stats_level_5,
				              c18_stats_level_6
				        ))) AS  source_hash
          INTO #temp_source
          FROM mdn_bronze.wd_fin.raas_statistic WITH(NOLOCK)
         WHERE system_app_file_log_id = @system_app_file_log_id;


		SET @count = @@ROWCOUNT;


        CREATE NONCLUSTERED INDEX IX_#temp_source_source_sk_source_key_1_source_hash
          ON #temp_source(source_sk,source_key_1,source_key_2,source_hash);


        SELECT statistic_sk		                              AS target_sk,
               statistic_account_set					          AS target_key_1,
		       statistic_ledger_account					      AS target_key_2,
               dw_md5_hash                                     AS target_hash
          INTO #temp_target
          FROM mdn_silver.wd_fin.statistic;

        CREATE NONCLUSTERED INDEX IX_#temp_target_target_sk_target_key_1_target_hash
          ON #temp_target(target_sk,target_key_1,target_key_2,target_hash);


		SET @end_datetime = GETDATE();
        SET @elapsed = mdn_ops.dbo.fn_elapsed(@start_datetime,@end_datetime);

	    SET @message = @area + ' Completed. Count = ' + CONVERT(VARCHAR(20),@count) + '. Elapsed Time = ' + @elapsed
		EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;


		/*******************************************************************************************************************/
		/* Insertion of new records                                                                                        */
		/*******************************************************************************************************************/

         -- Insert any new (key columns that do not exist in target) rows from source.
        SET @area = 'Insertion of New Records';

	    SET @start_datetime = GETDATE();
	    SET @message = @area + ' Starting...';
	    EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;


        INSERT INTO mdn_silver.wd_fin.statistic
        (
               statistic_id					
			  ,statistic_account_set			
			  ,statistic_ledger_account		
			  ,is_retired			
			  ,statistic_account_name			
			  ,statistic_ledger_account_type	
			  ,statistic_level_1				
			  ,statistic_level_2				
			  ,statistic_level_3				
			  ,statistic_level_4				
			  ,statistic_level_5				
			  ,statistic_level_6				
			  ,statistic_stats_level_1			
			  ,statistic_stats_level_2			
			  ,statistic_stats_level_3			
			  ,statistic_stats_level_4			
			  ,statistic_stats_level_5			
			  ,statistic_stats_level_6			
			  ,system_app_file_log_id
              ,batch_number
              ,dw_md5_hash
        )
        SELECT
               temp_source.statistic_id					
		      ,temp_source.statistic_account_set			
		      ,temp_source.statistic_ledger_account		
		      ,temp_source.is_retired			
		      ,temp_source.statistic_account_name			
		      ,temp_source.statistic_ledger_account_type	
		      ,temp_source.statistic_level_1				
		      ,temp_source.statistic_level_2				
		      ,temp_source.statistic_level_3				
		      ,temp_source.statistic_level_4				
		      ,temp_source.statistic_level_5				
		      ,temp_source.statistic_level_6				
		      ,temp_source.statistic_stats_level_1			
		      ,temp_source.statistic_stats_level_2			
		      ,temp_source.statistic_stats_level_3			
		      ,temp_source.statistic_stats_level_4			
		      ,temp_source.statistic_stats_level_5			
		      ,temp_source.statistic_stats_level_6			
              ,@system_app_file_log_id               AS system_app_file_log_id
              ,brnz_source.batch_number          AS batch_number -- These rows are tied to the previous batch_number so from file to gold, all processes share the same batch_number.
              ,temp_source.source_hash               AS dw_md5_hash
          FROM #temp_source                             AS temp_source
         INNER JOIN mdn_bronze.wd_fin.raas_statistic         AS brnz_source
            ON temp_source.source_sk = brnz_source.id
          LEFT JOIN #temp_target                                    AS temp_target
            ON temp_source.source_key_1 = temp_target.target_key_1
		   AND temp_source.source_key_2 = temp_target.target_key_2
          LEFT JOIN mdn_silver.wd_fin.statistic                     AS slvr_target
            ON temp_target.target_sk = slvr_target.statistic_sk
         WHERE slvr_target.statistic_sk IS NULL;    -- INSERT WHERE THE OUTER JOIN failed meaning the target key column was not found.

        
		SET @count = @@ROWCOUNT;
        SET @insert_count = @count;
	    SET @end_datetime = GETDATE();
        SET @elapsed = mdn_ops.dbo.fn_elapsed(@start_datetime,@end_datetime);

	    SET @message = @area + ' Completed. Count = ' + CONVERT(VARCHAR(20),@count) + '. Elapsed Time = ' + @elapsed
	    EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;


        /*******************************************************************************************************************/
		/* Update of Existing Records                                                                                      */
		/*******************************************************************************************************************/

        -- Update records where the key columns already exist
        SET @area = 'Update of Existing Records';

	    SET @start_datetime = GETDATE();
	    SET @message = @area + ' Starting...';
	    EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;


        UPDATE slvr_target
           SET
               slvr_target.statistic_account_set			= temp_source.statistic_account_set,
		       slvr_target.statistic_ledger_account		    = temp_source.statistic_ledger_account,
		       slvr_target.is_retired					    = temp_source.is_retired,
		       slvr_target.statistic_account_name		    = temp_source.statistic_account_name,
		       slvr_target.statistic_ledger_account_type	= temp_source.statistic_ledger_account_type,
		       slvr_target.statistic_level_1				= temp_source.statistic_level_1,
		       slvr_target.statistic_level_2				= temp_source.statistic_level_2,
		       slvr_target.statistic_level_3				= temp_source.statistic_level_3,
		       slvr_target.statistic_level_4				= temp_source.statistic_level_4,
		       slvr_target.statistic_level_5				= temp_source.statistic_level_5,
		       slvr_target.statistic_level_6				= temp_source.statistic_level_6,
		       slvr_target.statistic_stats_level_1		    = temp_source.statistic_stats_level_1,
		       slvr_target.statistic_stats_level_2		    = temp_source.statistic_stats_level_2,
		       slvr_target.statistic_stats_level_3		    = temp_source.statistic_stats_level_3,
		       slvr_target.statistic_stats_level_4		    = temp_source.statistic_stats_level_4,
		       slvr_target.statistic_stats_level_5		    = temp_source.statistic_stats_level_5,
		       slvr_target.statistic_stats_level_6		    = temp_source.statistic_stats_level_6,
               dw_updated_at								= @ProcessDate,
               dw_updated_by								= @current_user,
               dw_md5_hash								    = temp_source.source_hash, -- Just in case the hash is not available in the bronze.
               batch_number								    = brnz_source.batch_number, -- Typing the updated records to the previous batch_number from the bronze load.
               system_app_file_log_id					    = @system_app_file_log_id
          FROM mdn_bronze.wd_fin.raas_statistic       AS brnz_source
         INNER JOIN #temp_source                                  AS temp_source
            ON temp_source.source_sk = brnz_source.id
         INNER JOIN #temp_target                                  AS temp_target
            ON temp_source.source_key_1 = temp_target.target_key_1 
		   AND temp_source.source_key_2 = temp_target.target_key_2 
		   AND temp_source.source_hash <> temp_target.target_hash
         INNER JOIN mdn_silver.wd_fin.statistic                   AS slvr_target
            ON temp_target.target_sk = slvr_target.statistic_sk
      

        SET @count = @@ROWCOUNT;
        SET @update_count = @count;
	    SET @end_datetime = GETDATE();
        SET @elapsed = mdn_ops.dbo.fn_elapsed(@start_datetime,@end_datetime);


	    SET @message = @area + ' Completed. Count = ' + CONVERT(VARCHAR(20),@count) + '. Elapsed Time = ' + @elapsed
	    EXEC mdn_ops..usp_system_app_log @bronze_to_silver_mnemonic,NULL,@message,@bronze_to_silver_batch_number;

		
		SET @load_count = @insert_count + @update_count
		SET @load_end_date = GETDATE()
        
      END TRY  

      BEGIN CATCH 
        

	    SET @error = ERROR_NUMBER();
		SET @load_status = 'Error'
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



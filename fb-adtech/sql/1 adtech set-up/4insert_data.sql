--insert data into firebolt tables

--reset
    --TRUNCATE TABLE ltv;
    --TRUNCATE TABLE account;
    --TRUNCATE TABLE owned_apps;

--ltv
    INSERT INTO ltv (
        ltv_hour_tz
        ,app_id
        ,campaign
        ,ltv_country
        ,currency
        ,ltv_currency
        ,ad
        ,ad_id
        ,adset_name
        ,adset_id
        ,campaign_id
        ,unmasked_media_source
        ,media_source
        ,partner
        ,site_id
        ,channel
        ,event_name
        ,ltv_device_rank
        ,dashboard_device_rank
        ,attribution_type
        ,ltv_timezone
        ,keywords
        ,is_attributed
        ,attributed_touch_type
        ,source
        ,clicks_count
        ,impressions_count
        ,inappevents_count
        ,organic_inappevents_count
        ,installs_count
        ,organic_installs_count
        ,launches_count
        ,organic_launches_count
        ,uninstalls_count
        ,click_installs_count
        ,impression_installs_count
        ,revenue
        ,organic_revenue
        ,revenue_alt
        ,organic_revenue_alt
        ,first_inapps
        ,loyals
        ,install_cost
        ,install_cost_alt
        ,install_assists
        ,organic_first_inapps
        ,organic_loyals
        ,ltv_timestamp
        ,SOURCE_FILE_NAME
        ,SOURCE_FILE_TIMESTAMP
        ,ltv_timestamp_dt
    )
    SELECT
        ltv_hour_tz
        ,app_id
        ,campaign
        ,ltv_country
        ,currency
        ,ltv_currency
        ,ad
        ,ad_id
        ,adset_name
        ,adset_id
        ,campaign_id
        ,unmasked_media_source
        ,media_source
        ,partner
        ,site_id
        ,channel
        ,event_name
        ,ltv_device_rank
        ,dashboard_device_rank
        ,attribution_type
        ,ltv_timezone
        ,keywords
        ,is_attributed
        ,attributed_touch_type
        ,source
        ,clicks_count
        ,impressions_count
        ,inappevents_count
        ,organic_inappevents_count
        ,installs_count
        ,organic_installs_count
        ,launches_count
        ,organic_launches_count
        ,uninstalls_count
        ,click_installs_count
        ,impression_installs_count
        ,revenue
        ,organic_revenue
        ,revenue_alt
        ,organic_revenue_alt
        ,first_inapps
        ,loyals
        ,install_cost
        ,install_cost_alt
        ,install_assists
        ,organic_first_inapps
        ,organic_loyals
        ,ltv_timestamp
        ,$SOURCE_FILE_NAME
        ,$SOURCE_FILE_TIMESTAMP
        ,CAST(DATE_ADD('year', 6, TO_TIMESTAMP(ltv_timestamp / 1000.0)) AS DATE) AS ltv_timestamp_dt --make dates 2025
    FROM ltv_external
    ;

--acount
    INSERT INTO account 
    SELECT 
        * 
        ,$SOURCE_FILE_NAME
        ,$SOURCE_FILE_TIMESTAMP 
    FROM account_external
    ;

--owned_apps
    INSERT INTO owned_apps 
    SELECT 
        * 
        ,$SOURCE_FILE_NAME
        ,$SOURCE_FILE_TIMESTAMP 
    FROM owned_apps_external
    ;

show tables;
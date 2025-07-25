--create firebolt tables

--reset
    --DROP TABLE ltv;
    --DROP TABLE account;
    --DROP TABLE owned_apps;

--ltv
    CREATE TABLE IF NOT EXISTS ltv (
        ltv_hour_tz Text,
        app_id Text,
        campaign Text,
        ltv_country Text,
        currency Text,
        ltv_currency Text,
        ad Text,
        ad_id Text,
        adset_name Text,
        adset_id Text,
        campaign_id Text,
        unmasked_media_source Text,
        media_source Text,
        partner Text,
        site_id Text,
        channel Text,
        event_name Text,
        ltv_device_rank Text,
        dashboard_device_rank Text,
        attribution_type Text,
        ltv_timezone Text,
        keywords Text,
        is_attributed Text,
        attributed_touch_type Text,
        source Text,
        clicks_count Long,
        impressions_count Long,
        inappevents_count Long,
        organic_inappevents_count Long,
        installs_count Long,
        organic_installs_count Long,
        launches_count Long,
        organic_launches_count Long,
        uninstalls_count Long,
        click_installs_count Long,
        impression_installs_count Long,
        revenue Double,
        organic_revenue Double,
        revenue_alt Double,
        organic_revenue_alt Double,
        first_inapps Long,
        loyals Long,
        install_cost Double,
        install_cost_alt Double,
        install_assists Long,
        organic_first_inapps Long,
        organic_loyals Long,
        ltv_timestamp Long,
        SOURCE_FILE_NAME Text,
        SOURCE_FILE_TIMESTAMP Timestamp,
        ltv_timestamp_dt Date
    )
    PRIMARY INDEX ltv_timestamp_dt, media_source, app_id
    ;

--account
    CREATE TABLE IF NOT EXISTS account (
        account_email_id  Text,
        name Text,
        x18_digit_id Text,
        shipping_country Text,
        customer_tier_new  Text,
        billing_country_code  Text,
        account_manager_zd  Text,
        sales_manager_zd  Text,
        billing_city  Text,
        region  Text,
        id  Text,
        hq_status  Text,
        churned_lost_status  Text,
        account_id  Text,
        account_status  Text,
        account_sub_status  Text,
        website  Text,
        customer_engagement_manger  Text,
        secondary_csm_zd  Text,
        type_of_account  Text,
        longtail_account_checkbox Int,
        hidden_active_package_name  Text,
        master_account  Text,
        SOURCE_FILE_NAME Text,
        SOURCE_FILE_TIMESTAMP Timestamp
    )
    PRIMARY INDEX id
    ;

--owned_apps
    CREATE TABLE IF NOT EXISTS owned_apps (
        id Text,
        owner_account Text,
        name Text,
        platform Text,
        app_slug  Text,
        test_app Int,
        SOURCE_FILE_NAME Text,
        SOURCE_FILE_TIMESTAMP Timestamp
    )
    PRIMARY INDEX id, app_slug
    ;
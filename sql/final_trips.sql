CREATE OR REPLACE TABLE `cdmxmobility.cyclistic2024.final_trips` AS

SELECT
    ride_id,
    rideable_type,
    started_at,
    ended_at,
    member_casual,

    TIMESTAMP_DIFF(ended_at, started_at, MINUTE) AS ride_length,

    FORMAT_TIMESTAMP('%A', started_at) AS day_of_week,

    EXTRACT(HOUR FROM started_at) AS ride_hour,

    start_station_name,
    end_station_name

FROM `cdmxmobility.cyclistic2024.your_raw_table`

WHERE started_at IS NOT NULL
  AND ended_at IS NOT NULL
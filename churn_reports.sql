-- avg rating of churned and unchurned users
SELECT
    is_churned,
    AVG(feedback_rating) AS "Average Rating"
FROM
    customers
    JOIN feedbacks ON feedbacks.customer_id = customers.customer_id
GROUP BY
    is_churned;

-- avg age of churned and unchurned users
SELECT
    is_churned,
    AVG(age) AS "average age"
FROM
    customers
GROUP BY
    is_churned;

-- churn rate
SELECT
    ROUND(SUM(is_churned) / COUNT(*) * 100, 2) AS "churn rate"
FROM
    customers;

-- churn per service type
SELECT
    service_type,
    SUM(
        CASE
            WHEN is_churned = 1 THEN 1
            ELSE 0
        END
    ) AS churned_users,
    SUM(
        CASE
            WHEN is_churned = 0 THEN 1
            ELSE 0
        END
    ) AS unchurned_users,
    COUNT(service_type) AS total_users,
    (
        SUM(
            CASE
                WHEN is_churned = 1 THEN 1
                ELSE 0
            END
        ) * 100 / COUNT(service_type)
    ) AS churn_rate
FROM
    services
    JOIN customers ON services.customer_id = customers.customer_id
GROUP BY
    service_type;

-- avg usage of churned and non-churned user
SELECT
    is_churned,
    AVG(usage_month) AS monthly_usage,
    AVG(usage_minutes)
FROM
    customers
    JOIN usages ON usages.customer_id = customers.customer_id
GROUP BY
    is_churned;

-- churn per complaint type
SELECT
    complaint_type,
    SUM(
        CASE
            WHEN is_churned = 1 THEN 1
            ELSE 0
        END
    ) AS churned_users,
    SUM(
        CASE
            WHEN is_churned = 0 THEN 1
            ELSE 0
        END
    ) AS unchurned_users,
    COUNT(complaint_type) AS total_complaints,
    (
        SUM(
            CASE
                WHEN is_churned = 1 THEN 1
                ELSE 0
            END
        ) * 100 / COUNT(complaint_type)
    ) AS churn_rate
FROM
    complaints
    JOIN customers ON complaints.customer_id = customers.customer_id
GROUP BY
    complaint_type;
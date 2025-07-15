CREATE TABLE
    IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        age INT NOT NULL,
        signup_date DATE,
        is_churned BOOLEAN DEFAULT FALSE
    );

CREATE TABLE
    IF NOT EXISTS services (
        service_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        service_type ENUM ('Internet', 'Mobile', 'TV', 'Cloud', 'Banking') NOT NULL,
        start_date DATE,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );

CREATE TABLE
    IF NOT EXISTS complaints (
        complaint_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        complaint_type ENUM ('Billing', 'Network', 'Support', 'Service', 'App') NOT NULL,
        complaint_date DATE,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );

CREATE TABLE
    IF NOT EXISTS feedbacks (
        feedback_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        feedback_rating ENUM ('1', '2', '3', '4', '5') NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );

CREATE TABLE
    IF NOT EXISTS `usages` (
        usage_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        usage_month INT,
        usage_minutes INT,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );


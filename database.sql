CREATE DATABASE apartment_management;

USE apartment_management;

CREATE TABLE tenants (
    tenant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    move_in_date DATE NOT NULL,
    apartment_id INT
);

CREATE TABLE apartments (
    apartment_id INT AUTO_INCREMENT PRIMARY KEY,
    unit_number VARCHAR(20) UNIQUE NOT NULL,
    bedrooms INT NOT NULL,
    bathrooms INT NOT NULL,
    square_feet INT NOT NULL,
    monthly_rent DECIMAL(10,2) NOT NULL,
    status ENUM('vacant', 'occupied', 'maintenance') DEFAULT 'vacant'
);

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL,
    apartment_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('cash', 'check', 'credit card', 'bank transfer') NOT NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
    FOREIGN KEY (apartment_id) REFERENCES apartments(apartment_id)
);

CREATE TABLE maintenance (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    apartment_id INT NOT NULL,
    tenant_id INT NOT NULL,
    description TEXT NOT NULL,
    request_date DATE NOT NULL,
    status ENUM('pending', 'in progress', 'completed') DEFAULT 'pending',
    completion_date DATE,
    FOREIGN KEY (apartment_id) REFERENCES apartments(apartment_id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);

CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    hire_date DATE NOT NULL
);
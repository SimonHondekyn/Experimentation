-- Create the 'dvwa' database
DROP DATABASE IF EXISTS dvwa;
CREATE DATABASE dvwa;

-- Drop the 'dvwa' user if it already exists
DROP USER IF EXISTS 'dvwa'@'%' ;

-- Create a new 'dvwa' user with a password
CREATE USER 'dvwa'@'%' IDENTIFIED BY 'p@ssw0rd';

-- Grant all privileges on the dvwa database to the dvwa user
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'%';

-- Flush privileges to ensure the changes take effect
FLUSH PRIVILEGES;

-- Use the 'dvwa' database
USE dvwa;

-- Create the 'users' table (this is the default table for DVWA)
CREATE TABLE users (
  user_id INT(6) AUTO_INCREMENT,
  first_name VARCHAR(15),
  last_name VARCHAR(15),
  user VARCHAR(15) NOT NULL UNIQUE,
  password VARCHAR(64) NOT NULL,
  avatar VARCHAR(70),
  last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  failed_login INT(3) DEFAULT 0,
  PRIMARY KEY (user_id)
);

-- Insert some initial users into the 'users' table
INSERT INTO users VALUES
  ('admin', 'admin', 'admin', MD5('password'), '/hackable/users/admin.jpg', NOW(), '0'),
  ('Gordon', 'Brown', 'gordonb', MD5('abc123'), '/hackable/users/gordonb.jpg', NOW(), '0'),
  ('Hack', 'Me', '1337', MD5('charley'), '/hackable/users/1337.jpg', NOW(), '0'),
  ('Pablo', 'Picasso', 'pablo', MD5('letmein'), '/hackable/users/pablo.jpg', NOW(), '0'),
  ('Bob', 'Smith', 'smithy', MD5('password'), '/hackable/users/smithy.jpg', NOW(), '0');

-- Create the 'guestbook' table
CREATE TABLE guestbook (
  comment_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  comment VARCHAR(300) NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (comment_id)
);

-- Insert some initial data into the 'guestbook' table
INSERT INTO guestbook VALUES
  ('This is a test comment.', 'test');
-- Add school_year column to myproject_setting table
-- Run this SQL command in your MySQL database

ALTER TABLE myproject_setting 
ADD COLUMN school_year VARCHAR(20) DEFAULT '25-1';

-- Update existing records to have default school year
UPDATE myproject_setting 
SET school_year = '25-1' 
WHERE school_year IS NULL;
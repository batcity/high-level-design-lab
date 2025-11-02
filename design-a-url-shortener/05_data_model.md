# Data model:

## 1. Entities:

- User
- Shortened URL
- URL

## 2. Relationships:

- Users create Shortened URLs that map to full URLs
- Users (even anonymous ones) access the shortened URL

## 3. ER Diagram
![ER Diagram](url-shortener-ER-diagram.png)

## 4. Attributes    

**users table:**

| Attribute | Type | Notes |
|-----------|-----------|-----------|
| user_id | BIGINT | Auto incrementing counter (primary key) |
| username | varchar(32) | User defined username |
| password | VARCHAR(255) | hashed password |
| email | VARCHAR(255) | Unique per acccount |


**urls table:**

| Attribute     | Type        | Notes                       |
| ------------- | ----------- | --------------------------- |
| url_id        | BIGINT      | Primary Key, auto-increment |
| url           | TEXT        | Original URL                |
| shortened_url | VARCHAR(10) | Unique, indexed             |
| user_id       | BIGINT      | Foreign key to users        |
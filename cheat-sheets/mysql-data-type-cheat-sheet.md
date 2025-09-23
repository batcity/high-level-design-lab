# 🗂 MySQL Data Type Cheat Sheet

## 1. Numeric Types
| Type | Storage | Use Case |
|------|---------|---------|
| **TINYINT** (1 byte) | -128 to 127 / 0 to 255 (unsigned) | Small flags (status codes, booleans) |
| **BOOLEAN** (alias for TINYINT(1)) | 1 byte | True/False values |
| **SMALLINT** (2 bytes) | -32,768 to 32,767 | Small integers (age, year offset) |
| **MEDIUMINT** (3 bytes) | -8,388,608 to 8,388,607 | Medium-range integers |
| **INT / INTEGER** (4 bytes) | -2,147,483,648 to 2,147,483,647 | General-purpose whole numbers (IDs, counts) |
| **BIGINT** (8 bytes) | ±9 quintillion | Large counters (financial amounts, high IDs) |
| **DECIMAL(M, D)** | Variable | Exact fixed-point, good for money & precision (e.g., `DECIMAL(10,2)`) |
| **FLOAT** (4 bytes) | Approximate | Small floating point numbers, not exact |
| **DOUBLE / REAL** (8 bytes) | Approximate | Scientific calculations, large ranges |

**Rule of Thumb:**  
- Use **INT** for IDs unless you expect billions → then **BIGINT**.  
- Use **DECIMAL** for money, not FLOAT/DOUBLE.  
- Use **TINYINT(1)** for booleans.  

---

## 2. String Types
| Type | Storage | Use Case |
|------|---------|---------|
| **CHAR(n)** | Fixed-length (0–255) | Small, fixed strings (e.g., country codes `CHAR(2)`) |
| **VARCHAR(n)** | Variable-length (0–65535) | General text where length varies (names, emails) |
| **TEXT** | Up to 65,535 | Large text (articles, descriptions) |
| **MEDIUMTEXT** | Up to 16M | Longer text (logs, big content) |
| **LONGTEXT** | Up to 4GB | Very large text (books, blobs of JSON) |
| **BLOB** | Binary data (up to 65,535) | Images, files, encrypted data |
| **MEDIUMBLOB** | Up to 16M | Larger binaries |
| **LONGBLOB** | Up to 4GB | Very large binaries |

**Rule of Thumb:**  
- Use **VARCHAR** for most text.  
- Use **CHAR** only when all values are the same length.  
- Use **TEXT/BLOB** only when really needed (they can’t be indexed efficiently).  

---

## 3. Date & Time Types
| Type | Storage | Use Case | Notes |
|------|---------|---------|------|
| **DATE** | 3 bytes | Calendar dates (`YYYY-MM-DD`) | Range: 1000-01-01 → 9999-12-31 |
| **DATETIME** | 8 bytes (pre-5.6.4), 8–13 bytes (5.6.4+) | Date + time (`YYYY-MM-DD HH:MM:SS`) | Not timezone-aware; supports fractional seconds since 5.6.4 |
| **TIMESTAMP** | 4 bytes (no fractions), 7–8 bytes (with fractional seconds, 5.6.4+) | Date + time with auto-update and timezone awareness | Range: 1970-01-01 UTC → 2038-01-19 UTC |
| **TIME** | 3 bytes (pre-5.6.4), 3–6 bytes (5.6.4+) | Time of day (`HH:MM:SS`) | Supports fractional seconds since 5.6.4 |
| **YEAR(4)** | 1 byte | Year only (`YYYY`) | Range: 1901 → 2155 |

**Rule of Thumb:**  
- **DATE** → birthdays, due dates.  
- **DATETIME** → events/logs, no timezone shifts.  
- **TIMESTAMP** → system events, auto-tracked, timezone aware.  
- **TIME** → durations or daily schedules.  
- **YEAR** → standalone year values.  

---

## 4. JSON & Special Types
| Type | Use Case |
|------|---------|
| **JSON** | Semi-structured data (validated JSON, supports functions) |
| **ENUM('a','b','c')** | Limited set of values (gender, status) |
| **SET('a','b','c')** | Multiple-choice list (rarely used) |

**Rule of Thumb:**  
- Use **ENUM** only if values will never change (e.g., `status ENUM('pending','done')`).  
- Use **JSON** for flexible schema but don’t overuse (harder to query).  

---

## ⚡ Quick Decision Guide
- **ID / Keys** → `INT` (or `BIGINT` if very large)  
- **Boolean/Flags** → `TINYINT(1)` (or `BOOLEAN`)  
- **Money** → `DECIMAL(10,2)`  
- **Variable text** → `VARCHAR(n)`  
- **Fixed short text** → `CHAR(n)`  
- **Logs / Articles** → `TEXT`  
- **Date only** → `DATE`  
- **Date + time (event)** → `DATETIME`  
- **Date + time (system)** → `TIMESTAMP`  
- **Unstructured data** → `JSON`

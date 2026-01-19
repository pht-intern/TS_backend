# Database Validation Guide

This guide explains how the database validation system fixes common MySQL errors.

## Problems Fixed

### 1. NULL sent to NOT NULL columns
**Problem:** `city VARCHAR(100) NOT NULL` but Python sends `city = None`

**Solution:** The `auto_sanitize_params()` function converts empty strings to `None`, but for NOT NULL columns, you should use `safe_str()` with a default value:

```python
from utils.helpers import safe_str

city = safe_str(data.get('city'), default='Unknown', max_length=250)
```

### 2. Empty string sent to INT/DECIMAL
**Problem:** Form sends `price = ""` but column is `price INT`

**Solution:** Automatically handled! Empty strings are converted to `None` (MySQL NULL). For NOT NULL numeric columns, use `safe_int()` or `safe_float()`:

```python
from utils.helpers import safe_int, safe_float

price = safe_float(data.get('price'), default=0.0)  # NOT NULL column
total_flats = safe_int(data.get('total_flats'), None)  # NULLable column
```

### 3. Invalid JSON sent to JSON columns
**Problem:** Sending `amenities = ""` or `amenities = []` to `amenities JSON` column

**Solution:** Automatically handled! Dict/list values are converted to JSON strings:

```python
# This works automatically:
amenities = data.get('amenities', [])  # List will be converted to JSON string
metadata = {"key": "value"}  # Dict will be converted to JSON string

# Or use the helper:
from utils.helpers import safe_json
metadata_json = safe_json(data.get('metadata'), default=None)
```

### 4. Column count mismatch
**Problem:** `INSERT INTO properties (a, b, c) VALUES (%s, %s)` - one column missing

**Solution:** Automatically validated! The `execute_insert()` and `execute_update()` functions validate column count before execution and raise a clear error if mismatch detected.

### 5. Data too long for VARCHAR columns
**Problem:** `title VARCHAR(100)` but frontend sends 300+ characters

**Solution:** Use `safe_str()` with `max_length` parameter:

```python
from utils.helpers import safe_str

title = safe_str(data.get('title'), max_length=100, allow_none=False)
```

### 6. Foreign key constraint failure
**Problem:** Inserting `location_id = 9999` but that ID doesn't exist

**Solution:** Use `validate_foreign_key()` before inserting:

```python
from utils.db_validator import validate_foreign_key

# Validate before insert
if property_id:
    validate_foreign_key('residential_properties', 'id', property_id)
    # Or for plot properties:
    validate_foreign_key('plot_properties', 'id', property_id)
```

## Usage Examples

### Basic INSERT with automatic sanitization

```python
from database import execute_insert

query = """
    INSERT INTO properties (city, price, amenities, description)
    VALUES (%s, %s, %s, %s)
"""

params = (
    data.get('city'),           # Will be sanitized if empty string
    data.get('price'),          # Empty string -> None
    data.get('amenities', []),  # List -> JSON string automatically
    data.get('description')     # None is fine for nullable columns
)

# Column count is automatically validated
property_id = execute_insert(query, params)
```

### Advanced INSERT with column specs

```python
from utils.db_validator import sanitize_params_for_insert

column_specs = {
    'city': {
        'type': 'VARCHAR(250)',
        'not_null': True,
        'max_length': 250,
        'default': 'Unknown'
    },
    'price': {
        'type': 'DECIMAL(12, 2)',
        'not_null': True,
        'default': 0.0
    },
    'amenities': {
        'type': 'JSON',
        'is_json': True,
        'default': None
    }
}

query, sanitized_params = sanitize_params_for_insert(query, params, column_specs)
property_id = execute_insert(query, sanitized_params)
```

## Helper Functions Reference

### `safe_str(value, default='', max_length=None, allow_none=False)`
Safely convert to string with truncation and default handling.

### `safe_int(value, default=0)`
Safely convert to integer, handling None and empty strings.

### `safe_float(value, default=0.0)`
Safely convert to float, handling None, empty strings, and currency formats.

### `safe_json(value, default=None)`
Convert Python objects to valid JSON strings for JSON columns.

### `validate_foreign_key(table, column, value, allow_none=True)`
Validate that a foreign key value exists in the referenced table.

### `validate_column_count(query, params)`
Validate that placeholder count matches parameter count.

## Error Messages

The validation system provides helpful error messages:

- **Column count mismatch:** Shows exact count difference and query preview
- **NOT NULL violation:** Suggests checking data sanitization
- **Invalid numeric value:** Suggests using None instead of empty strings
- **Data too long:** Suggests truncating before inserting
- **Foreign key violation:** Shows which table/column/value failed
- **Invalid JSON:** Suggests using json.dumps() for Python objects

## Best Practices

1. **Always use helper functions for NOT NULL columns:**
   ```python
   city = safe_str(data.get('city'), default='Unknown', max_length=250)
   price = safe_float(data.get('price'), default=0.0)
   ```

2. **Let the system handle nullable columns:**
   ```python
   description = data.get('description')  # None is fine, will be NULL in DB
   ```

3. **Use safe_json for JSON columns:**
   ```python
   amenities = safe_json(data.get('amenities'), default=None)
   ```

4. **Validate foreign keys when you know the relationship:**
   ```python
   if property_id:
       validate_foreign_key('residential_properties', 'id', property_id)
   ```

5. **Trust the automatic validation:**
   - Column count is always validated
   - Empty strings are automatically converted to None
   - Dict/list values are automatically converted to JSON strings

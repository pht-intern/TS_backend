"""
Database validation and sanitization utilities
Handles common MySQL data type issues before insertion/update
"""
import json
import re
from typing import Any, Optional, Tuple, List, Dict
from database import execute_query


def sanitize_for_not_null(value: Any, default: Any, column_type: str = "VARCHAR") -> Any:
    """
    Sanitize value for NOT NULL columns.
    Converts None to appropriate default based on column type.
    
    Args:
        value: The value to sanitize
        default: Default value to use if value is None
        column_type: MySQL column type (VARCHAR, INT, DECIMAL, etc.)
    
    Returns:
        Sanitized value
    """
    if value is None:
        return default
    
    # For string types, also handle empty strings if default is provided
    if column_type.upper() in ('VARCHAR', 'TEXT', 'CHAR'):
        if isinstance(value, str) and value.strip() == '':
            return default if default is not None else ''
    
    return value


def sanitize_for_numeric(value: Any, default: Any = None, allow_none: bool = True) -> Optional[Any]:
    """
    Sanitize value for INT/DECIMAL columns.
    Converts empty strings to None or default value.
    
    Args:
        value: The value to sanitize
        default: Default value to use if value is empty/invalid
        allow_none: Whether None is allowed (for nullable columns)
    
    Returns:
        Sanitized numeric value or None
    """
    if value is None:
        return None if allow_none else default
    
    if isinstance(value, str):
        value = value.strip()
        if value == '' or value.lower() in ('nan', 'none', 'null'):
            return None if allow_none else default
    
    # Try to convert to number
    try:
        # Check if it's a float (has decimal point)
        if '.' in str(value):
            result = float(value)
        else:
            result = int(float(value))  # Convert via float to handle "10.0" -> 10
        
        # Check for NaN or infinity
        if result != result:  # NaN check
            return None if allow_none else default
        if result == float('inf') or result == float('-inf'):
            return None if allow_none else default
        
        return result
    except (ValueError, TypeError):
        return None if allow_none else default


def sanitize_json(value: Any, default: Any = None) -> Optional[str]:
    """
    Sanitize value for JSON columns.
    Converts Python objects to valid JSON strings.
    
    Args:
        value: The value to sanitize (can be dict, list, str, None, empty string)
        default: Default JSON to use if value is invalid (defaults to None)
    
    Returns:
        Valid JSON string or None
    """
    if value is None:
        return default
    
    # If already a valid JSON string, validate it
    if isinstance(value, str):
        value = value.strip()
        if value == '':
            return default
        
        # Try to parse to validate it's valid JSON
        try:
            json.loads(value)
            return value  # Already valid JSON string
        except (json.JSONDecodeError, ValueError):
            # Not valid JSON, try to convert
            pass
    
    # Convert Python objects to JSON
    try:
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        elif isinstance(value, str):
            # Try to parse and re-stringify to ensure valid JSON
            parsed = json.loads(value)
            return json.dumps(parsed)
        else:
            # For other types, convert to JSON
            return json.dumps(value)
    except (TypeError, ValueError, json.JSONDecodeError):
        return default


def truncate_string(value: Any, max_length: int) -> Optional[str]:
    """
    Truncate string to fit VARCHAR column length.
    
    Args:
        value: The string value to truncate
        max_length: Maximum length allowed
    
    Returns:
        Truncated string or None if value is None
    """
    if value is None:
        return None
    
    if not isinstance(value, str):
        value = str(value)
    
    if len(value) > max_length:
        return value[:max_length]
    
    return value


def validate_column_count(query: str, params: Tuple) -> bool:
    """
    Validate that the number of placeholders matches the number of parameters.
    
    Args:
        query: SQL query string with %s placeholders
        params: Tuple of parameters
    
    Returns:
        True if count matches, False otherwise
    
    Raises:
        ValueError: If count doesn't match
    """
    placeholder_count = query.count('%s')
    params_count = len(params) if params else 0
    
    if placeholder_count != params_count:
        raise ValueError(
            f"SQL placeholder count ({placeholder_count}) does not match params count ({params_count}). "
            f"Query: {query[:200]}... Params: {params}"
        )
    
    return True


def validate_foreign_key(table: str, column: str, value: Any, allow_none: bool = True) -> bool:
    """
    Validate that a foreign key value exists in the referenced table.
    
    Args:
        table: Name of the referenced table
        column: Name of the primary key column (usually 'id')
        value: The foreign key value to validate
        allow_none: Whether None/null is allowed
    
    Returns:
        True if valid, False otherwise
    
    Raises:
        ValueError: If foreign key doesn't exist
    """
    if value is None:
        return allow_none
    
    try:
        # Convert to int if it's a numeric string
        if isinstance(value, str) and value.strip().isdigit():
            value = int(value.strip())
        
        # Query to check if the ID exists
        check_query = f"SELECT COUNT(*) as count FROM {table} WHERE {column} = %s"
        result = execute_query(check_query, (value,))
        
        if result and result[0].get('count', 0) > 0:
            return True
        else:
            raise ValueError(
                f"Foreign key constraint violation: {table}.{column} = {value} does not exist"
            )
    except Exception as e:
        # Re-raise ValueError, but wrap other exceptions
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Error validating foreign key {table}.{column} = {value}: {str(e)}")


def auto_sanitize_params(params: Tuple) -> Tuple:
    """
    Automatically sanitize parameters for common MySQL issues.
    This is a simpler version that handles the most common cases without column specs.
    
    Handles:
    1. NULL sent to NOT NULL columns - converts empty strings to None (will fail gracefully)
    2. Empty string sent to INT/DECIMAL - converts to None
    3. JSON column receiving invalid JSON - converts dict/list to JSON string
    4. Column count mismatch - validated separately before this function
    
    Args:
        params: Tuple of parameters
    
    Returns:
        Tuple of sanitized parameters
    """
    sanitized = []
    for param in params:
        # Handle None values - keep as None (MySQL will handle NULL)
        if param is None:
            sanitized.append(None)
        # Handle empty strings - convert to None (MySQL NULL)
        # This prevents "Incorrect integer value" errors when empty string sent to INT/DECIMAL
        elif isinstance(param, str) and param.strip() == '':
            sanitized.append(None)
        # Handle list/dict for JSON columns - convert to JSON string
        # This prevents "Invalid JSON" errors
        elif isinstance(param, (dict, list)):
            try:
                sanitized.append(json.dumps(param))
            except (TypeError, ValueError):
                sanitized.append(None)
        # Handle numeric strings that might be empty after stripping
        elif isinstance(param, str):
            stripped = param.strip()
            if stripped == '' or stripped.lower() in ('nan', 'none', 'null'):
                sanitized.append(None)
            else:
                sanitized.append(param)
        # Handle other types as-is
        else:
            sanitized.append(param)
    
    return tuple(sanitized)


def sanitize_params_for_insert(
    query: str,
    params: Tuple,
    column_specs: Optional[Dict[str, Dict[str, Any]]] = None
) -> Tuple[str, Tuple]:
    """
    Comprehensive sanitization of parameters for INSERT queries.
    
    Args:
        query: SQL INSERT query
        params: Tuple of parameters
        column_specs: Optional dict mapping column names to their specs:
            {
                'column_name': {
                    'type': 'VARCHAR(100)',  # MySQL type
                    'not_null': True,         # Whether column is NOT NULL
                    'max_length': 100,         # For VARCHAR columns
                    'default': 'default_value', # Default if None/empty
                    'is_json': False,          # Whether it's a JSON column
                    'is_foreign_key': None,    # Tuple of (table, column) if FK, or None
                    'allow_none': True          # Whether None is allowed
                }
            }
    
    Returns:
        Tuple of (sanitized_query, sanitized_params)
    
    Raises:
        ValueError: If validation fails
    """
    # First validate column count
    validate_column_count(query, params)
    
    # Extract column names from INSERT query
    # Format: INSERT INTO table (col1, col2, col3) VALUES (%s, %s, %s)
    column_match = re.search(r'INSERT INTO\s+\w+\s*\((.*?)\)\s*VALUES', query, re.IGNORECASE)
    if not column_match:
        # If we can't parse columns, just validate count and return
        return query, params
    
    column_names = [col.strip() for col in column_match.group(1).split(',')]
    
    # Sanitize each parameter based on column specs
    sanitized_params = []
    for i, (col_name, param_value) in enumerate(zip(column_names, params)):
        if column_specs and col_name in column_specs:
            spec = column_specs[col_name]
            col_type = spec.get('type', 'VARCHAR').upper()
            not_null = spec.get('not_null', False)
            max_length = spec.get('max_length')
            default = spec.get('default')
            is_json = spec.get('is_json', False)
            is_foreign_key = spec.get('is_foreign_key')
            allow_none = spec.get('allow_none', not not_null)
            
            # Handle JSON columns
            if is_json:
                param_value = sanitize_json(param_value, default)
            
            # Handle NOT NULL columns
            if not_null:
                if col_type.startswith('VARCHAR') or col_type.startswith('TEXT') or col_type.startswith('CHAR'):
                    param_value = sanitize_for_not_null(param_value, default or '', col_type)
                    # Truncate if max_length specified
                    if max_length:
                        param_value = truncate_string(param_value, max_length)
                elif col_type in ('INT', 'BIGINT', 'SMALLINT', 'TINYINT', 'MEDIUMINT'):
                    param_value = sanitize_for_numeric(param_value, default or 0, allow_none=False)
                elif col_type in ('DECIMAL', 'FLOAT', 'DOUBLE'):
                    param_value = sanitize_for_numeric(param_value, default or 0.0, allow_none=False)
            else:
                # Nullable columns
                if col_type.startswith('VARCHAR') or col_type.startswith('TEXT') or col_type.startswith('CHAR'):
                    if isinstance(param_value, str) and param_value.strip() == '':
                        param_value = None
                    # Truncate if max_length specified
                    if max_length and param_value:
                        param_value = truncate_string(param_value, max_length)
                elif col_type in ('INT', 'BIGINT', 'SMALLINT', 'TINYINT', 'MEDIUMINT', 'DECIMAL', 'FLOAT', 'DOUBLE'):
                    param_value = sanitize_for_numeric(param_value, None, allow_none=True)
            
            # Validate foreign keys
            if is_foreign_key and param_value is not None:
                fk_table, fk_column = is_foreign_key
                validate_foreign_key(fk_table, fk_column, param_value, allow_none=True)
        
        sanitized_params.append(param_value)
    
    return query, tuple(sanitized_params)


def sanitize_params_for_update(
    query: str,
    params: Tuple,
    column_specs: Optional[Dict[str, Dict[str, Any]]] = None
) -> Tuple[str, Tuple]:
    """
    Comprehensive sanitization of parameters for UPDATE queries.
    Similar to sanitize_params_for_insert but handles UPDATE syntax.
    """
    # Validate column count
    validate_column_count(query, params)
    
    # For UPDATE queries, we need to parse SET clause
    # Format: UPDATE table SET col1 = %s, col2 = %s WHERE id = %s
    set_match = re.search(r'SET\s+(.*?)\s+WHERE', query, re.IGNORECASE)
    if not set_match:
        # If we can't parse, just validate count and return
        return query, params
    
    set_clause = set_match.group(1)
    # Extract column names from SET clause
    column_names = []
    for part in set_clause.split(','):
        col_match = re.search(r'(\w+)\s*=', part, re.IGNORECASE)
        if col_match:
            column_names.append(col_match.group(1).strip())
    
    # Also count WHERE clause parameters
    where_params_count = query.count('%s') - len(column_names)
    
    # Sanitize SET clause parameters
    sanitized_params = []
    for i, col_name in enumerate(column_names):
        if i < len(params) - where_params_count:
            param_value = params[i]
            
            if column_specs and col_name in column_specs:
                spec = column_specs[col_name]
                col_type = spec.get('type', 'VARCHAR').upper()
                not_null = spec.get('not_null', False)
                max_length = spec.get('max_length')
                default = spec.get('default')
                is_json = spec.get('is_json', False)
                is_foreign_key = spec.get('is_foreign_key')
                allow_none = spec.get('allow_none', not not_null)
                
                # Handle JSON columns
                if is_json:
                    param_value = sanitize_json(param_value, default)
                
                # Handle NOT NULL columns
                if not_null:
                    if col_type.startswith('VARCHAR') or col_type.startswith('TEXT') or col_type.startswith('CHAR'):
                        param_value = sanitize_for_not_null(param_value, default or '', col_type)
                        if max_length:
                            param_value = truncate_string(param_value, max_length)
                    elif col_type in ('INT', 'BIGINT', 'SMALLINT', 'TINYINT', 'MEDIUMINT'):
                        param_value = sanitize_for_numeric(param_value, default or 0, allow_none=False)
                    elif col_type in ('DECIMAL', 'FLOAT', 'DOUBLE'):
                        param_value = sanitize_for_numeric(param_value, default or 0.0, allow_none=False)
                else:
                    if col_type.startswith('VARCHAR') or col_type.startswith('TEXT') or col_type.startswith('CHAR'):
                        if isinstance(param_value, str) and param_value.strip() == '':
                            param_value = None
                        if max_length and param_value:
                            param_value = truncate_string(param_value, max_length)
                    elif col_type in ('INT', 'BIGINT', 'SMALLINT', 'TINYINT', 'MEDIUMINT', 'DECIMAL', 'FLOAT', 'DOUBLE'):
                        param_value = sanitize_for_numeric(param_value, None, allow_none=True)
                
                # Validate foreign keys
                if is_foreign_key and param_value is not None:
                    fk_table, fk_column = is_foreign_key
                    validate_foreign_key(fk_table, fk_column, param_value, allow_none=True)
            
            sanitized_params.append(param_value)
    
    # Add WHERE clause parameters as-is
    sanitized_params.extend(params[-where_params_count:])
    
    return query, tuple(sanitized_params)

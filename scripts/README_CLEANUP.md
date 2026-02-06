# ID Collision Cleanup Script

## Overview

This script detects and fixes property ID collisions between `commercial_properties`, `residential_properties`, and `plot_properties` tables.

**Problem:** Each table has its own AUTO_INCREMENT ID, so ID 3 can exist in multiple tables, causing backend ambiguity.

**Solution:** Detect collisions and delete duplicates from incorrect tables.

## Usage

### Step 1: Detect Collisions

```bash
cd backend/scripts
python cleanup_id_collisions.py --detect-only
```

This will show all property IDs that exist in multiple tables without making any changes.

### Step 2: Inspect Specific Collision

For a specific property ID (e.g., ID 3):

```bash
python cleanup_id_collisions.py --detect-only --property-id 3
```

### Step 3: Dry Run (Preview Changes)

See what would be deleted without actually deleting:

```bash
# Keep commercial, delete from plot/residential
python cleanup_id_collisions.py --fix --dry-run --keep-table commercial

# Keep plot, delete from commercial/residential  
python cleanup_id_collisions.py --fix --dry-run --keep-table plot

# Keep residential, delete from commercial/plot
python cleanup_id_collisions.py --fix --dry-run --keep-table residential
```

### Step 4: Fix Collisions

**⚠️ WARNING: This will permanently delete data. Always run --dry-run first!**

```bash
# Example: Keep commercial table, delete from plot table
python cleanup_id_collisions.py --fix --keep-table commercial

# Fix specific property ID only
python cleanup_id_collisions.py --fix --keep-table commercial --property-id 3
```

## Examples

### Example 1: Property ID 3 exists in both commercial and plot

**Detection:**
```bash
python cleanup_id_collisions.py --detect-only --property-id 3
```

**Output:**
```
COLLISION DETECTED: Property ID 3
Type: commercial + plot

Commercial Table:
  Name: Office Space XYZ
  Type: office_space
  Created: 2024-01-15 10:30:00

Plot Table:
  Name: Plot ABC
  Created: 2024-01-20 14:20:00
```

**Decision:** If "Office Space XYZ" is correct (commercial), delete from plot:

```bash
# Preview first
python cleanup_id_collisions.py --fix --dry-run --keep-table commercial --property-id 3

# Then actually fix
python cleanup_id_collisions.py --fix --keep-table commercial --property-id 3
```

### Example 2: Fix all collisions (keep commercial)

```bash
# Preview all changes
python cleanup_id_collisions.py --fix --dry-run --keep-table commercial

# Apply changes
python cleanup_id_collisions.py --fix --keep-table commercial
```

## Important Notes

1. **Always run `--detect-only` first** to see what collisions exist
2. **Always run `--dry-run` before `--fix`** to preview changes
3. **Check related data** - The script shows images and features that will be deleted
4. **Backup your database** before running `--fix` without `--dry-run`
5. **Choose the correct table** - Decide which table is correct before deleting

## Related Data

The script automatically checks for:
- Images (`commercial_property_images`, `residential_property_images`, `plot_property_images`)
- Features (`property_features`)

**Warning:** Deleting a property will also delete its related images and features from that table.

## Verification

After fixing, verify the property only exists in one table:

```sql
SELECT 
    (SELECT COUNT(*) FROM commercial_properties WHERE id = 3) +
    (SELECT COUNT(*) FROM residential_properties WHERE id = 3) +
    (SELECT COUNT(*) FROM plot_properties WHERE id = 3) as total_count;
-- Should return 1
```

## Troubleshooting

### "Database engine not initialized"
- Check that `.env` file exists in project root
- Verify `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME` are set

### "No collisions found"
- Good! Your database is clean
- The backend will work correctly

### "Error deleting"
- Check database permissions
- Verify the property ID exists
- Check for foreign key constraints

## After Cleanup

Once collisions are fixed:
1. ✅ Backend will stop returning 500 errors
2. ✅ Properties will be editable again
3. ✅ Frontend will show correct data
4. ✅ No more undefined behavior

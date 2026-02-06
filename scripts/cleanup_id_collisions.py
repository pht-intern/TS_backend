#!/usr/bin/env python3
"""
ID Collision Cleanup Script

This script detects and optionally fixes property ID collisions between tables.
Property IDs should only exist in ONE table (commercial_properties, residential_properties, or plot_properties).

Usage:
    python cleanup_id_collisions.py --detect-only          # Just find collisions
    python cleanup_id_collisions.py --fix --dry-run        # Show what would be deleted
    python cleanup_id_collisions.py --fix --keep-table commercial  # Actually delete duplicates (USE WITH CAUTION)
"""

import sys
import os
import argparse
from typing import List, Dict, Tuple

# Add parent directory to path to import database module
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(backend_dir)

# Add both backend and project root to path
sys.path.insert(0, backend_dir)
sys.path.insert(0, project_root)

# Change to backend directory to ensure relative imports work
os.chdir(backend_dir)

# Import database functions
try:
    from database import execute_query, execute_update
except ImportError as e:
    print("ERROR: Could not import database module.")
    print(f"Error: {e}")
    print(f"Current path: {os.getcwd()}")
    print(f"Script dir: {script_dir}")
    print(f"Backend dir: {backend_dir}")
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path}")
    sys.exit(1)


def find_collisions() -> List[Dict]:
    """Find all property IDs that exist in multiple tables."""
    collisions = []
    
    # Check commercial + residential
    query = """
        SELECT 
            c.id as property_id,
            'commercial + residential' as collision_type,
            c.property_name as commercial_name,
            c.property_type as commercial_type,
            c.created_at as commercial_created,
            r.property_name as residential_name,
            r.type as residential_type,
            r.created_at as residential_created
        FROM commercial_properties c
        INNER JOIN residential_properties r ON c.id = r.id
        ORDER BY c.id
    """
    results = execute_query(query)
    for row in results:
        collisions.append({
            'id': row['property_id'],
            'type': row['collision_type'],
            'tables': ['commercial', 'residential'],
            'commercial': {
                'name': row['commercial_name'],
                'type': row['commercial_type'],
                'created': row['commercial_created']
            },
            'residential': {
                'name': row['residential_name'],
                'type': row['residential_type'],
                'created': row['residential_created']
            }
        })
    
    # Check commercial + plot
    query = """
        SELECT 
            c.id as property_id,
            'commercial + plot' as collision_type,
            c.property_name as commercial_name,
            c.property_type as commercial_type,
            c.created_at as commercial_created,
            p.project_name as plot_name,
            p.created_at as plot_created
        FROM commercial_properties c
        INNER JOIN plot_properties p ON c.id = p.id
        ORDER BY c.id
    """
    results = execute_query(query)
    for row in results:
        collisions.append({
            'id': row['property_id'],
            'type': row['collision_type'],
            'tables': ['commercial', 'plot'],
            'commercial': {
                'name': row['commercial_name'],
                'type': row['commercial_type'],
                'created': row['commercial_created']
            },
            'plot': {
                'name': row['plot_name'],
                'created': row['plot_created']
            }
        })
    
    # Check residential + plot
    query = """
        SELECT 
            r.id as property_id,
            'residential + plot' as collision_type,
            r.property_name as residential_name,
            r.type as residential_type,
            r.created_at as residential_created,
            p.project_name as plot_name,
            p.created_at as plot_created
        FROM residential_properties r
        INNER JOIN plot_properties p ON r.id = p.id
        ORDER BY r.id
    """
    results = execute_query(query)
    for row in results:
        collisions.append({
            'id': row['property_id'],
            'type': row['collision_type'],
            'tables': ['residential', 'plot'],
            'residential': {
                'name': row['residential_name'],
                'type': row['residential_type'],
                'created': row['residential_created']
            },
            'plot': {
                'name': row['plot_name'],
                'created': row['plot_created']
            }
        })
    
    # Check all three tables
    query = """
        SELECT 
            c.id as property_id,
            'commercial + residential + plot' as collision_type,
            c.property_name as commercial_name,
            c.property_type as commercial_type,
            r.property_name as residential_name,
            r.type as residential_type,
            p.project_name as plot_name
        FROM commercial_properties c
        INNER JOIN residential_properties r ON c.id = r.id
        INNER JOIN plot_properties p ON c.id = p.id
        ORDER BY c.id
    """
    results = execute_query(query)
    for row in results:
        collisions.append({
            'id': row['property_id'],
            'type': row['collision_type'],
            'tables': ['commercial', 'residential', 'plot'],
            'commercial': {
                'name': row['commercial_name'],
                'type': row['commercial_type']
            },
            'residential': {
                'name': row['residential_name'],
                'type': row['residential_type']
            },
            'plot': {
                'name': row['plot_name']
            }
        })
    
    return collisions


def check_related_data(property_id: int, table: str) -> Dict:
    """Check for related data (images, features) before deleting."""
    related = {
        'images': [],
        'features': []
    }
    
    # Check images
    if table == 'commercial':
        query = "SELECT * FROM commercial_property_images WHERE property_id = %s"
    elif table == 'residential':
        query = "SELECT * FROM residential_property_images WHERE property_id = %s"
    elif table == 'plot':
        query = "SELECT * FROM plot_property_images WHERE property_id = %s"
    else:
        return related
    
    images = execute_query(query, (property_id,))
    related['images'] = [dict(img) for img in images]
    
    # Check features
    query = "SELECT * FROM property_features WHERE property_category = %s AND property_id = %s"
    features = execute_query(query, (table, property_id))
    related['features'] = [dict(feat) for feat in features]
    
    return related


def delete_from_table(property_id: int, table: str, dry_run: bool = True) -> bool:
    """Delete property from specified table."""
    table_map = {
        'commercial': 'commercial_properties',
        'residential': 'residential_properties',
        'plot': 'plot_properties'
    }
    
    table_name = table_map.get(table)
    if not table_name:
        print(f"ERROR: Invalid table name: {table}")
        return False
    
    if dry_run:
        print(f"  [DRY RUN] Would delete: DELETE FROM {table_name} WHERE id = {property_id}")
        return True
    
    try:
        query = f"DELETE FROM {table_name} WHERE id = %s"
        execute_update(query, (property_id,))
        print(f"  ✓ Deleted property ID {property_id} from {table_name}")
        return True
    except Exception as e:
        print(f"  ✗ Error deleting from {table_name}: {e}")
        return False


def print_collision_details(collision: Dict):
    """Print detailed information about a collision."""
    print(f"\n{'='*80}")
    print(f"COLLISION DETECTED: Property ID {collision['id']}")
    print(f"Type: {collision['type']}")
    print(f"{'='*80}")
    
    if 'commercial' in collision:
        print(f"\nCommercial Table:")
        print(f"  Name: {collision['commercial'].get('name', 'N/A')}")
        print(f"  Type: {collision['commercial'].get('type', 'N/A')}")
        print(f"  Created: {collision['commercial'].get('created', 'N/A')}")
    
    if 'residential' in collision:
        print(f"\nResidential Table:")
        print(f"  Name: {collision['residential'].get('name', 'N/A')}")
        print(f"  Type: {collision['residential'].get('type', 'N/A')}")
        print(f"  Created: {collision['residential'].get('created', 'N/A')}")
    
    if 'plot' in collision:
        print(f"\nPlot Table:")
        print(f"  Name: {collision['plot'].get('name', 'N/A')}")
        print(f"  Created: {collision['plot'].get('created', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description='Detect and fix property ID collisions between tables'
    )
    parser.add_argument(
        '--detect-only',
        action='store_true',
        help='Only detect collisions, do not fix'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Attempt to fix collisions (requires --keep-table)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be deleted without actually deleting'
    )
    parser.add_argument(
        '--keep-table',
        choices=['commercial', 'residential', 'plot'],
        help='When fixing, keep property in this table (delete from others)'
    )
    parser.add_argument(
        '--property-id',
        type=int,
        help='Fix collision for specific property ID only'
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print("Property ID Collision Detection and Cleanup")
    print("="*80)
    
    # Find collisions
    print("\nScanning for collisions...")
    collisions = find_collisions()
    
    if not collisions:
        print("\n✓ No collisions found! All property IDs are unique across tables.")
        return 0
    
    print(f"\n⚠️  Found {len(collisions)} collision(s):")
    
    # Filter by property_id if specified
    if args.property_id:
        collisions = [c for c in collisions if c['id'] == args.property_id]
        if not collisions:
            print(f"\n✗ No collision found for property ID {args.property_id}")
            return 1
        print(f"\nFiltered to property ID {args.property_id}")
    
    # Print all collisions
    for collision in collisions:
        print_collision_details(collision)
        
        # Check related data
        print(f"\nRelated Data Check:")
        for table in collision['tables']:
            related = check_related_data(collision['id'], table)
            if related['images']:
                print(f"  {table.capitalize()} has {len(related['images'])} image(s)")
            if related['features']:
                print(f"  {table.capitalize()} has {len(related['features'])} feature(s)")
    
    # If detect-only, stop here
    if args.detect_only:
        print(f"\n{'='*80}")
        print("Detection complete. Use --fix to clean up collisions.")
        print("="*80)
        return 0
    
    # Fix collisions
    if args.fix:
        if not args.keep_table:
            print("\n✗ ERROR: --fix requires --keep-table to specify which table to keep")
            print("   Example: --fix --keep-table commercial")
            print("   This will delete the property from other tables, keeping only commercial")
            return 1
        
        print(f"\n{'='*80}")
        print(f"FIXING COLLISIONS (keeping {args.keep_table} table)")
        if args.dry_run:
            print("DRY RUN MODE - No changes will be made")
        print("="*80)
        
        for collision in collisions:
            print(f"\nFixing collision for Property ID {collision['id']}:")
            
            # Delete from all tables except the one to keep
            for table in collision['tables']:
                if table != args.keep_table:
                    # Check related data first
                    related = check_related_data(collision['id'], table)
                    if related['images'] or related['features']:
                        print(f"  ⚠️  WARNING: {table.capitalize()} table has related data:")
                        if related['images']:
                            print(f"     - {len(related['images'])} image(s) will be deleted")
                        if related['features']:
                            print(f"     - {len(related['features'])} feature(s) will be deleted")
                    
                    delete_from_table(collision['id'], table, dry_run=args.dry_run)
            
            # Verify cleanup
            if not args.dry_run:
                verify_query = """
                    SELECT 
                        (SELECT COUNT(*) FROM commercial_properties WHERE id = %s) +
                        (SELECT COUNT(*) FROM residential_properties WHERE id = %s) +
                        (SELECT COUNT(*) FROM plot_properties WHERE id = %s) as total_count
                """
                result = execute_query(verify_query, (collision['id'], collision['id'], collision['id']))
                total = result[0]['total_count'] if result else 0
                
                if total == 1:
                    print(f"  ✓ Verified: Property ID {collision['id']} now exists in exactly 1 table")
                else:
                    print(f"  ✗ ERROR: Property ID {collision['id']} still exists in {total} table(s)")
        
        print(f"\n{'='*80}")
        if args.dry_run:
            print("Dry run complete. Remove --dry-run to apply changes.")
        else:
            print("Cleanup complete!")
        print("="*80)
        return 0
    
    # If neither detect-only nor fix, show help
    print("\nUse --detect-only to just find collisions")
    print("Use --fix --keep-table <table> to fix collisions")
    print("Use --dry-run to preview changes before applying")
    return 0


if __name__ == '__main__':
    sys.exit(main())

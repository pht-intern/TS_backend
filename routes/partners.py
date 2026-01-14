"""
Partners routes
"""
from flask import request, jsonify
import traceback
from database import execute_query
from schemas import PartnerResponseSchema
from utils.helpers import normalize_image_url, abort_with_message


def register_partners_routes(app):
    """Register partners routes"""
    
    @app.route("/api/partners", methods=["GET"])
    def get_partners():
        """Get all partners"""
        try:
            is_active_str = request.args.get('is_active', '').lower()
            is_active = None
            if is_active_str == 'true':
                is_active = True
            elif is_active_str == 'false':
                is_active = False
            
            if is_active is not None:
                is_active_int = 1 if is_active else 0
                query = "SELECT * FROM partners WHERE is_active = %s ORDER BY display_order, name"
                partners = execute_query(query, (is_active_int,))
            else:
                query = "SELECT * FROM partners ORDER BY display_order, name"
                partners = execute_query(query)
            
            normalized_partners = []
            for p in partners:
                try:
                    partner_dict = dict(p)
                    # Ensure all required fields are present
                    if 'is_active' not in partner_dict:
                        partner_dict['is_active'] = True
                    elif isinstance(partner_dict['is_active'], int):
                        partner_dict['is_active'] = bool(partner_dict['is_active'])
                    if 'display_order' not in partner_dict:
                        partner_dict['display_order'] = 0
                    if 'description' not in partner_dict:
                        partner_dict['description'] = None
                    if 'created_at' not in partner_dict:
                        partner_dict['created_at'] = None
                    if 'updated_at' not in partner_dict:
                        partner_dict['updated_at'] = None
                    
                    if 'logo_url' in partner_dict and partner_dict['logo_url']:
                        partner_dict['logo_url'] = normalize_image_url(partner_dict['logo_url'])
                    
                    normalized_partners.append(PartnerResponseSchema(**partner_dict))
                except Exception as schema_error:
                    print(f"Error converting partner {p.get('id', 'unknown')}: {str(schema_error)}")
                    traceback.print_exc()
                    continue
            
            result = [p.dict() for p in normalized_partners]
            print(f"Successfully fetched {len(result)} partners (is_active filter: {is_active})")
            return jsonify(result)
        except Exception as e:
            error_msg = str(e)
            print(f"Error fetching partners: {error_msg}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching partners: {error_msg}")

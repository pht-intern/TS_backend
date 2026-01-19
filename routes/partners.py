"""
Partners routes
"""
from flask import request, jsonify
import traceback
from database import execute_query, execute_update
from schemas import PartnerResponseSchema, PartnerUpdateSchema
from utils.helpers import normalize_image_url, abort_with_message, require_admin_auth


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
    
    @app.route("/api/partners/<int:partner_id>", methods=["POST"])
    @require_admin_auth
    def update_partner(partner_id: int):
        """Update a partner"""
        try:
            existing = execute_query("SELECT id FROM partners WHERE id = %s", (partner_id,))
            if not existing:
                abort_with_message(404, "Partner not found")
            
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
            partner_data = PartnerUpdateSchema(**data)
            
            updates = []
            params = []
            
            if partner_data.name is not None:
                updates.append("name = %s")
                params.append(partner_data.name)
            if partner_data.logo_url is not None:
                updates.append("logo_url = %s")
                params.append(partner_data.logo_url)
            if partner_data.website_url is not None:
                updates.append("website_url = %s")
                params.append(partner_data.website_url)
            if partner_data.is_active is not None:
                updates.append("is_active = %s")
                params.append(1 if partner_data.is_active else 0)
            if partner_data.display_order is not None:
                updates.append("display_order = %s")
                params.append(partner_data.display_order)
            
            if updates:
                params.append(partner_id)
                update_query = f"UPDATE partners SET {', '.join(updates)} WHERE id = %s"
                execute_update(update_query, tuple(params))
            
            partners = execute_query("SELECT * FROM partners WHERE id = %s", (partner_id,))
            partner_dict = dict(partners[0])
            if 'logo_url' in partner_dict:
                partner_dict['logo_url'] = normalize_image_url(partner_dict['logo_url'])
            
            response = PartnerResponseSchema(**partner_dict)
            return jsonify(response.dict())
        except Exception as e:
            print(f"Error updating partner: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error updating partner: {str(e)}")
    
    @app.route("/api/partners/<int:partner_id>", methods=["DELETE"])
    @require_admin_auth
    def delete_partner(partner_id: int):
        """Delete a partner"""
        try:
            result = execute_update("DELETE FROM partners WHERE id = %s", (partner_id,))
            if result == 0:
                abort_with_message(404, "Partner not found")
            return jsonify({"message": "Partner deleted successfully"})
        except Exception as e:
            print(f"Error deleting partner: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error deleting partner: {str(e)}")

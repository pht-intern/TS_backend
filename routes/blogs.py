"""
Blogs routes
"""
from flask import request, jsonify
import json
import traceback
from database import execute_query, execute_update, execute_insert
from schemas import (
    BlogCreateSchema, BlogUpdateSchema, BlogResponseSchema,
    PaginationParams, PaginatedResponse, MessageResponse
)
from utils.helpers import (
    abort_with_message, get_pagination_params, calculate_pages, normalize_image_url, require_admin_auth
)


def register_blogs_routes(app):
    """Register blogs routes"""
    
    @app.route("/api/blogs", methods=["GET"])
    def get_blogs():
        """Get all blogs with filtering and pagination"""
        try:
            pagination = get_pagination_params()
            offset = (pagination.page - 1) * pagination.limit
            
            category = request.args.get('category')
            is_featured = request.args.get('is_featured', type=lambda x: x.lower() == 'true' if x else None)
            is_active = request.args.get('is_active', type=lambda x: x.lower() == 'true' if x else None)
            
            conditions = []
            params = []
            
            if is_active is not None:
                is_active_int = 1 if is_active else 0
                conditions.append("is_active = %s")
                params.append(is_active_int)
            
            if category:
                conditions.append("category = %s")
                params.append(category)
            
            if is_featured is not None:
                is_featured_int = 1 if is_featured else 0
                conditions.append("is_featured = %s")
                params.append(is_featured_int)
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            count_query = f"SELECT COUNT(*) as total FROM blogs WHERE {where_clause}"
            total_result = execute_query(count_query, tuple(params))
            total = total_result[0]['total'] if total_result else 0
            
            query = f"SELECT * FROM blogs WHERE {where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([pagination.limit, offset])
            
            blogs = execute_query(query, tuple(params))
            
            blog_list = []
            for blog in blogs:
                blog_dict = dict(blog)
                if blog_dict.get('tags'):
                    try:
                        if isinstance(blog_dict['tags'], str):
                            blog_dict['tags'] = json.loads(blog_dict['tags'])
                        elif not isinstance(blog_dict['tags'], list):
                            blog_dict['tags'] = []
                    except:
                        blog_dict['tags'] = []
                else:
                    blog_dict['tags'] = []
                if 'image_url' in blog_dict and blog_dict['image_url']:
                    blog_dict['image_url'] = normalize_image_url(blog_dict['image_url'])
                blog_list.append(blog_dict)
            
            response = PaginatedResponse(
                total=total,
                page=pagination.page,
                limit=pagination.limit,
                pages=calculate_pages(total, pagination.limit),
                items=blog_list
            )
            return jsonify(response.dict())
        except Exception as e:
            traceback.print_exc()
            abort_with_message(500, f"Failed to fetch blogs: {str(e)}")
    
    @app.route("/api/blogs/<int:blog_id>", methods=["GET"])
    def get_blog(blog_id: int):
        """Get a single blog by ID"""
        try:
            blog_query = "SELECT * FROM blogs WHERE id = %s"
            blogs = execute_query(blog_query, (blog_id,))
            
            if not blogs:
                abort_with_message(404, "Blog not found")
            
            blog_data = dict(blogs[0])
            
            if blog_data.get('tags'):
                try:
                    if isinstance(blog_data['tags'], str):
                        blog_data['tags'] = json.loads(blog_data['tags'])
                    elif not isinstance(blog_data['tags'], list):
                        blog_data['tags'] = []
                except:
                    blog_data['tags'] = []
            else:
                blog_data['tags'] = []
            
            if 'image_url' in blog_data and blog_data['image_url']:
                blog_data['image_url'] = normalize_image_url(blog_data['image_url'])
            
            response = BlogResponseSchema(**blog_data)
            return jsonify(response.dict())
        except Exception as e:
            print(f"Error fetching blog: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error fetching blog: {str(e)}")
    
    @app.route("/api/blogs/<int:blog_id>/increment-views", methods=["POST"])
    def increment_blog_views(blog_id: int):
        """Increment blog view count"""
        try:
            # Check if blog exists
            existing = execute_query("SELECT id, views FROM blogs WHERE id = %s", (blog_id,))
            if not existing:
                abort_with_message(404, "Blog not found")
            
            # Increment views
            execute_update("UPDATE blogs SET views = views + 1 WHERE id = %s", (blog_id,))
            
            # Return updated views count
            updated = execute_query("SELECT views FROM blogs WHERE id = %s", (blog_id,))
            return jsonify({"views": updated[0]['views'] if updated else 0})
        except Exception as e:
            print(f"Error incrementing blog views: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error incrementing blog views: {str(e)}")
    
    @app.route("/api/blogs", methods=["POST"])
    @require_admin_auth
    def create_blog():
        """Create a new blog"""
        try:
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
            blog_data = BlogCreateSchema(**data)
            
            tags_json = json.dumps(blog_data.tags) if blog_data.tags else None
            
            insert_query = """
                INSERT INTO blogs (
                    title, excerpt, content, category, tags, image_url, 
                    author, views, is_featured, is_active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            blog_id = execute_insert(insert_query, (
                blog_data.title,
                blog_data.excerpt,
                blog_data.content,
                blog_data.category,
                tags_json,
                blog_data.image_url,
                blog_data.author or 'Tirumakudalu Properties',
                blog_data.views or 0,
                1 if blog_data.is_featured else 0,
                1 if blog_data.is_active else 0
            ))
            
            # Return the created blog directly (no re-fetch needed)
            blog_data_dict = {
                'id': blog_id,
                'title': blog_data.title,
                'excerpt': blog_data.excerpt,
                'content': blog_data.content,
                'category': blog_data.category,
                'tags': blog_data.tags or [],
                'image_url': normalize_image_url(blog_data.image_url) if blog_data.image_url else None,
                'author': blog_data.author or 'Tirumakudalu Properties',
                'views': blog_data.views or 0,
                'is_featured': bool(blog_data.is_featured),
                'is_active': bool(blog_data.is_active),
                'created_at': None,  # Will be set by DB, but not needed for response
                'updated_at': None
            }
            
            response = BlogResponseSchema(**blog_data_dict)
            return jsonify(response.dict()), 201
        except Exception as e:
            print(f"Error creating blog: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error creating blog: {str(e)}")
    
    @app.route("/api/blogs/<int:blog_id>", methods=["POST"])
    @require_admin_auth
    def update_blog(blog_id: int):
        """Update a blog"""
        try:
            existing = execute_query("SELECT id FROM blogs WHERE id = %s", (blog_id,))
            if not existing:
                abort_with_message(404, "Blog not found")
            
            data = request.get_json()
            if not data:
                abort_with_message(400, "Invalid request data")
            
            blog_data = BlogUpdateSchema(**data)
            
            updates = []
            params = []
            
            if blog_data.title is not None:
                updates.append("title = %s")
                params.append(blog_data.title)
            if blog_data.excerpt is not None:
                updates.append("excerpt = %s")
                params.append(blog_data.excerpt)
            if blog_data.content is not None:
                updates.append("content = %s")
                params.append(blog_data.content)
            if blog_data.category is not None:
                updates.append("category = %s")
                params.append(blog_data.category)
            if blog_data.tags is not None:
                updates.append("tags = %s")
                tags_json = json.dumps(blog_data.tags)
                params.append(tags_json)
            if blog_data.image_url is not None:
                updates.append("image_url = %s")
                params.append(blog_data.image_url)
            if blog_data.author is not None:
                updates.append("author = %s")
                params.append(blog_data.author)
            if blog_data.views is not None:
                updates.append("views = %s")
                params.append(blog_data.views)
            if blog_data.is_featured is not None:
                updates.append("is_featured = %s")
                params.append(blog_data.is_featured)
            if blog_data.is_active is not None:
                updates.append("is_active = %s")
                params.append(blog_data.is_active)
            
            if not updates:
                blog_query = "SELECT * FROM blogs WHERE id = %s"
                blogs = execute_query(blog_query, (blog_id,))
                blog_data_dict = dict(blogs[0])
                if blog_data_dict.get('tags'):
                    try:
                        if isinstance(blog_data_dict['tags'], str):
                            blog_data_dict['tags'] = json.loads(blog_data_dict['tags'])
                    except:
                        blog_data_dict['tags'] = []
                response = BlogResponseSchema(**blog_data_dict)
                return jsonify(response.dict())
            
            params.append(blog_id)
            update_query = f"UPDATE blogs SET {', '.join(updates)} WHERE id = %s"
            execute_update(update_query, tuple(params))
            
            # Return updated blog
            blog_query = "SELECT * FROM blogs WHERE id = %s"
            blogs = execute_query(blog_query, (blog_id,))
            blog_data_dict = dict(blogs[0])
            if blog_data_dict.get('tags'):
                try:
                    if isinstance(blog_data_dict['tags'], str):
                        blog_data_dict['tags'] = json.loads(blog_data_dict['tags'])
                except:
                    blog_data_dict['tags'] = []
            if 'image_url' in blog_data_dict and blog_data_dict['image_url']:
                blog_data_dict['image_url'] = normalize_image_url(blog_data_dict['image_url'])
            
            response = BlogResponseSchema(**blog_data_dict)
            return jsonify(response.dict())
        except Exception as e:
            print(f"Error updating blog: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error updating blog: {str(e)}")
    
    @app.route("/api/blogs/<int:blog_id>", methods=["DELETE"])
    @require_admin_auth
    def delete_blog(blog_id: int):
        """Delete a blog"""
        try:
            existing = execute_query("SELECT id FROM blogs WHERE id = %s", (blog_id,))
            if not existing:
                abort_with_message(404, "Blog not found")
            
            delete_query = "DELETE FROM blogs WHERE id = %s"
            execute_update(delete_query, (blog_id,))
            
            response = MessageResponse(message="Blog deleted successfully")
            return jsonify(response.dict())
        except Exception as e:
            print(f"Error deleting blog: {str(e)}")
            traceback.print_exc()
            abort_with_message(500, f"Error deleting blog: {str(e)}")

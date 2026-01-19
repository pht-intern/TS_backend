"""
API Schemas for Tirumakudalu Properties
Pydantic schemas for API request/response validation
"""

from typing import Optional, List
from datetime import datetime
import json
from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_serializer, field_validator
from models import (
    PropertyType, PropertyStatus, InquiryStatus,
    Property, PropertyImage, PropertyFeature,
    PropertyProjectImage, PropertyFloorplanImage, PropertyMasterplanImage,
    Partner, Testimonial, ContactInquiry,
    Blog, User, UserRole,
    VisitorInfo, Log, LogType,
    SystemMetrics, TemporaryMetrics,
    CacheLog, CacheOperation, CacheStatus
)


# ============================================
# COMMON SCHEMAS
# ============================================

class MessageResponse(BaseModel):
    """Standard message response"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: Optional[str] = None
    success: bool = False


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(10, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    total: int
    page: int
    limit: int
    pages: int
    items: List[dict]


# ============================================
# PROPERTY SCHEMAS
# ============================================

class PropertyCreateSchema(BaseModel):
    """Schema for creating a property"""
    title: str = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    price: float = Field(..., gt=0)
    price_text: Optional[str] = Field(None, max_length=500, description="Original price text (e.g., '3BHK: Rs.3.32 Cr, 4BHK: Rs.3.72 Cr')")
    type: PropertyType
    bedrooms: int = Field(..., gt=0)
    bathrooms: float = Field(..., gt=0)
    area: int = Field(..., gt=0, description="Area in square feet")
    status: PropertyStatus
    description: Optional[str] = None
    is_featured: bool = False
    is_active: bool = True
    location_link: Optional[str] = Field(None, description="Google Maps location link")
    directions: Optional[str] = Field(None, description="Directions to the property")
    length: Optional[float] = Field(None, ge=0, description="Property length in feet (for residential properties)")
    breadth: Optional[float] = Field(None, ge=0, description="Property breadth in feet (for residential properties)")
    images: Optional[List[str]] = Field(default=[], description="List of image URLs")
    features: Optional[List[str]] = Field(default=[], description="List of feature names")


class PropertyUpdateSchema(BaseModel):
    """Schema for updating a property"""
    title: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    price_text: Optional[str] = Field(None, max_length=500, description="Original price text (e.g., '3BHK: Rs.3.32 Cr, 4BHK: Rs.3.72 Cr')")
    type: Optional[PropertyType] = None
    bedrooms: Optional[int] = Field(None, gt=0)
    bathrooms: Optional[float] = Field(None, gt=0)
    area: Optional[int] = Field(None, gt=0)
    status: Optional[PropertyStatus] = None
    description: Optional[str] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    location_link: Optional[str] = Field(None, description="Google Maps location link")
    directions: Optional[str] = Field(None, description="Directions to the property")
    length: Optional[float] = Field(None, ge=0, description="Property length in feet (for residential properties)")
    breadth: Optional[float] = Field(None, ge=0, description="Property breadth in feet (for residential properties)")
    images: Optional[List[str]] = None
    features: Optional[List[str]] = None


class PropertyImageSchema(BaseModel):
    """Property image schema for responses"""
    id: int
    image_url: str
    image_order: int
    is_primary: bool
    created_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class PropertyProjectImageSchema(BaseModel):
    """Property project image schema for responses"""
    id: int
    property_id: int
    image_url: str
    image_order: int
    created_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class PropertyFloorplanImageSchema(BaseModel):
    """Property floorplan image schema for responses"""
    id: int
    property_id: int
    image_url: str
    image_order: int
    created_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class PropertyMasterplanImageSchema(BaseModel):
    """Property masterplan image schema for responses"""
    id: int
    property_id: int
    image_url: str
    image_order: int
    created_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class PropertyFeatureSchema(BaseModel):
    """Property feature schema for responses"""
    id: int
    feature_name: str
    created_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class PropertyResponseSchema(BaseModel):
    """Property response schema with related data"""
    id: int
    title: str
    location: Optional[str] = None  # Constructed from city + locality if not present
    price: float
    price_text: Optional[str] = None
    type: PropertyType
    bedrooms: int
    bathrooms: Optional[float] = 0
    area: Optional[int] = None  # Can be buildup_area or plot_area
    status: PropertyStatus
    description: Optional[str]
    is_featured: bool
    is_active: bool
    location_link: Optional[str] = None
    directions: Optional[str] = None
    length: Optional[float] = None
    breadth: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    images: List[PropertyImageSchema] = Field(default_factory=list)
    project_images: List[PropertyProjectImageSchema] = Field(default_factory=list)
    floorplan_images: List[PropertyFloorplanImageSchema] = Field(default_factory=list)
    masterplan_images: List[PropertyMasterplanImageSchema] = Field(default_factory=list)
    features: List[PropertyFeatureSchema] = Field(default_factory=list)
    # Additional optional fields that may exist in database
    city: Optional[str] = None
    locality: Optional[str] = None
    property_name: Optional[str] = None
    project_name: Optional[str] = None
    unit_type: Optional[str] = None
    property_category: Optional[str] = None
    builder: Optional[str] = None
    configuration: Optional[str] = None
    plot_area: Optional[float] = None
    plot_length: Optional[float] = None
    plot_breadth: Optional[float] = None
    buildup_area: Optional[float] = None
    carpet_area: Optional[float] = None
    super_built_up_area: Optional[float] = None
    total_flats: Optional[int] = None
    total_floors: Optional[int] = None
    total_acres: Optional[float] = None
    property_status: Optional[str] = None  # Alternative status field (ready_to_move, under_construction, etc.)
    listing_type: Optional[str] = None  # new, resell
    video_link: Optional[str] = None  # Video preview link
    direction: Optional[str] = None  # Property facing direction (east, west, north, south)
    price_negotiable: Optional[bool] = None
    price_includes_registration: Optional[bool] = None

    @field_validator('is_featured', 'is_active', 'price_negotiable', 'price_includes_registration', mode='before')
    @classmethod
    def parse_bool(cls, v):
        """Convert MySQL TINYINT(1) (0/1) to bool"""
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return False if v is None else bool(v)

    @field_validator('status', mode='before')
    @classmethod
    def parse_status(cls, v):
        """Convert status string to PropertyStatus enum - handles legacy DB values"""
        if not v:
            return PropertyStatus.SALE
        if isinstance(v, PropertyStatus):
            return v
        if isinstance(v, str):
            # Normalize: handle spaces, dashes, underscores, case variations
            normalized = v.lower().replace(" ", "_").replace("-", "_").strip()
            # Try direct match first
            try:
                return PropertyStatus(normalized)
            except ValueError:
                # Try to find in enum members (case-insensitive)
                for member_name, member_value in PropertyStatus.__members__.items():
                    if member_name.lower() == normalized or member_value.value.lower() == normalized:
                        return member_value
                # Default fallback
                return PropertyStatus.SALE
        return PropertyStatus.SALE

    @field_validator('type', mode='before')
    @classmethod
    def parse_type(cls, v):
        """Convert type string to PropertyType enum - handles legacy DB values"""
        if not v:
            return PropertyType.HOUSE
        if isinstance(v, PropertyType):
            return v
        if isinstance(v, str):
            # Normalize: handle spaces, dashes, underscores, case variations
            normalized = v.lower().replace(" ", "_").replace("-", "_").strip()
            # Try direct match first
            try:
                return PropertyType(normalized)
            except ValueError:
                # Try to find in enum members (case-insensitive)
                for member_name, member_value in PropertyType.__members__.items():
                    if member_name.lower() == normalized or member_value.value.lower() == normalized:
                        return member_value
                # Default fallback
                return PropertyType.HOUSE
        return PropertyType.HOUSE

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class PropertyListResponseSchema(BaseModel):
    """Property list response schema (simplified)"""
    id: int
    title: str
    location: str
    price: float
    price_text: Optional[str] = None
    type: PropertyType
    bedrooms: int
    bathrooms: float
    area: int
    status: PropertyStatus
    is_featured: bool
    location_link: Optional[str] = None
    directions: Optional[str] = None
    primary_image: Optional[str] = None
    created_at: Optional[datetime] = None
    # Additional optional fields that may exist in database
    builder: Optional[str] = None
    configuration: Optional[str] = None
    plot_area: Optional[str] = None
    super_built_up_area: Optional[str] = None
    total_flats: Optional[str] = None
    total_floors: Optional[str] = None
    total_acres: Optional[str] = None
    property_status: Optional[str] = None  # Alternative status field

    @field_validator('is_featured', mode='before')
    @classmethod
    def parse_bool(cls, v):
        """Convert MySQL TINYINT(1) (0/1) to bool"""
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return False if v is None else bool(v)

    @field_validator('status', mode='before')
    @classmethod
    def parse_status(cls, v):
        """Convert status string to PropertyStatus enum - handles legacy DB values"""
        if not v:
            return PropertyStatus.SALE
        if isinstance(v, PropertyStatus):
            return v
        if isinstance(v, str):
            # Normalize: handle spaces, dashes, underscores, case variations
            normalized = v.lower().replace(" ", "_").replace("-", "_").strip()
            # Try direct match first
            try:
                return PropertyStatus(normalized)
            except ValueError:
                # Try to find in enum members (case-insensitive)
                for member_name, member_value in PropertyStatus.__members__.items():
                    if member_name.lower() == normalized or member_value.value.lower() == normalized:
                        return member_value
                # Default fallback
                return PropertyStatus.SALE
        return PropertyStatus.SALE

    @field_validator('type', mode='before')
    @classmethod
    def parse_type(cls, v):
        """Convert type string to PropertyType enum - handles legacy DB values"""
        if not v:
            return PropertyType.HOUSE
        if isinstance(v, PropertyType):
            return v
        if isinstance(v, str):
            # Normalize: handle spaces, dashes, underscores, case variations
            normalized = v.lower().replace(" ", "_").replace("-", "_").strip()
            # Try direct match first
            try:
                return PropertyType(normalized)
            except ValueError:
                # Try to find in enum members (case-insensitive)
                for member_name, member_value in PropertyType.__members__.items():
                    if member_name.lower() == normalized or member_value.value.lower() == normalized:
                        return member_value
                # Default fallback
                return PropertyType.HOUSE
        return PropertyType.HOUSE

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class PropertyFilterSchema(BaseModel):
    """Schema for property filtering"""
    type: Optional[PropertyType] = None
    status: Optional[PropertyStatus] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    min_bedrooms: Optional[int] = Field(None, ge=0)
    max_bedrooms: Optional[int] = Field(None, ge=0)
    min_area: Optional[int] = Field(None, ge=0)
    max_area: Optional[int] = Field(None, ge=0)
    location: Optional[str] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = True


# ============================================
# PARTNER SCHEMAS
# ============================================

class PartnerCreateSchema(BaseModel):
    """Schema for creating a partner"""
    name: str = Field(..., max_length=255)
    logo_url: Optional[str] = None  # Removed max_length to allow base64 images (will be converted to file)
    website_url: Optional[str] = None  # Changed from HttpUrl to str for flexibility
    is_active: bool = True
    display_order: int = 0


class PartnerUpdateSchema(BaseModel):
    """Schema for updating a partner"""
    name: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = None  # Removed max_length to allow base64 images (will be converted to file)
    website_url: Optional[str] = None  # Changed from HttpUrl to str for flexibility
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class PartnerResponseSchema(BaseModel):
    """Partner response schema"""
    id: int
    name: str
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    display_order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('is_active', mode='before')
    @classmethod
    def parse_bool(cls, v):
        """Convert MySQL TINYINT(1) (0/1) to bool"""
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return False if v is None else bool(v)

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


# ============================================
# TESTIMONIAL SCHEMAS
# ============================================

class TestimonialCreateSchema(BaseModel):
    """Schema for creating a testimonial"""
    client_name: str = Field(..., max_length=255)
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = Field(None, max_length=20)
    service_type: Optional[str] = Field(None, max_length=100)
    rating: Optional[int] = Field(None, ge=1, le=5)
    message: str
    is_approved: bool = False
    is_featured: bool = False


class TestimonialUpdateSchema(BaseModel):
    """Schema for updating a testimonial"""
    client_name: Optional[str] = Field(None, max_length=255)
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = Field(None, max_length=20)
    service_type: Optional[str] = Field(None, max_length=100)
    rating: Optional[int] = Field(None, ge=1, le=5)
    message: Optional[str] = None
    is_approved: Optional[bool] = None
    is_featured: Optional[bool] = None


class TestimonialResponseSchema(BaseModel):
    """Testimonial response schema"""
    id: int
    client_name: str
    client_email: Optional[str]
    client_phone: Optional[str]
    service_type: Optional[str]
    rating: Optional[int]
    message: str
    is_approved: bool
    is_featured: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('is_approved', 'is_featured', mode='before')
    @classmethod
    def parse_bool(cls, v):
        """Convert MySQL TINYINT(1) (0/1) to bool"""
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return False

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class TestimonialPublicSchema(BaseModel):
    """Public testimonial schema (only approved)"""
    id: int
    client_name: str
    service_type: Optional[str]
    rating: Optional[int]
    message: str
    is_featured: bool
    created_at: Optional[datetime] = None

    @field_validator('is_featured', mode='before')
    @classmethod
    def parse_bool(cls, v):
        """Convert MySQL TINYINT(1) (0/1) to bool"""
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return False

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


# ============================================
# CONTACT INQUIRY SCHEMAS
# ============================================

class ContactInquiryCreateSchema(BaseModel):
    """Schema for creating a contact inquiry"""
    name: str = Field(..., max_length=255)
    email: EmailStr
    subject: Optional[str] = Field(None, max_length=255)
    message: str
    phone: Optional[str] = Field(None, max_length=20)
    property_id: Optional[int] = None
    # Note: ip_address is captured server-side, not from client input


class ContactInquiryUpdateSchema(BaseModel):
    """Schema for updating a contact inquiry"""
    name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    subject: Optional[str] = Field(None, max_length=255)
    message: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    property_id: Optional[int] = None
    status: Optional[InquiryStatus] = None
    ip_address: Optional[str] = Field(None, max_length=45)


class ContactInquiryResponseSchema(BaseModel):
    """Contact inquiry response schema"""
    id: int
    name: str
    email: str
    subject: Optional[str]
    message: str
    phone: Optional[str]
    property_id: Optional[int]
    status: InquiryStatus
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('status', mode='before')
    @classmethod
    def parse_status(cls, v):
        """Convert status string to InquiryStatus enum - handles legacy DB values"""
        if not v:
            return InquiryStatus.NEW
        if isinstance(v, InquiryStatus):
            return v
        if isinstance(v, str):
            # Normalize: handle spaces, dashes, underscores, case variations
            normalized = v.lower().replace(" ", "_").replace("-", "_").strip()
            # Try direct match first
            try:
                return InquiryStatus(normalized)
            except ValueError:
                # Try to find in enum members (case-insensitive)
                for member_name, member_value in InquiryStatus.__members__.items():
                    if member_name.lower() == normalized or member_value.value.lower() == normalized:
                        return member_value
                # Default fallback
                return InquiryStatus.NEW
        return InquiryStatus.NEW

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


# ============================================
# STATISTICS SCHEMAS
# ============================================

class PropertyStatsSchema(BaseModel):
    """Property statistics schema"""
    total: int
    for_sale: int
    for_rent: int
    by_type: dict
    featured: int


class DashboardStatsSchema(BaseModel):
    """Dashboard statistics schema"""
    total_properties: int
    active_properties: int
    featured_properties: int
    total_partners: int
    active_partners: int
    total_testimonials: int
    approved_testimonials: int
    new_inquiries: int
    total_inquiries: int
    total_logs: int
    properties_by_type: dict
    properties_by_status: dict


class FrontendStatsSchema(BaseModel):
    """Frontend statistics schema for homepage"""
    properties_listed: int
    happy_clients: int
    years_experience: int
    deals_closed: int


# ============================================
# AUTHENTICATION SCHEMAS
# ============================================

class LoginSchema(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class LoginResponseSchema(BaseModel):
    """Login response schema"""
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None


class TokenData(BaseModel):
    """Token data schema"""
    user_id: int
    email: str
    role: str


# ============================================
# USER SCHEMAS
# ============================================

class UserCreateSchema(BaseModel):
    """Schema for creating a user"""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password (will be hashed)")
    full_name: Optional[str] = Field(None, max_length=255)
    role: UserRole = UserRole.ADMIN
    is_active: bool = True


class UserUpdateSchema(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, description="New password (will be hashed)")
    full_name: Optional[str] = Field(None, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponseSchema(BaseModel):
    """User response schema"""
    id: int
    email: str
    full_name: Optional[str]
    role: UserRole
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_serializer('created_at', 'updated_at', 'last_login')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


# ============================================
# VISITOR INFO SCHEMAS
# ============================================

class VisitorInfoCreateSchema(BaseModel):
    """Schema for creating visitor info from popup modal"""
    full_name: str = Field(..., max_length=255)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    looking_for: Optional[str] = None


class VisitorInfoResponseSchema(BaseModel):
    """Visitor info response schema"""
    id: int
    full_name: str
    email: str
    phone: str
    looking_for: Optional[str]
    ip_address: Optional[str] = Field(None, max_length=45)
    created_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


# ============================================
# LOG SCHEMAS
# ============================================

class LogCreateSchema(BaseModel):
    """Schema for creating a log entry"""
    log_type: str = Field(..., max_length=50, description="Type of log (info, warning, error, action)")
    action: str = Field(..., max_length=100, description="Action performed")
    description: Optional[str] = None
    user_email: Optional[str] = Field(None, max_length=255)
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    metadata: Optional[dict] = None


class LogResponseSchema(BaseModel):
    """Log response schema"""
    id: int
    log_type: str
    action: str
    description: Optional[str]
    user_email: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    metadata: Optional[dict]
    created_at: Optional[datetime] = None

    @field_validator('metadata', mode='before')
    @classmethod
    def parse_metadata(cls, v):
        """Parse JSON metadata from MySQL string or dict"""
        if v is None:
            return None
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v) if v else None
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


# ============================================
# SEARCH SCHEMAS
# ============================================

class SearchQuerySchema(BaseModel):
    """Search query schema"""
    query: Optional[str] = None
    filters: Optional[PropertyFilterSchema] = None
    pagination: Optional[PaginationParams] = None
    sort_by: Optional[str] = Field(None, description="Sort field (price, created_at, etc.)")
    sort_order: Optional[str] = Field(None, pattern="^(asc|desc)$", description="Sort order")


class SearchResponseSchema(BaseModel):
    """Search response schema"""
    total: int
    page: int
    limit: int
    pages: int
    results: List[PropertyListResponseSchema]


# ============================================
# BLOG SCHEMAS
# ============================================

class BlogCreateSchema(BaseModel):
    """Schema for creating a blog"""
    title: str = Field(..., max_length=255)
    excerpt: Optional[str] = None
    content: str
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = Field(default=[], description="List of tags")
    image_url: Optional[str] = None
    author: Optional[str] = Field(None, max_length=255)
    views: int = 0
    is_featured: bool = False
    is_active: bool = True


class BlogUpdateSchema(BaseModel):
    """Schema for updating a blog"""
    title: Optional[str] = Field(None, max_length=255)
    excerpt: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None
    author: Optional[str] = Field(None, max_length=255)
    views: Optional[int] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None


class BlogResponseSchema(BaseModel):
    """Blog response schema"""
    id: int
    title: str
    excerpt: Optional[str]
    content: Optional[str]
    category: Optional[str]
    tags: Optional[List[str]]
    image_url: Optional[str]
    author: Optional[str]
    views: int
    is_featured: bool
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, v):
        """Parse JSON tags from MySQL string or list"""
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                parsed = json.loads(v) if v else []
                return parsed if isinstance(parsed, list) else []
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @field_validator('is_featured', 'is_active', mode='before')
    @classmethod
    def parse_bool(cls, v):
        """Convert MySQL TINYINT(1) (0/1) to bool"""
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return False if v is None else bool(v)

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


# ============================================
# SYSTEM METRICS SCHEMAS
# ============================================

class SystemMetricsCreateSchema(BaseModel):
    """Schema for creating a system metrics entry"""
    cpu_usage: float = Field(..., ge=0, le=100, description="CPU usage percentage")
    ram_usage: float = Field(..., ge=0, le=100, description="RAM usage percentage")
    ram_used_mb: float = Field(..., ge=0, description="RAM used in MB")
    ram_total_mb: float = Field(..., ge=0, description="Total RAM in MB")
    bandwidth_in_mb: float = Field(0, ge=0, description="Bandwidth in (MB)")
    bandwidth_out_mb: float = Field(0, ge=0, description="Bandwidth out (MB)")
    bandwidth_total_mb: float = Field(0, ge=0, description="Total bandwidth (MB)")


class SystemMetricsResponseSchema(BaseModel):
    """System metrics response schema"""
    id: int
    cpu_usage: float
    ram_usage: float
    ram_used_mb: float
    ram_total_mb: float
    bandwidth_in_mb: float
    bandwidth_out_mb: float
    bandwidth_total_mb: float
    created_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class SystemMetricsListResponseSchema(BaseModel):
    """System metrics list response schema"""
    success: bool
    metrics: List[SystemMetricsResponseSchema]
    message: Optional[str] = None


# ============================================
# TEMPORARY METRICS SCHEMAS
# ============================================

class TemporaryMetricsCreateSchema(BaseModel):
    """Schema for creating a temporary metrics entry (for stat cards auto-refresh)"""
    cpu_usage: float = Field(..., ge=0, le=100, description="CPU usage percentage")
    ram_usage: float = Field(..., ge=0, le=100, description="RAM usage percentage")
    ram_used_mb: float = Field(..., ge=0, description="RAM used in MB")
    ram_total_mb: float = Field(..., ge=0, description="Total RAM in MB")
    bandwidth_in_mb: float = Field(0, ge=0, description="Bandwidth in (MB)")
    bandwidth_out_mb: float = Field(0, ge=0, description="Bandwidth out (MB)")
    bandwidth_total_mb: float = Field(0, ge=0, description="Total bandwidth (MB)")


class TemporaryMetricsResponseSchema(BaseModel):
    """Temporary metrics response schema (for stat cards)"""
    id: int
    cpu_usage: float
    ram_usage: float
    ram_used_mb: float
    ram_total_mb: float
    bandwidth_in_mb: float
    bandwidth_out_mb: float
    bandwidth_total_mb: float
    created_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class TemporaryMetricsCurrentResponseSchema(BaseModel):
    """Current temporary metrics response schema (latest entry for stat cards)"""
    success: bool
    metrics: Optional[TemporaryMetricsResponseSchema] = None
    message: Optional[str] = None


# ============================================
# CACHE LOG SCHEMAS
# ============================================

class CacheLogCreateSchema(BaseModel):
    """Schema for creating a cache log entry"""
    cache_key: str = Field(..., max_length=500, description="Cache key that was accessed")
    operation: CacheOperation = Field(..., description="Cache operation: hit, miss, set, delete")
    cache_type: Optional[str] = Field(None, max_length=50, description="Type of cache: property, partner, testimonial, etc.")
    response_time_ms: Optional[float] = Field(None, ge=0, description="Response time in milliseconds")
    cache_size_kb: Optional[float] = Field(None, ge=0, description="Size of cached data in KB")
    status: CacheStatus = Field(CacheStatus.SUCCESS, description="Operation status: success, error")
    error_message: Optional[str] = Field(None, description="Error message if operation failed")
    ip_address: Optional[str] = Field(None, max_length=45, description="IP address of the request")
    user_agent: Optional[str] = Field(None, description="User agent of the request")
    metadata: Optional[dict] = Field(None, description="Additional metadata about the cache operation")


class CacheLogResponseSchema(BaseModel):
    """Cache log response schema"""
    id: int
    cache_key: str
    operation: CacheOperation
    cache_type: Optional[str] = None
    response_time_ms: Optional[float] = None
    cache_size_kb: Optional[float] = None
    status: CacheStatus
    error_message: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: Optional[datetime] = None

    @field_validator('metadata', mode='before')
    @classmethod
    def parse_metadata(cls, v):
        """Parse JSON metadata from MySQL string or dict"""
        if v is None:
            return None
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v) if v else None
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    @field_validator('operation', mode='before')
    @classmethod
    def parse_operation(cls, v):
        """Convert operation string to CacheOperation enum - handles legacy DB values"""
        if not v:
            return CacheOperation.HIT
        if isinstance(v, CacheOperation):
            return v
        if isinstance(v, str):
            # Normalize: handle spaces, dashes, underscores, case variations
            normalized = v.lower().replace(" ", "_").replace("-", "_").strip()
            # Try direct match first
            try:
                return CacheOperation(normalized)
            except ValueError:
                # Try to find in enum members (case-insensitive)
                for member_name, member_value in CacheOperation.__members__.items():
                    if member_name.lower() == normalized or member_value.value.lower() == normalized:
                        return member_value
                # Default fallback
                return CacheOperation.HIT
        return CacheOperation.HIT

    @field_validator('status', mode='before')
    @classmethod
    def parse_status(cls, v):
        """Convert status string to CacheStatus enum - handles legacy DB values"""
        if not v:
            return CacheStatus.SUCCESS
        if isinstance(v, CacheStatus):
            return v
        if isinstance(v, str):
            # Normalize: handle spaces, dashes, underscores, case variations
            normalized = v.lower().replace(" ", "_").replace("-", "_").strip()
            # Try direct match first
            try:
                return CacheStatus(normalized)
            except ValueError:
                # Try to find in enum members (case-insensitive)
                for member_name, member_value in CacheStatus.__members__.items():
                    if member_name.lower() == normalized or member_value.value.lower() == normalized:
                        return member_value
                # Default fallback
                return CacheStatus.SUCCESS
        return CacheStatus.SUCCESS

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow extra fields from database


class CacheLogListResponseSchema(BaseModel):
    """Cache log list response schema with pagination"""
    success: bool
    logs: List[CacheLogResponseSchema] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    limit: int = 50
    pages: int = 0
    has_more: bool = False
    message: Optional[str] = None


class CacheLogFilterSchema(BaseModel):
    """Schema for filtering cache logs"""
    operation: Optional[CacheOperation] = None
    status: Optional[CacheStatus] = None
    cache_type: Optional[str] = None
    search: Optional[str] = None
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(50, ge=1, le=500, description="Items per page")
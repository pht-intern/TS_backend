"""
Database Models for Tirumakudalu Properties
Pydantic models for data validation and serialization
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from enum import Enum


# Enums for type safety
class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    VILLA = "villa"


class PropertyStatus(str, Enum):
    SALE = "sale"
    RENT = "rent"
    RESALE = "resale"
    NEW = "new"


class InquiryStatus(str, Enum):
    NEW = "new"
    READ = "read"
    REPLIED = "replied"
    CLOSED = "closed"


# ============================================
# PROPERTY MODELS
# ============================================

class PropertyBase(BaseModel):
    """Base property model with common fields"""
    title: str = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    price: float = Field(..., gt=0)
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


class PropertyCreate(PropertyBase):
    """Model for creating a new property"""
    pass


class PropertyUpdate(BaseModel):
    """Model for updating a property (all fields optional)"""
    title: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    price: Optional[float] = Field(None, gt=0)
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


class Property(PropertyBase):
    """Complete property model with database fields"""
    id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


class PropertyWithDetails(Property):
    """Property model with related images and features"""
    images: List['PropertyImage'] = []
    project_images: List['PropertyProjectImage'] = []
    floorplan_images: List['PropertyFloorplanImage'] = []
    masterplan_images: List['PropertyMasterplanImage'] = []
    features: List['PropertyFeature'] = []


# ============================================
# PROPERTY IMAGE MODELS
# ============================================

class PropertyImageBase(BaseModel):
    """Base property image model"""
    property_id: int
    image_url: str = Field(...)  # Removed max_length=500 to allow TEXT (base64 images can be long)
    image_order: int = 0
    is_primary: bool = False


class PropertyImageCreate(PropertyImageBase):
    """Model for creating a new property image"""
    pass


class PropertyImage(PropertyImageBase):
    """Complete property image model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# PROPERTY CATEGORIZED IMAGE MODELS
# ============================================

class PropertyImageCategory(str, Enum):
    """Property image category enum"""
    PROJECT = "project"
    FLOORPLAN = "floorplan"
    MASTERPLAN = "masterplan"


class PropertyProjectImageBase(BaseModel):
    """Base property project image model"""
    property_id: int
    image_url: str = Field(...)
    image_order: int = 0


class PropertyProjectImageCreate(PropertyProjectImageBase):
    """Model for creating a new property project image"""
    pass


class PropertyProjectImage(PropertyProjectImageBase):
    """Complete property project image model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


class PropertyFloorplanImageBase(BaseModel):
    """Base property floorplan image model"""
    property_id: int
    image_url: str = Field(...)
    image_order: int = 0


class PropertyFloorplanImageCreate(PropertyFloorplanImageBase):
    """Model for creating a new property floorplan image"""
    pass


class PropertyFloorplanImage(PropertyFloorplanImageBase):
    """Complete property floorplan image model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


class PropertyMasterplanImageBase(BaseModel):
    """Base property masterplan image model"""
    property_id: int
    image_url: str = Field(...)
    image_order: int = 0


class PropertyMasterplanImageCreate(PropertyMasterplanImageBase):
    """Model for creating a new property masterplan image"""
    pass


class PropertyMasterplanImage(PropertyMasterplanImageBase):
    """Complete property masterplan image model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# PROPERTY FEATURE MODELS
# ============================================

class PropertyFeatureBase(BaseModel):
    """Base property feature model"""
    property_id: int
    feature_name: str = Field(..., max_length=100)


class PropertyFeatureCreate(PropertyFeatureBase):
    """Model for creating a new property feature"""
    pass


class PropertyFeature(PropertyFeatureBase):
    """Complete property feature model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# PARTNER MODELS
# ============================================

class PartnerBase(BaseModel):
    """Base partner model"""
    name: str = Field(..., max_length=255)
    logo_url: Optional[str] = None
    website_url: Optional[str] = Field(None, max_length=500)
    is_active: bool = True
    display_order: int = 0


class PartnerCreate(PartnerBase):
    """Model for creating a new partner"""
    pass


class PartnerUpdate(BaseModel):
    """Model for updating a partner"""
    name: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=500)
    website_url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class Partner(PartnerBase):
    """Complete partner model"""
    id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# TESTIMONIAL MODELS
# ============================================

class TestimonialBase(BaseModel):
    """Base testimonial model"""
    client_name: str = Field(..., max_length=255)
    client_email: Optional[str] = Field(None, max_length=255)
    client_phone: Optional[str] = Field(None, max_length=20)
    service_type: Optional[str] = Field(None, max_length=100)
    rating: Optional[int] = Field(None, ge=1, le=5)
    message: str
    is_approved: bool = False
    is_featured: bool = False


class TestimonialCreate(TestimonialBase):
    """Model for creating a new testimonial"""
    pass


class TestimonialUpdate(BaseModel):
    """Model for updating a testimonial"""
    client_name: Optional[str] = Field(None, max_length=255)
    client_email: Optional[str] = Field(None, max_length=255)
    client_phone: Optional[str] = Field(None, max_length=20)
    service_type: Optional[str] = Field(None, max_length=100)
    rating: Optional[int] = Field(None, ge=1, le=5)
    message: Optional[str] = None
    is_approved: Optional[bool] = None
    is_featured: Optional[bool] = None


class Testimonial(TestimonialBase):
    """Complete testimonial model"""
    id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# CONTACT INQUIRY MODELS
# ============================================

class ContactInquiryBase(BaseModel):
    """Base contact inquiry model"""
    name: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    subject: Optional[str] = Field(None, max_length=255)
    message: str
    phone: Optional[str] = Field(None, max_length=20)
    property_id: Optional[int] = None
    status: InquiryStatus = InquiryStatus.NEW
    ip_address: Optional[str] = Field(None, max_length=45)


class ContactInquiryCreate(ContactInquiryBase):
    """Model for creating a new contact inquiry"""
    pass


class ContactInquiryUpdate(BaseModel):
    """Model for updating a contact inquiry"""
    name: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    subject: Optional[str] = Field(None, max_length=255)
    message: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    property_id: Optional[int] = None
    status: Optional[InquiryStatus] = None
    ip_address: Optional[str] = Field(None, max_length=45)


class ContactInquiry(ContactInquiryBase):
    """Complete contact inquiry model"""
    id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# SYSTEM METRICS MODELS
# ============================================

class SystemMetricsBase(BaseModel):
    """Base system metrics model"""
    cpu_usage: float = Field(..., ge=0, le=100, description="CPU usage percentage")
    ram_usage: float = Field(..., ge=0, le=100, description="RAM usage percentage")
    ram_used_mb: float = Field(..., ge=0, description="RAM used in MB")
    ram_total_mb: float = Field(..., ge=0, description="Total RAM in MB")
    bandwidth_in_mb: float = Field(0, ge=0, description="Bandwidth in (MB)")
    bandwidth_out_mb: float = Field(0, ge=0, description="Bandwidth out (MB)")
    bandwidth_total_mb: float = Field(0, ge=0, description="Total bandwidth (MB)")


class SystemMetricsCreate(SystemMetricsBase):
    """Model for creating a new system metrics entry"""
    pass


class SystemMetrics(SystemMetricsBase):
    """Complete system metrics model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# TEMPORARY METRICS MODELS
# ============================================

class TemporaryMetricsBase(BaseModel):
    """Base temporary metrics model (for stat cards auto-refresh)"""
    cpu_usage: float = Field(..., ge=0, le=100, description="CPU usage percentage")
    ram_usage: float = Field(..., ge=0, le=100, description="RAM usage percentage")
    ram_used_mb: float = Field(..., ge=0, description="RAM used in MB")
    ram_total_mb: float = Field(..., ge=0, description="Total RAM in MB")
    bandwidth_in_mb: float = Field(0, ge=0, description="Bandwidth in (MB)")
    bandwidth_out_mb: float = Field(0, ge=0, description="Bandwidth out (MB)")
    bandwidth_total_mb: float = Field(0, ge=0, description="Total bandwidth (MB)")


class TemporaryMetricsCreate(TemporaryMetricsBase):
    """Model for creating a new temporary metrics entry"""
    pass


class TemporaryMetrics(TemporaryMetricsBase):
    """Complete temporary metrics model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# BLOG MODELS
# ============================================

class BlogBase(BaseModel):
    """Base blog model"""
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


class BlogCreate(BlogBase):
    """Model for creating a new blog"""
    pass


class BlogUpdate(BaseModel):
    """Model for updating a blog (all fields optional)"""
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


class Blog(BlogBase):
    """Complete blog model"""
    id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# USER MODELS
# ============================================

class UserRole(str, Enum):
    """User role enum"""
    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    """Base user model"""
    email: str = Field(..., max_length=255)
    password_hash: str = Field(..., max_length=255)
    full_name: Optional[str] = Field(None, max_length=255)
    role: UserRole = UserRole.ADMIN
    is_active: bool = True


class UserCreate(BaseModel):
    """Model for creating a new user"""
    email: str = Field(..., max_length=255)
    password: str  # Will be hashed before storage
    full_name: Optional[str] = Field(None, max_length=255)
    role: UserRole = UserRole.ADMIN
    is_active: bool = True


class UserUpdate(BaseModel):
    """Model for updating a user (all fields optional)"""
    email: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = None  # Will be hashed before storage
    password_hash: Optional[str] = Field(None, max_length=255)
    full_name: Optional[str] = Field(None, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """Complete user model"""
    id: int
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at', 'last_login')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# VISITOR INFO MODELS
# ============================================

class VisitorInfoBase(BaseModel):
    """Base visitor info model"""
    full_name: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    phone: str = Field(..., max_length=20)
    looking_for: Optional[str] = None
    ip_address: Optional[str] = Field(None, max_length=45)


class VisitorInfoCreate(VisitorInfoBase):
    """Model for creating a new visitor info entry"""
    pass


class VisitorInfo(VisitorInfoBase):
    """Complete visitor info model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# LOG MODELS
# ============================================

class LogType(str, Enum):
    """Log type enum"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    ACTION = "action"


class LogBase(BaseModel):
    """Base log model"""
    log_type: str = Field(..., max_length=50, description="Type of log (info, warning, error, action)")
    action: str = Field(..., max_length=100, description="Action performed")
    description: Optional[str] = None
    user_email: Optional[str] = Field(None, max_length=255)
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    metadata: Optional[dict] = None


class LogCreate(LogBase):
    """Model for creating a new log entry"""
    pass


class Log(LogBase):
    """Complete log model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# CACHE LOG MODELS
# ============================================

class CacheOperation(str, Enum):
    """Cache operation type enum"""
    HIT = "hit"
    MISS = "miss"
    SET = "set"
    DELETE = "delete"


class CacheStatus(str, Enum):
    """Cache operation status enum"""
    SUCCESS = "success"
    ERROR = "error"


class CacheLogBase(BaseModel):
    """Base cache log model"""
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


class CacheLogCreate(CacheLogBase):
    """Model for creating a new cache log entry"""
    pass


class CacheLog(CacheLogBase):
    """Complete cache log model"""
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime, _info):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True


# ============================================
# HELPER FUNCTIONS
# ============================================

def dict_to_model(model_class: type[BaseModel], data: dict) -> BaseModel:
    """Convert dictionary to Pydantic model"""
    return model_class(**data)


def model_to_dict(model: BaseModel, exclude_none: bool = False) -> dict:
    """Convert Pydantic model to dictionary"""
    return model.model_dump(exclude_none=exclude_none)


# Update forward references
PropertyWithDetails.model_rebuild()
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
    BUILDER_FLOOR = "builder_floor"


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


from typing import Optional

from sqlmodel import Field, SQLModel


class Agency(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(index=True)
    street: Optional[str] = None
    zipcode: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class Listing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agency_id: Optional[int] = Field(default=None, foreign_key="agency.id")
    alternative_reference: Optional[str] = None
    attributes: Optional[str] = None
    city: Optional[str] = None
    cover_image: Optional[int] = None
    created: Optional[str] = None
    description: Optional[str] = None
    description_title: Optional[str] = None
    # documents: Optional[List[str]] = None
    floor: Optional[str] = None
    # images: Optional[List[int]] = None
    is_furnished: Optional[bool] = None
    is_selling_furniture: Optional[int] = None
    is_temporary: Optional[bool] = None
    latitude: Optional[float] = None
    live_viewing_url: Optional[str] = None
    livingspace: Optional[int] = None
    longitude: Optional[float] = None
    moving_date: Optional[str] = None
    moving_date_type: Optional[str] = None
    number_of_rooms: Optional[str] = None
    object_category: Optional[str] = None
    object_type: Optional[str] = None
    offer_type: Optional[str] = None
    pitch_title: Optional[str] = None
    pk: Optional[int] = None
    price_display: Optional[int] = None
    price_display_type: Optional[str] = None
    price_unit: Optional[str] = None
    public_address: Optional[str] = None
    public_title: Optional[str] = None
    published: Optional[str] = None
    ref_house: Optional[str] = None
    ref_object: Optional[str] = None
    ref_property: Optional[str] = None
    reference: Optional[str] = None
    rent_charges: Optional[str] = None
    rent_gross: Optional[str] = None
    rent_net: Optional[str] = None
    rent_title: Optional[str] = None
    reserved: Optional[bool] = None
    short_title: Optional[str] = None
    short_url: Optional[str] = None
    slug: Optional[str] = None
    space_display: Optional[str] = None
    status: Optional[str] = None
    street: Optional[str] = None
    submit_url: Optional[str] = None
    surface_living: Optional[int] = None
    surface_property: Optional[int] = None
    surface_usable: Optional[int] = None
    surface_usable_minimum: Optional[int] = None
    tour_url: Optional[str] = None
    url: Optional[str] = None
    video_url: Optional[str] = None
    volume: Optional[int] = None
    website_url: Optional[str] = None
    year_built: Optional[int] = None
    year_renovated: Optional[int] = None
    zipcode: Optional[bool] = None

from ninja import NinjaAPI
from .models import Trip, Step, Photo
from django.shortcuts import get_object_or_404
from ninja import Schema

api = NinjaAPI()


class CoverPhotoRef(Schema):
    id: int
    url: str

class PhotoSchema(Schema):
    id: int
    name: str
    description: str | None = None
    date: str
    url: str

class StepSchema(Schema):
    id: int
    name: str
    lat: float
    lng: float
    description: str
    cover_photo: CoverPhotoRef | None = None
    photos: list[PhotoSchema] = []

class StepCreateSchema(Schema):
    name: str
    lat: float
    lng: float
    description: str

class TripSchema(Schema):
    id: int
    name: str
    cover_photo: CoverPhotoRef | None = None
    steps: list[StepSchema] = []

class PhotoCreateSchema(Schema):
    name: str
    description: str | None = None
    url: str

@api.get("/trips", response=list[TripSchema])
def list_trips(request):
    trips = Trip.objects.prefetch_related(
        'cover_photo',
        'steps__cover_photo',
        'steps__photos'
    ).all()
    return [TripSchema(
        id=t.id, #type: ignore
        name=t.name,
        steps=[
            StepSchema(
                id=s.id,
                name=s.name,
                lat=s.lat,
                lng=s.lng,
                description=s.description,
                cover_photo=(
                    CoverPhotoRef(id=s.cover_photo.id, url=s.cover_photo.url) # type: ignore
                    if s.cover_photo else None
                ),
                photos=[
                    PhotoSchema(
                        id=p.id,
                        name=p.name,
                        description=p.description,
                        date=p.date.isoformat(),
                        url=p.url
                    ) for p in s.photos.all() # type: ignore
                ]
            ) for s in t.steps.all() #type: ignore
        ]
        , cover_photo=(
            CoverPhotoRef(id=t.cover_photo.id, url=t.cover_photo.url) # type: ignore
            if t.cover_photo else None
        )
    ) for t in trips]

@api.post("/trips", response=TripSchema)
def create_trip(request, data: TripSchema):
    trip = Trip.objects.create(name=data.name)
    return TripSchema(id=trip.id, name=trip.name, steps=[]) # type: ignore

@api.post("/trips/{trip_id}/steps", response=StepSchema)
def add_step(request, trip_id: int, data: StepCreateSchema):
    trip = get_object_or_404(Trip, id=trip_id)
    step = Step.objects.create(trip=trip, **data.dict())
    return StepSchema(id=step.id, name=step.name, lat=step.lat, lng=step.lng, description=step.description) # type: ignore

@api.post("/trips/{trip_id}/steps/{step_id}/photos", response=PhotoSchema)
def create_photo(request, trip_id: int, step_id: int, data: PhotoCreateSchema):
    step = get_object_or_404(Step, id=step_id, trip_id=trip_id)
    photo = Photo.objects.create(step=step, name=data.name, description=data.description, url=data.url)
    return PhotoSchema(id=photo.id, name=photo.name, description=photo.description, date=photo.date.isoformat(), url=photo.url) # type: ignore

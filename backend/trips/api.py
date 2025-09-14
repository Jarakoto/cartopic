from ninja import NinjaAPI
from .models import Trip, Step, Photo
from django.shortcuts import get_object_or_404
from ninja import Schema, File, Form
from ninja.files import UploadedFile
from .services.owncloud import upload_file, OwnCloudError

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
    order: int
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

class PhotoUploadResponse(Schema):
    id: int
    name: str
    description: str | None = None
    url: str
    date: str

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
                order=s.order,  # type: ignore[attr-defined]
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
            ) for s in t.steps.all().order_by('order') #type: ignore
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
    return StepSchema(id=step.id, name=step.name, lat=step.lat, lng=step.lng, description=step.description, order=step.order) # type: ignore[attr-defined]

@api.post("/trips/{trip_id}/steps/{step_id}/photos", response=PhotoSchema)
def create_photo(request, trip_id: int, step_id: int, data: PhotoCreateSchema):
    step = get_object_or_404(Step, id=step_id, trip_id=trip_id)
    photo = Photo.objects.create(step=step, name=data.name, description=data.description, url=data.url)
    return PhotoSchema(id=photo.id, name=photo.name, description=photo.description, date=photo.date.isoformat(), url=photo.url) # type: ignore

@api.post("/trips/{trip_id}/steps/{step_id}/photos/upload", response=PhotoUploadResponse)
def upload_photo(
    request,
    trip_id: int,
    step_id: int,
    file: UploadedFile = File(...),  # type: ignore
    name: str | None = Form(None),  # type: ignore
    description: str | None = Form(None),  # type: ignore
):  # type: ignore
    """Upload a photo file and create a Photo record.

    name / description are expected as multipart form fields together with the file.
    """
    step = get_object_or_404(Step, id=step_id, trip_id=trip_id)
    display_name = name or file.name
    try:
        share_page_url, direct_url = upload_file(file.read(), file.name)
    except OwnCloudError as e:
        status = 400 if 'incomplete' in str(e).lower() else 500
        return api.create_response(request, {"error": str(e)}, status=status)
    photo = Photo.objects.create(step=step, name=display_name, description=description, url=direct_url)
    return PhotoUploadResponse(
    id=photo.id,  # type: ignore[attr-defined]
        name=photo.name,
        description=photo.description,
        url=photo.url,
        date=photo.date.isoformat(),
    )  # type: ignore

from ninja import NinjaAPI
from .models import Trip, Step
from django.shortcuts import get_object_or_404
from ninja import Schema

api = NinjaAPI()


class StepSchema(Schema):
    id: int
    name: str
    lat: float
    lng: float
    description: str

class StepCreateSchema(Schema):
    name: str
    lat: float
    lng: float
    description: str

class TripSchema(Schema):
    id: int
    name: str
    steps: list[StepSchema] = []

@api.get("/trips", response=list[TripSchema])
def list_trips(request):
    trips = Trip.objects.prefetch_related('steps').all()
    return [TripSchema(
        id=t.id, #type: ignore
        name=t.name,
        steps=[
            StepSchema(
                id=s.id,
                name=s.name,
                lat=s.lat,
                lng=s.lng,
                description=s.description
            ) for s in t.steps.all() #type: ignore
        ]
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

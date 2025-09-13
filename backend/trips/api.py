from ninja import NinjaAPI
from .models import Trip, Step
from django.shortcuts import get_object_or_404
from ninja import Schema

api = NinjaAPI()

class StepSchema(Schema):
    id: int
    name: str

class TripSchema(Schema):
    id: int
    name: str
    steps: list[StepSchema] = []

@api.get("/trips", response=list[TripSchema])
def list_trips(request):
    trips = Trip.objects.prefetch_related('steps').all()
    return [TripSchema(id=t.id, name=t.name, steps=[StepSchema(id=s.id, name=s.name) for s in t.steps.all()]) for t in trips] # type: ignore

@api.post("/trips", response=TripSchema)
def create_trip(request, data: TripSchema):
    trip = Trip.objects.create(name=data.name)
    return TripSchema(id=trip.id, name=trip.name, steps=[]) # type: ignore

@api.post("/trips/{trip_id}/steps", response=StepSchema)
def add_step(request, trip_id: int, data: StepSchema):
    trip = get_object_or_404(Trip, id=trip_id)
    step = Step.objects.create(trip=trip, name=data.name)
    return StepSchema(id=step.id, name=step.name) # type: ignore

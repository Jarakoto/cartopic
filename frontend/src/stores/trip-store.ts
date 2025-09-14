import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from 'boot/axios';
import camelcaseKeys from 'camelcase-keys';
import { type AxiosInstance } from 'axios';

export interface CoverPhotoRef { id: number; url: string }

export interface Photo {
  id: number;
  name: string;
  description?: string | null;
  date: string;
  url: string;
}

export interface Step {
  id: number;
  name: string;
  description: string;
  lat: number;
  lng: number;
  startedAt: Date | null;
  endedAt: Date | null;
  coverPhoto?: CoverPhotoRef | null; // optional cover reference from backend
  photos?: Photo[]; // lazy-loaded photos for carousel
}

export interface Trip {
  id: number;
  name: string;
  description: string;
  steps: Step[];
  startedAt: Date | null;
  endedAt: Date | null;
  coverPhoto?: CoverPhotoRef | null; // optional cover reference from backend
}

export const useTripStore = defineStore('trip', () => {
  const trips = ref<Trip[]>([]);
  const selectedTrip = ref<Trip | null>(null);
  const selectedStep = ref<Step | null>(null);

  async function fetchTrips(api: AxiosInstance) {
    const response = await api.get('/trips');
    trips.value = camelcaseKeys(response.data, { deep: true });
  }

  function setSelectedStep(step: Step | null) {
    if (step === null) { selectedStep.value = null; return; }
    if (selectedTrip.value) {
      const foundStep = selectedTrip.value.steps.find(s => s.id === step.id);
      if (foundStep) {
        selectedStep.value = foundStep;
      }
    }
  }

  function setSelectedTrip(trip: Trip) {
    selectedTrip.value = trip;
  }

  async function addStep(step: { name: string; description: string; lng: number; lat: number }) {
    if (!selectedTrip.value) return;
    // Add a dummy id to satisfy backend validation
    const payload = { ...step, id: Date.now() };
    const response = await api.post(`/trips/${selectedTrip.value.id}/steps`, payload);
    const newStep = response.data;
    selectedTrip.value.steps.push(newStep);
    return newStep;
  }

  // Helper to get a trip's cover URL with fallback logic (currently returns coverPhoto.url or null)
  function getTripCoverUrl(trip: Trip): string | null {
    return trip.coverPhoto?.url || null;
  }

  function getStepCoverUrl(step: Step): string | null {
    return step.coverPhoto?.url || null;
  }

  return { trips, fetchTrips, selectedTrip, selectedStep, setSelectedTrip, addStep, setSelectedStep, getTripCoverUrl, getStepCoverUrl };
});

import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from 'boot/axios';
import camelcaseKeys from 'camelcase-keys';
import { type AxiosInstance } from 'axios';

export interface Step {
  id: number;
  name: string;
  description: string;
  lat: number;
  lng: number;
  startedAt: Date | null;
  endedAt: Date | null;
}

export interface Trip {
  id: number;
  name: string;
  description: string;
  steps: Step[];
  startedAt: Date | null;
  endedAt: Date | null;
}

export const useTripStore = defineStore('trip', () => {
  const trips = ref<Trip[]>([]);
  const selectedTrip = ref<Trip | null>(null);

  async function fetchTrips(api: AxiosInstance) {
    const response = await api.get('/trips');
    trips.value = camelcaseKeys(response.data, { deep: true });
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

  return { trips, fetchTrips, selectedTrip, setSelectedTrip, addStep };
});

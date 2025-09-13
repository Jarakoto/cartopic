import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { AxiosInstance } from 'axios';
import camelcaseKeys from 'camelcase-keys';

export interface Step {
  id: number;
  name: string;
  description: string;
  latitude: number;
  longitude: number;
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

  async function fetchTrips(api: AxiosInstance) {
    const response = await api.get('/trips');
    trips.value = camelcaseKeys(response.data, { deep: true });;
  }

  return { trips, fetchTrips };
});

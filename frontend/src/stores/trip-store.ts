import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { AxiosInstance } from 'axios';

export interface Step {
  id: number;
  name: string;
}

export interface Trip {
  id: number;
  name: string;
  steps: Step[];
}

export const useTripStore = defineStore('trip', () => {
  const trips = ref<Trip[]>([]);

  async function fetchTrips(api: AxiosInstance) {
    const response = await api.get('/trips');
    trips.value = response.data;
  }

  return { trips, fetchTrips };
});

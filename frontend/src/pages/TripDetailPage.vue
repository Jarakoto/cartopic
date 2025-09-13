<template>
  <q-page class="q-pa-md">
    <q-card v-if="trip">
      <q-card-section>
        <div class="text-h6">Trip: {{ trip.name }}</div>
        <q-list>
          <q-item v-for="step in trip.steps" :key="step.id">
            <q-item-section>{{ step.name }}</q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
    <div v-else>Loading...</div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useTripStore } from 'stores/trip-store';

const route = useRoute();
const tripStore = useTripStore();
const trip = ref(tripStore.trips.find(t => t.id === Number(route.params.id)));

onMounted(() => {
  if (!trip.value) {
    // Optionally, fetch from API if not found in store
    // Or show not found message
  }
});
</script>

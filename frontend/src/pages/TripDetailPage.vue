<template>
  <q-page class="q-pa-none">
      <q-btn
        icon="arrow_back"
        class="absolute"
        style="top: 16px; left: 16px; z-index: 10;"
        @click="$router.back()"
        round
        color="primary"
        size="md"
      />
      <div id="map" class="fit"></div>
      <template v-if="mapLoaded && tripStore.selectedTrip">
        <router-view :map="map" />
      </template>
  </q-page>
</template>

<script setup lang="ts">

import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useTripStore } from 'stores/trip-store';

const route = useRoute();
const tripStore = useTripStore();
const mapLoaded = ref(false);
let map: maplibregl.Map;

onMounted(() => {
  if (!route.params.id || typeof(route.params.id) !== 'string') {
    throw new Error('Trip id is required.');
  }

  const tripId = Number(route.params.id);
  if (!tripId) {
    throw new Error('Trip id is required.');
  }
  const trip = tripStore.trips.find(t => t.id === Number(route.params.id))
  if (!trip) {
    throw new Error(`Trip with id ${route.params.id} not found.`);
  }
  tripStore.setSelectedTrip(trip)
  handleStep()

  map = new maplibregl.Map({
    container: 'map',
    style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
    center: [47.516667, -18.933333],
    zoom: 13 // high zoom
  });
  map.on('load', () => {
    mapLoaded.value = true;
  });

});
  const handleStep = () => {
    const stepId = route.params.stepId ? Number(route.params.stepId) : null;
    if (route.params.stepId && stepId === null) {
      throw new Error(`Step with id ${stepId} not found.`);
    }
    if (stepId !== null) {
      const step = tripStore.selectedTrip?.steps?.find(s => s.id === stepId);
      if (!step) {
        throw new Error(`Step with id ${stepId} not found.`);
      }
      tripStore.setSelectedStep(step);
    } else {
      tripStore.setSelectedStep(null);
    }
  };

  watch(() => route.params.stepId, handleStep);
</script>

<style lang="scss">
  #map {
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;
    .maplibregl-ctrl-attrib {
      display: none;
    }
  }
</style>

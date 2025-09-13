<template>
  <q-page class="q-pa-none">
    <div id="map" class="fit"></div>
    <StepManager v-if="mapLoaded" :map="map" />
  </q-page>
</template>

<script setup lang="ts">

import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useTripStore } from 'stores/trip-store';
import StepManager from 'components/TripDetail/StepManager.vue';

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

  map = new maplibregl.Map({
    container: 'map',
    style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL',
    center: [47.516667, -18.933333],
    zoom: 13 // high zoom
  });
  map.on('load', () => {
    mapLoaded.value = true;
  });

});

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

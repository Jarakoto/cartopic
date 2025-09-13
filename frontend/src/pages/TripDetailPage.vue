<template>
  <q-page class="q-pa-none">
    <div id="map" class="fit"></div>
  </q-page>
</template>

<script setup lang="ts">

import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useTripStore } from 'stores/trip-store';

const route = useRoute();
const tripStore = useTripStore();
const trip = ref(tripStore.trips.find(t => t.id === Number(route.params.id)));

onMounted(() => {
  if (!route.params.id || typeof(route.params.id) !== 'string') {
    throw new Error('Trip id is required.');
  }
  if (!trip.value) {
    throw new Error(`Trip with id ${route.params.id} not found.`);
  }
  new maplibregl.Map({
    container: 'map',
    style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL',
    center: [0, 0],
    zoom: 2
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

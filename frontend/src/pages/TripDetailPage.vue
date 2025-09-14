<template>
  <q-page class="q-pa-none">
    <q-btn icon="arrow_back" class="absolute" style="top: 16px; left: 16px; z-index: 10;" @click="$router.back()" round
      color="primary" size="md" />
    <div id="map" class="fit"></div>
    <!-- Step name now shown inside marker, not as floating label -->
    <template v-if="mapLoaded && tripStore.selectedTrip">
      <router-view :map="map" @add-step="handleAddStep" />
    </template>
  </q-page>
</template>

<script setup lang="ts">
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { type Step, useTripStore } from 'stores/trip-store';

const route = useRoute();
const tripStore = useTripStore();
const mapLoaded = ref(false);
let map: maplibregl.Map;
// Step markers
let stepMarkers: maplibregl.Marker[] = [];

const flyToStep = (step: Step | null) => {
  if (map && step) {
    map.flyTo({ center: [step.lng, step.lat], zoom: 16, duration: 2000 });
  }
};

watch(() => tripStore.selectedStep, flyToStep);

onMounted(() => {
  if (!route.params.id || typeof (route.params.id) !== 'string') {
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
    drawSteps();
    if (tripStore.selectedStep) {
      void flyToStep(tripStore.selectedStep);
    }
  });

  // Watch steps changes to redraw markers/layers
  watch(() => tripStore.selectedTrip?.steps?.length, () => {
    if (mapLoaded.value) drawSteps();
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

function clearStepMarkers() {
  stepMarkers.forEach(m => m.remove());
  stepMarkers = [];
}

function drawSteps() {
  if (!map || !tripStore.selectedTrip) return;
  clearStepMarkers();
  // Remove old sources/layers
  if (map.getLayer('steps-arc')) map.removeLayer('steps-arc');
  if (map.getSource('steps-line')) map.removeSource('steps-line');
  if (map.getSource('steps')) map.removeSource('steps');
  const steps = tripStore.selectedTrip.steps || [];
  if (!steps.length) return;
  steps.forEach(step => {
    const markerEl = document.createElement('div');
    markerEl.style.width = '35px';
    markerEl.style.height = '35px';
    markerEl.style.borderRadius = '50%';
    markerEl.style.background = '#cecece';
    markerEl.style.border = '2px solid #fff';
    markerEl.style.boxShadow = '0 2px 6px rgba(0,0,0,0.15)';
    markerEl.style.display = 'flex';
    markerEl.style.alignItems = 'center';
    markerEl.style.justifyContent = 'center';
    markerEl.style.overflow = 'hidden';
    markerEl.style.cursor = 'pointer';

    // Highlight if selected
    if (tripStore.selectedStep && step.id === tripStore.selectedStep.id) {
      markerEl.style.border = '3px solid #1976D2';
      markerEl.style.width = '50px';
      markerEl.style.height = '50px';
      markerEl.style.zIndex = '10';
    }

    let photoUrl = '';
    if (step.coverPhoto) {
      photoUrl = step.coverPhoto.url;
    } else if (step.photos && step.photos.length > 0) {
      photoUrl = (step.photos[0])!.url;
    }

    if (photoUrl) {
      markerEl.innerHTML = `<img src='${photoUrl}' style='width:100%;height:100%;object-fit:cover;border-radius:50%;' alt='photo' />`;
    } else {
      markerEl.innerHTML = `<span style='color:#222;font-size:14px;font-weight:bold;'>${step.name[0] || ''}</span>`;
    }
    markerEl.title = step.name;

    markerEl.addEventListener('click', () => {
      tripStore.setSelectedStep(step);
    });
    const marker = new maplibregl.Marker({ element: markerEl, anchor: 'center' })
      .setLngLat([step.lng, step.lat])
      .addTo(map);
    stepMarkers.push(marker);
  });
  // GeoJSON sources
  const pointFeatures = steps.map(s => ({
    type: 'Feature',
    geometry: { type: 'Point', coordinates: [s.lng, s.lat] },
    properties: { id: s.id, name: s.name }
  }));
  const collection = { type: 'FeatureCollection', features: pointFeatures } as GeoJSON.FeatureCollection;
  map.addSource('steps', { type: 'geojson', data: collection });
  if (pointFeatures.length > 1) {
    const line = {
      type: 'Feature',
      geometry: { type: 'LineString', coordinates: pointFeatures.map(f => f.geometry.coordinates) },
      properties: {}
    } as GeoJSON.Feature<GeoJSON.LineString>;
    map.addSource('steps-line', { type: 'geojson', data: line });
    map.addLayer({
      id: 'steps-arc',
      type: 'line',
      source: 'steps-line',
      layout: { 'line-join': 'round', 'line-cap': 'round' },
      paint: { 'line-color': '#1976D2', 'line-width': 4, 'line-opacity': 0.6 }
    });
  }
}

async function handleAddStep(payload: { name: string; description: string; lng: number; lat: number }) {
  await tripStore.addStep(payload);
  drawSteps();
}
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

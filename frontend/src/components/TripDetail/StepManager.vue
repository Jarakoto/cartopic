<template>
  <div class="q-pa-sm step-manager absolute">
    <div class="row no-wrap q-gutter-sm">
      <q-card v-for="step in steps" :key="step.id" class="step-card q-pa-none" v-show="!stepAddEnabled">
        <q-card-section class="column items-center">
          <div class="q-mb-xs text-bold">{{ step.name }}</div>
        </q-card-section>
      </q-card>
    <q-card :class="['step-card', { 'full-width': stepAddEnabled }]">
      <q-card-section>
        <q-btn v-show="!stepAddEnabled" @click="setStepAddMode(!stepAddEnabled)">
          Ajouter une étape
        </q-btn>
        <div v-if="stepAddEnabled" class="step-adder-form">
          <q-form @submit.prevent="submitStep">
            <q-input v-model="name" label="Nom" dense outlined required />
            <q-input type="textarea" v-model="description" label="Description" dense outlined required />
            <q-input
              :model-value="cursorPosition ? `${cursorPosition.lng.toFixed(3)}, ${cursorPosition.lat.toFixed(3)}` : ''"
              label="Position du curseur"
              dense
              outlined
              :error="positionError"
              :error-message="positionError ? 'Positionner le curseur avec la carte' : ''"
              readonly
              required
            />
            <div class="column q-gutter-sm items-stretch">
              <q-btn type="submit" color="positive" label="Ajouter étape" />
              <q-btn @click="resetNewStepForm" color="negative" label="Annuler" />
            </div>
          </q-form>
        </div>
      </q-card-section>
    </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick } from 'vue';

import { ref, computed, onMounted } from 'vue';
import { useTripStore } from 'stores/trip-store';
import maplibregl from 'maplibre-gl';

const props = defineProps<{ map: maplibregl.Map }>();
const name = ref('');
const description = ref('');
const stepAddEnabled = ref(false);
const trip = useTripStore();
let cursorMarker: maplibregl.Marker | null = null;
let stepMarkers: maplibregl.Marker[] = [];
const cursorPosition = ref<{ lng: number; lat: number } | null>(null);
const positionError = ref(false);
const el = document.createElement('div');

const steps = computed(() => {
  return trip.selectedTrip!.steps ? trip.selectedTrip!.steps : [];
});

onMounted(() => {
  // Scroll to the end of the step-manager div after DOM is rendered
  void nextTick().then(() => {
    const container = document.querySelector('.step-manager');
    if (container) {
      container.scrollLeft = container.scrollWidth;
    }
  });
  // Add a cursor icon marker at the center
  el.style.background = 'none';
  el.style.width = '32px';
  el.style.height = '32px';
  el.style.display = 'flex';
  el.style.alignItems = 'center';
  el.style.justifyContent = 'center';
  el.innerHTML = `<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><line x1="16" y1="4" x2="16" y2="28" stroke="#1976D2" stroke-width="2"/><line x1="4" y1="16" x2="28" y2="16" stroke="#1976D2" stroke-width="2"/></svg>`;
  el.style.visibility = 'hidden'
  const center = props.map.getCenter();
  cursorMarker = new maplibregl.Marker({ element: el, anchor: 'center' })
    .setLngLat([center.lng, center.lat])
    .addTo(props.map);
  props.map.on('move', () => {
    const center = props.map.getCenter();
    if (cursorMarker) {
      cursorMarker.setLngLat([center.lng, center.lat]);
      cursorPosition.value = { lng: center.lng, lat: center.lat };
    }
  });

  // Add steps and arc layers
  addStepsLayers();
  addStepMarkers();
});

function addStepMarkers() {
  // Remove old markers
  stepMarkers.forEach(marker => marker.remove());
  stepMarkers = [];
  const map = props.map;
  const stepArr = steps.value;
  stepArr.forEach(step => {
    const markerEl = document.createElement('div');
    markerEl.style.width = '24px';
    markerEl.style.height = '24px';
    markerEl.style.borderRadius = '50%';
    markerEl.style.background = '#FF9800';
    markerEl.style.border = '2px solid #fff';
    markerEl.style.boxShadow = '0 2px 6px rgba(0,0,0,0.15)';
    markerEl.style.display = 'flex';
    markerEl.style.alignItems = 'center';
    markerEl.style.justifyContent = 'center';
    markerEl.innerHTML = `<span style='color:#222;font-size:14px;font-weight:bold;'>${step.name[0] || ''}</span>`;
    const marker = new maplibregl.Marker({ element: markerEl, anchor: 'center' })
      .setLngLat([step.lng, step.lat])
      .addTo(map);
    stepMarkers.push(marker);
  });
}

function addStepsLayers() {
  const map = props.map;
  // Remove old sources/layers if they exist
  if (map.getLayer('steps-points')) map.removeLayer('steps-points');
  if (map.getSource('steps')) map.removeSource('steps');
  if (map.getLayer('steps-arc')) map.removeLayer('steps-arc');
  if (map.getSource('steps-line')) map.removeSource('steps-line');

  const stepArr = steps.value;
  if (!stepArr.length) return;
  // Points source
  const features: GeoJSON.Feature<GeoJSON.Point>[] = stepArr.map(step => ({
    type: "Feature",
    geometry: {
      type: "Point",
      coordinates: [step.lng, step.lat]
    },
    properties: {
      id: step.id,
      name: step.name
    }
  }));
  const geojson: GeoJSON.FeatureCollection<GeoJSON.Geometry> = {
    type: "FeatureCollection",
    features
  };
  map.addSource('steps', {
    type: 'geojson',
    data: geojson
  });

  // Arc layer
  if (features.length > 1) {
    const lineFeature: GeoJSON.Feature<GeoJSON.LineString> = {
      type: "Feature",
      geometry: {
        type: "LineString",
        coordinates: features.map(f => f.geometry.coordinates)
      },
      properties: {}
    };
    map.addSource('steps-line', {
      type: 'geojson',
      data: lineFeature
    });
    map.addLayer({
      id: 'steps-arc',
      type: 'line',
      source: 'steps-line',
      layout: {
        'line-join': 'round',
        'line-cap': 'round'
      },
      paint: {
        'line-color': '#1976D2',
        'line-width': 4,
        'line-opacity': 0.6
      }
    });
  }
}

function resetNewStepForm() {
  name.value = '';
  cursorPosition.value = null;
  setStepAddMode(false)
}

function setStepAddMode(newValue: boolean) {
  stepAddEnabled.value = newValue;
  el.style.visibility = newValue ? 'visible' : 'hidden';
}

async function submitStep() {
  if (!name.value || !description.value || !cursorPosition.value) return;
  await trip.addStep({
    name: name.value,
    description: description.value,
    lng: cursorPosition.value.lng,
    lat: cursorPosition.value.lat
  });
  resetNewStepForm();
}

</script>

<style lang="scss">
.step-manager {
  bottom: 0;
  background: white;
  right: 0;
  width: 100%;
  overflow-x: scroll;
}
.step-card {
  min-width: 200px;
  max-width: 200px;
  flex-shrink: 0;
  margin-right: 8px;
}
.step-card.full-width {
  min-width: 100%;
  max-width: 100%;
}
</style>
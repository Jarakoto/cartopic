<template>
  <div class="step-manager absolute"
    style="top: 20px; right: 20px; z-index: 10; background: white; padding: 16px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); min-width: 250px;">
    <div class="text-h6 q-mb-md">Étapes</div>
    <q-list bordered>
      <q-item v-for="step in steps" :key="step.id">
        <q-item-section>{{ step.name }}</q-item-section>
      </q-item>
      <q-item v-if="steps.length === 0">
        <q-item-section>Aucune étape</q-item-section>
      </q-item>
    </q-list>
    <q-separator class="q-my-md" />
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
  </div>
</template>

<script setup lang="ts">

import { ref, computed, onMounted } from 'vue';
import { useTripStore } from 'stores/trip-store';
import maplibregl from 'maplibre-gl';

const props = defineProps<{ map: maplibregl.Map }>();
const name = ref('');
const description = ref('');
const stepAddEnabled = ref(false);
const trip = useTripStore();
let cursorMarker: maplibregl.Marker | null = null;
const cursorPosition = ref<{ lng: number; lat: number } | null>(null);
const positionError = ref(false);
const el = document.createElement('div');

const steps = computed(() => {
  return trip.selectedTrip!.steps ? trip.selectedTrip!.steps : [];
});

onMounted(() => {
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
})

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
  width: 400px;
}
</style>
<template>
  <div class="q-pa-sm step-manager absolute">
    <div class="row no-wrap q-gutter-sm">
      <q-card
        v-for="step in steps"
        :key="step.id"
        class="step-card q-pa-none"
        v-show="!stepAddEnabled"
        @click="selectExistingStep(step.id)"
        style="cursor:pointer;"
      >
        <q-card-section class="column items-center">
          <div class="q-mb-xs text-bold">{{ step.name }}</div>
        </q-card-section>
      </q-card>
      <q-card :class="['step-card', { 'full-width': stepAddEnabled }]">
        <q-card-section>
          <q-btn v-show="!stepAddEnabled" @click="toggleAddMode()">
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
import { nextTick, ref, computed, onMounted } from 'vue';
import { useTripStore } from 'stores/trip-store';
import { useRouter } from 'vue-router';

import maplibregl from 'maplibre-gl';

// Accept map from parent again, internalize cursor logic
const props = defineProps<{ map: maplibregl.Map }>();
const emits = defineEmits<{
  (e: 'select-step', id: number): void;
  (e: 'add-step', payload: { name: string; description: string; lng: number; lat: number }): void;
  (e: 'cancel-add'): void;
}>();

const name = ref('');
const description = ref('');
const stepAddEnabled = ref(false);
const trip = useTripStore();
const router = useRouter();
const positionError = ref(false);
// Cursor marker elements
let cursorMarker: maplibregl.Marker | null = null;
let cursorEl: HTMLDivElement | null = null;
const cursorPosition = ref<{ lng: number; lat: number } | null>(null);

const steps = computed(() => trip.selectedTrip?.steps || []);

function selectExistingStep(stepId: number) {
  emits('select-step', stepId);
  if (trip.selectedTrip) {
    void router.push(`/trips/${trip.selectedTrip.id}/steps/${stepId}`);
  }
}

function toggleAddMode() {
  setStepAddMode(!stepAddEnabled.value);
}

onMounted(() => {
  void nextTick().then(() => {
    const container = document.querySelector('.step-manager');
    if (container) container.scrollLeft = container.scrollWidth;
  });
  initCursorMarker();
  props.map.on('move', () => {
    if (!cursorMarker) return;
    const center = props.map.getCenter();
    cursorMarker.setLngLat([center.lng, center.lat]);
    cursorPosition.value = { lng: center.lng, lat: center.lat };
  });
});

function resetNewStepForm() {
  name.value = '';
  description.value = '';
  setStepAddMode(false);
  emits('cancel-add');
}

function setStepAddMode(newValue: boolean) {
  stepAddEnabled.value = newValue;
  toggleCursorVisibility(newValue);
  if (newValue && !cursorPosition.value) positionError.value = true; else positionError.value = false;
}

function initCursorMarker() {
  cursorEl = document.createElement('div');
  cursorEl.style.background = 'none';
  cursorEl.style.width = '32px';
  cursorEl.style.height = '32px';
  cursorEl.style.display = 'flex';
  cursorEl.style.alignItems = 'center';
  cursorEl.style.justifyContent = 'center';
  cursorEl.innerHTML = `<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><line x1="16" y1="4" x2="16" y2="28" stroke="#1976D2" stroke-width="2"/><line x1="4" y1="16" x2="28" y2="16" stroke="#1976D2" stroke-width="2"/></svg>`;
  cursorEl.style.visibility = 'hidden';
  const center = props.map.getCenter();
  cursorMarker = new maplibregl.Marker({ element: cursorEl, anchor: 'center' })
    .setLngLat([center.lng, center.lat])
    .addTo(props.map);
  cursorPosition.value = { lng: center.lng, lat: center.lat };
}

function toggleCursorVisibility(visible: boolean) {
  if (cursorEl) cursorEl.style.visibility = visible ? 'visible' : 'hidden';
}

function submitStep() {
  if (!name.value || !description.value || !cursorPosition.value) {
    positionError.value = !cursorPosition.value;
    return;
  }
  emits('add-step', {
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
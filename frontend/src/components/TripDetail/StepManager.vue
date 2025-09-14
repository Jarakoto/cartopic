<template>
  <div class="q-pa-sm q-pr-none step-manager absolute-bottom flex items-center justify-start full-width">
    <div class="cards-nav-wrapper row items-center no-wrap full-width relative q-gutter-sm">
      <q-btn class="desktop-nav-btn nav-left" size="md" flat icon="chevron_left" v-show="canShowNav"
        :disable="!canGoPrev" @click="focusByDelta(-1)" />
      <div class="cards-row-wrapper col-grow">
        <div class="step-cards-row flex row no-wrap q-gutter-md q-py-none"
          v-touch-swipe.mouse.horizontal.prevent="handleSwipe"
          style="overflow-x: auto; touch-action: pan-y; -webkit-overflow-scrolling: touch;">
          <q-card v-for="(step) in steps" :key="step.id" class="step-card cursor-pointer"
            :class="{ focused: step.id === prefocusedStepId }" :data-step-id="step.id" @click="selectStep(step)" flat
            bordered>
            <q-card-section>
              <div class="text-bold q-mb-xs">{{ step.name }}</div>
              <div class="q-mb-xs text-caption text-grey-7 align-center flex">{{ new
                Date(step.startedAt!).toLocaleDateString(undefined, {
                  month:
                    '2-digit', day: '2-digit'
                }) }}
                <template v-if="step.endedAt">
                  &#8594;
                  {{ new Date(step.endedAt).toLocaleDateString(undefined, {
                    month: '2-digit', day: '2-digit'
                  }) }}
                </template>
              </div>
            </q-card-section>
          </q-card>
          <div v-if="stepAddEnabled" class="step-card full-width q-pa-md">
            <q-form @submit.prevent="submitStep">
              <q-input v-model="name" label="Nom" dense outlined required />
              <q-input type="textarea" v-model="description" label="Description" dense outlined required />
              <q-input
                :model-value="cursorPosition ? `${cursorPosition.lng.toFixed(3)}, ${cursorPosition.lat.toFixed(3)}` : ''"
                label="Position du curseur" dense outlined :error="positionError"
                :error-message="positionError ? 'Positionner le curseur avec la carte' : ''" readonly required />
              <div class="column q-gutter-sm items-stretch">
                <q-btn type="submit" color="positive" label="Ajouter étape" />
                <q-btn @click="resetNewStepForm" color="negative" label="Annuler" />
              </div>
            </q-form>
          </div>
          <div v-if="!stepAddEnabled" class="step-card q-pa-md">
            <q-btn @click="toggleAddMode()">
              Ajouter une étape
            </q-btn>
          </div>
        </div>
      </div>
      <q-btn class="desktop-nav-btn nav-right" size="md" unelevated icon="chevron_right" v-show="canShowNav"
        :disable="!canGoNext" @click="focusByDelta(1)" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref, computed, onMounted, watch } from 'vue';
import { type Step, useTripStore } from 'stores/trip-store';
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
const prefocusedStep = ref<Step | null>(null);

const prefocusedStepId = computed(() => prefocusedStep.value ? prefocusedStep.value.id : null);

const isDesktop = ref(typeof window !== 'undefined' ? window.innerWidth > 600 : true);
if (typeof window !== 'undefined') {
  window.addEventListener('resize', () => { isDesktop.value = window.innerWidth > 600; });
}
const canGoPrev = computed(() => {
  if (!steps.value.length) return false;
  const idx = steps.value.findIndex(s => s.id === prefocusedStepId.value);
  return idx > 0;
});
const canGoNext = computed(() => {
  if (!steps.value.length) return false;
  const idx = steps.value.findIndex(s => s.id === prefocusedStepId.value);
  return idx !== -1 && idx < steps.value.length - 1;
});
const canShowNav = computed(() => isDesktop.value && steps.value.length > 1);

function selectStep({ id: stepId }: { id: number }) {
  emits('select-step', stepId);
  if (trip.selectedTrip) {
    void router.push(`/trips/${trip.selectedTrip.id}/steps/${stepId}`);
  }
}

function centerFocusedCard() {
  if (prefocusedStepId.value == null) return;
  const container = document.querySelector('.step-cards-row');
  const card = document.querySelector(`.step-card[data-step-id="${prefocusedStepId.value}"]`);
  if (!container || !card) return;
  const cRect = container.getBoundingClientRect();
  const cardRect = card.getBoundingClientRect();
  const offset = (cardRect.left + cardRect.width / 2) - (cRect.left + cRect.width / 2);
  (container as HTMLElement).scrollBy({ left: offset, behavior: 'smooth' });
  props.map.flyTo({ center: [prefocusedStep.value!.lng, prefocusedStep.value!.lat], zoom: 12, duration: 2000 });
}

function focusByDelta(delta: number) {
  if (!steps.value.length) return;
  const idx = steps.value.findIndex(s => s.id === prefocusedStepId.value);
  const currentIdx = idx === -1 ? 0 : idx;
  let nextIdx = currentIdx + delta;
  if (nextIdx < 0) nextIdx = 0;
  if (nextIdx >= steps.value.length) nextIdx = steps.value.length - 1;
  const next = steps.value[nextIdx];
  if (next) {
    prefocusedStep.value = next;
    void nextTick(() => centerFocusedCard());
  }
}

interface SwipeDetails {
  evt?: Event;
  touch?: boolean;
  mouse?: boolean;
  direction?: 'left' | 'right' | 'up' | 'down';
  duration?: number;
  distance?: { x?: number; y?: number };
}

function handleSwipe(details: SwipeDetails) {
  if (!details.direction) return;
  if (details.direction === 'left') {
    focusByDelta(1);
  } else if (details.direction === 'right') {
    focusByDelta(-1);
  }
}

function toggleAddMode() {
  setStepAddMode(!stepAddEnabled.value);
}

onMounted(() => {
  // Prefocus last step
  if (steps.value.length > 0) {
    const last = steps.value[steps.value.length - 1];
    if (last) {
      prefocusedStep.value = last;
      void nextTick(() => centerFocusedCard());
    }
  }
  void nextTick().then(() => {
    const container = document.querySelector('.step-manager');
    if (container) (container as HTMLElement).scrollLeft = (container as HTMLElement).scrollWidth;
  });
  initCursorMarker();
  props.map.on('move', () => {
    if (!cursorMarker) return;
    const center = props.map.getCenter();
    cursorMarker.setLngLat([center.lng, center.lat]);
    cursorPosition.value = { lng: center.lng, lat: center.lat };
  });
});

// If steps load asynchronously later, focus last step only if none focused yet
watch(steps, (newSteps) => {
  if (!newSteps || !newSteps.length) return;
  if (prefocusedStepId.value == null) {
    const last = newSteps[newSteps.length - 1];
    if (last) {
      prefocusedStep.value = last;
      void nextTick(() => centerFocusedCard());
    }
  }
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
  left: 0;
  right: 0;


  /* Gradient edge overlays to hint horizontal overflow */
  /* Removed gradient edges (no overlay) */

  .cards-nav-wrapper {
    position: relative;
  }

  .cards-row-wrapper {
    flex: 1 1 auto;
    min-width: 0;
  }

  .desktop-nav-btn:disabled {
    opacity: 0.25;
  }

  /* Increase hit target area while keeping circular visual */
  .desktop-nav-btn.nav-left,
  .desktop-nav-btn.nav-right {
    --btn-size: 54px;
    width: var(--btn-size);
    height: var(--btn-size);
    display: flex;
    align-items: center;
    justify-content: center;
  }


}

/* Hide horizontal scrollbar while keeping scroll functionality */
.step-cards-row {
  scrollbar-width: none;
  /* Firefox */
  -ms-overflow-style: none;
  /* IE/Edge */
}

.step-cards-row::-webkit-scrollbar {
  width: 0;
  height: 0;
}

.desktop-nav-btn:disabled {
  opacity: 0.3;
}

// Only keep minimal custom styles for card sizing
.step-card {
  min-width: 200px;
  max-width: 200px;
  flex-shrink: 0;
}

.step-card.full-width {
  min-width: 100%;
  max-width: 100%;
}

.step-card {
  transition: border 0.2s, box-shadow 0.2s, transform 0.2s;
}

.step-card.focused {
  border: 2px solid #1976D2;
  box-shadow: 0 4px 14px rgba(25, 118, 210, 0.25);
  z-index: 1;
}
</style>

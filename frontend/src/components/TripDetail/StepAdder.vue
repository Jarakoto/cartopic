
<template>
  <div class="step-adder-form absolute" style="top: 20px; right: 20px; z-index: 10; background: white; padding: 16px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <q-form @submit.prevent="submitStep">
      <q-input v-model="stepName" label="Nom de l'étape" dense outlined required />
      <div class="q-mt-sm">
        <q-btn type="submit" color="primary" label="Ajouter à la position du curseur" />
      </div>
    </q-form>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';

const props = defineProps<{ map: maplibregl.Map }>();
const stepName = ref('');

function submitStep() {
  if (!props.map) return;
  const center = props.map.getCenter();
  // Here you would call an API or store action to create the step
  alert(`Step: ${stepName.value}\nLng: ${center.lng}\nLat: ${center.lat}`);
  stepName.value = '';
}
</script>
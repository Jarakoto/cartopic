<template>
  <SwipePanel>
    <div class="text-h4">{{ step!.name }}</div>
    <div class="q-mt-md">{{ step!.description }}</div>
  </SwipePanel>
</template>

<script lang="ts" setup>
import SwipePanel from '../Generic/SwipePanel.vue';
import { useTripStore } from 'stores/trip-store';

const tripStore = useTripStore();
const step = tripStore.selectedStep;

</script>

<style lang="scss">

</style>
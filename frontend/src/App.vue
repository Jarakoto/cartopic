<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted, getCurrentInstance } from 'vue';
import { useTripStore } from 'stores/trip-store';

const tripStore = useTripStore();

onMounted(async () => {
  const instance = getCurrentInstance();
  if (instance && instance.proxy) {
    await tripStore.fetchTrips(instance.proxy.$api);
  }
});
</script>

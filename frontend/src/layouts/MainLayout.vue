<template>
  <q-layout view="lHh Lpr lFf">
    <q-header v-if="false" elevated>
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" bordered>
      <q-list>
        <q-item-label header>Voyages</q-item-label>
        <q-item v-for="trip in tripStore.trips" :key="trip.id" clickable tag="router-link" :to="`/trips/${trip.id}`">
          <q-item-section>{{ trip.name }}</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useTripStore } from 'stores/trip-store';

const leftDrawerOpen = ref(false);
const tripStore = useTripStore();

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>

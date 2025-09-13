<template>
  <q-page class="q-pa-none">
    <div id="map" class="fit"></div>
  </q-page>
</template>

<script setup lang="ts">

import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

import { onMounted } from 'vue';

onMounted(() => {
  new maplibregl.Map({
    container: 'map',
    style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
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

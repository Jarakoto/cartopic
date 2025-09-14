<template>
  <SwipePanel>
  <div class="step-detail-wrapper">
    <div class="title-row">
      <div class="title text-h5 text-primary ellipsis">{{ step?.name }}</div>
    </div>
    <div class="tabs-area">
      <q-tabs v-model="tab" dense class="text-grey" active-color="primary" align="left" inline-label narrow-indicator indicator-color="primary">
        <q-tab name="description" icon="description" title="Description" label="Journal" />
        <q-tab name="photos" icon="photo" title="Photos" label="Photos" />
      </q-tabs>
      <q-separator />
      <q-tab-panels v-model="tab" animated class="panels">
        <q-tab-panel name="description" class="q-pl-none">
          <div class="desc-scroll">
            <p class="desc-text">{{ step?.description || '—' }}</p>
          </div>
        </q-tab-panel>
        <q-tab-panel name="photos" class="q-px-none panel-col">
          <PhotoViewer :photos="photos" :loading="loadingPhotos" />
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
  </SwipePanel>
</template>

<script lang="ts" setup>
import SwipePanel from '../Generic/SwipePanel.vue';
import { useTripStore } from 'stores/trip-store';
import { computed, ref } from 'vue';
import PhotoViewer from './PhotoViewer.vue';

const tripStore = useTripStore();
const step = computed(() => tripStore.selectedStep);
const photos = computed(() => step.value?.photos ?? []);
const loadingPhotos = ref(false);
const tab = ref<'description' | 'photos'>('description');

// Photo logic moved into PhotoViewer component

</script>
<style lang="sass">
.step-detail-wrapper
  display: flex
  flex-direction: column
  height: 100%
  width: 100%
  min-height: 0

@media (min-width: 920px)
  .step-detail-wrapper
    max-width: 900px
    margin: 0 auto
    width: 100%

.title-row
  flex: 0 0 auto
  padding: 4px 0 8px
  min-width: 0

.title
  font-weight: 600
  line-height: 1.2
  width: 100%

.tabs-area
  flex: 1 1 auto
  display: flex
  flex-direction: column
  min-height: 0

.panels
  flex: 1 1 auto
  display: flex
  flex-direction: column
  min-height: 0

.panels > .q-tab-panel
  flex: 1 1 auto
  display: flex
  flex-direction: column
  min-height: 0

.desc-scroll
  flex: 1 1 auto
  overflow-y: auto
  font-family: inherit
  white-space: pre-line
  min-height: 0

.desc-text
  margin: 0
  font-size: 0.875rem
  line-height: 1.35
  text-align: justify

// Utility
.panel-col
  display: flex
  flex-direction: column
  flex: 1 1 auto
  min-height: 0
</style>
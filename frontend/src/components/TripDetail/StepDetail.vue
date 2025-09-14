<template>
  <SwipePanel>
    <div class="column q-gutter-md">
      <div>
        <div class="text-h5 text-primary">{{ step?.name }}</div>
        <div class="text-body2 q-mt-xs" style="white-space: pre-line;">{{ step?.description }}</div>
      </div>
      <div>
        <q-img
          v-if="step?.coverPhoto?.url"
          :src="step.coverPhoto.url"
          class="rounded-borders shadow-1"
          :ratio="16/9"
          spinner-color="primary"
        >
          <template #error>
            <div class="absolute-full flex flex-center bg-grey-3 text-grey-6">Image indisponible</div>
          </template>
        </q-img>
      </div>
    </div>
  </SwipePanel>
</template>

<script lang="ts" setup>
import SwipePanel from '../Generic/SwipePanel.vue';
import { useTripStore } from 'stores/trip-store';
import { computed } from 'vue';

const tripStore = useTripStore();
const step = computed(() => tripStore.selectedStep);
</script>

<style lang="scss">
.placeholder {
  height: 180px;
  border: 1px dashed #ccc;
  border-radius: 8px;
  background: #fafafa;
}
</style>
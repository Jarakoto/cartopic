<template>
  <SwipePanel>
    <div class="step-detail-wrapper column q-gutter-md">
      <div>
        <div class="text-h5 text-primary">{{ step?.name }}</div>
        <div class="text-body2 q-mt-xs" style="white-space: pre-line;">{{ step?.description }}</div>
      </div>
      <div v-if="loadingPhotos" class="flex flex-center q-my-md">
        <q-spinner color="primary" size="2em" />
      </div>
      <div v-else>
        <q-carousel
          v-if="photos.length"
          v-model="slide"
          animated
          swipeable
          arrows
          infinite
          height="290px"
          class="bg-dark text-white shadow-2"
        >
          <q-carousel-slide
            v-for="p in photos"
            :key="p.id"
            :name="p.id"
            class="column no-wrap justify-end carousel-slide"
          >
            <div class="image-stage">
              <img :src="p.url" :alt="p.name || 'photo'" class="adaptive-photo" @error="onImgErr($event)" />
            </div>
            <div class="caption absolute-bottom custom-caption q-pa-sm" v-if="p.name || p.description">
              <div class="text-subtitle2" v-if="p.name">{{ p.name }}</div>
              <div class="text-caption" v-if="p.description">{{ p.description }}</div>
            </div>
          </q-carousel-slide>
        </q-carousel>
        <div v-else class="placeholder flex flex-center column text-grey-6 q-my-md">
          <q-icon name="photo_library" size="48px" />
          <div class="text-caption q-mt-xs">Aucune photo pour cette étape</div>
        </div>
      </div>
    </div>
  </SwipePanel>
</template>

<script lang="ts" setup>
import SwipePanel from '../Generic/SwipePanel.vue';
import { useTripStore } from 'stores/trip-store';
import { computed, ref, watch, onMounted } from 'vue';

const tripStore = useTripStore();
const step = computed(() => tripStore.selectedStep);
const photos = computed(() => step.value?.photos ?? []);
const loadingPhotos = ref(false);
const slide = ref<number | null>(null);

function initFirstSlide() {
  if (slide.value === null && photos.value.length && photos.value[0]) {
    slide.value = photos.value[0].id;
  }
}

onMounted(() => {
  initFirstSlide();
});

watch(photos, () => {
  // If no current slide or current slide id no longer exists, reset to first
  if (!photos.value.length) {
    slide.value = null;
    return;
  }
  const exists = photos.value.some(p => p.id === slide.value);
  if (!exists && photos.value[0]) {
    slide.value = photos.value[0].id;
  }
});

function onImgErr(e: Event) {
  const el = e.target as HTMLImageElement;
  el.style.opacity = '0.3';
  el.alt = 'Erreur chargement';
}

</script>

<style lang="sass">
.custom-caption
  text-align: center
  padding: 12px
  color: white
  background-color: rgba(0, 0, 0, .3)
.image-stage
  position: absolute
  top: 0
  left: 0
  width: 100%
  height: 100%
  display: flex
  justify-content: center
  align-items: center
  background: #000

.adaptive-photo
  max-width: 100%
  max-height: 100%
  width: auto
  height: auto
  object-fit: contain
  transition: opacity .25s ease
.step-detail-wrapper
  width: 100%
  max-width: 100%
  margin: 0 auto

@media (min-width: 920px)
  .step-detail-wrapper
    max-width: 900px
</style>
<template>
  <div class="photo-viewer q-pa-xs">
    <div v-if="loading" class="flex flex-center" style="min-height:120px;">
      <q-spinner color="primary" size="2em" />
    </div>
    <div v-else>
      <div v-if="photos.length" class="row q-col-gutter-md">
        <div v-for="p in photos" :key="p.id" class="col-12 col-md-4">
          <q-card flat bordered class="photo-card">
            <q-img
              :src="p.url"
              :alt="p.name || 'photo'"
              fit="cover"
              spinner-color="primary"
              @error="onImgErr($event)"
            />
            <q-card-section v-if="p.name || p.description" class="q-pt-sm q-pb-sm">
              <div class="text-subtitle2" v-if="p.name">{{ p.name }}</div>
              <div class="text-caption text-grey-7" style="white-space:pre-line" v-if="p.description">{{ p.description }}</div>
            </q-card-section>
          </q-card>
        </div>
      </div>
      <div v-else class="flex flex-center column text-grey-6" style="min-height:120px;">
        <q-icon name="photo_library" size="48px" />
        <div class="text-caption q-mt-xs">Aucune photo pour cette étape</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { QSpinner, QIcon, QCard, QImg, QCardSection } from 'quasar';
import { type Photo } from 'stores/trip-store';

interface Props {
  photos: Photo[]
  loading?: boolean
}

const props = defineProps<Props>();

function onImgErr(e: Event) {
  const el = e.target as HTMLImageElement;
  el.style.opacity = '0.3';
  el.alt = 'Erreur chargement';
}

const loading = computed(() => props.loading === true);
</script>

<style lang="sass" scoped>
.photo-viewer
  width: 100%
  display: flex
  flex-direction: column
  gap: 12px

.photo-card :deep(.q-img)
  border-bottom: 1px solid rgba(0,0,0,0.05)

</style>

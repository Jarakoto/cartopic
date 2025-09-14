<template>
  <q-dialog v-model="showModal">
    <q-card class="q-py-md" style="width:80vw; height:90vh; box-shadow:none; border-radius:8px;">
      <q-card-section class="flex flex-center" style="padding:0; height:calc(90vh - 56px);">
        <q-img :src="modalUrl" fit="contain" style="width:80vw; height:100%;" />
      </q-card-section>
      <q-card-actions align="right" style="background:transparent; position:absolute; top:0; right:0; width:100%;">
        <q-btn icon="close" color="grey" flat round @click="showModal = false" aria-label="Fermer"
          style="margin:16px;" />
      </q-card-actions>
    </q-card>
  </q-dialog>
  <div class="photo-viewer q-pa-xs">
    <div v-if="loading" class="flex flex-center" style="min-height:120px;">
      <q-spinner color="primary" size="2em" />
    </div>
    <div v-else>
      <div v-if="photos.length" class="gallery-row" style="display:flex; gap:16px;">
        <div v-for="(col, i) in photoColumns" :key="i" class="gallery-col"
          style="flex:1; display:flex; flex-direction:column; gap:16px;">
          <q-card v-for="p in col" :key="p.id" flat bordered class="photo-card">
            <div style="position:relative;">
              <q-img :src="p.url" :alt="p.name || 'photo'" fit="cover" spinner-color="primary"
                @error="onImgErr($event)" />
              <q-btn icon="fullscreen" size="sm" round flat color="white" class="absolute-top-right q-ma-xs"
                @click="openFullscreen(p.url)" aria-label="Agrandir" />
            </div>
            <q-card-section v-if="p.name || p.description" class="q-pt-sm q-pb-sm">
              <div class="text-subtitle2" v-if="p.name">{{ p.name }}</div>
              <div class="text-caption text-grey-7" style="white-space:pre-line" v-if="p.description">{{ p.description
              }}</div>
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
import { useQuasar } from 'quasar';
const $q = useQuasar();
const photoColumns = computed(() => {
  const arr = props.photos ?? [];
  if ($q.screen.lt.md) {
    // Mobile: single column
    return [arr];
  } else {
    // Desktop: 3 columns
    const cols: Photo[][] = [[], [], []];
    arr.forEach((p, idx) => {
      (cols[idx % 3]!).push(p);
    });
    return cols;
  }
});
import { ref } from 'vue';
const showModal = ref(false);
const modalUrl = ref('');
import { computed } from 'vue';
import { QSpinner, QIcon, QCard, QImg, QCardSection, QBtn } from 'quasar';

function openFullscreen(url: string) {
  modalUrl.value = url;
  showModal.value = true;
}
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

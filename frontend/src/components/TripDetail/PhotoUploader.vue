<template>
  <div class="photo-uploader q-pa-sm">
    <q-form @submit.prevent="startUpload" class="row q-col-gutter-md items-end">
      <div class="col-12">
        <q-input v-model="name" label="Titre (optionnel)" dense outlined clearable />
      </div>
      <div class="col-12">
        <q-input v-model="description" type="textarea" label="Description (optionnel)" dense outlined clearable />
      </div>
      <div class="col-12">
        <q-file v-model="file" label="Photo" type="file" :disable="uploading" accept="image/*" dense outlined clearable
          use-chips @rejected="onRejected" />
      </div>
      <div class="col-12 col-md-2">
        <q-btn :disable="!file || uploading" color="primary" label="Uploader" type="submit" unelevated />
      </div>
      <div class="col-12 col-md-2" v-if="uploading">
        <q-linear-progress :value="progressRatio" color="primary" rounded size="10px" />
        <div class="text-caption text-grey-7 q-mt-xs">{{ progress }}%</div>
      </div>
    </q-form>

    <div v-if="error" class="q-mt-sm text-negative text-caption">{{ error }}</div>
    <div v-if="success" class="q-mt-sm text-positive text-caption">Photo ajoutée</div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { api } from 'boot/axios';
import { type Photo, useTripStore } from 'stores/trip-store';
import { QForm, QFile, QInput, QBtn, QLinearProgress } from 'quasar';
import { AxiosError } from 'axios';

const emit = defineEmits<{ (e: 'uploaded', photo: Photo): void }>();

const file = ref<File | null>(null);
const name = ref('');
const description = ref('');
const uploading = ref(false);
const progress = ref(0);
const error = ref<string | null>(null);
const success = ref(false);

const tripStore = useTripStore();
const step = computed(() => tripStore.selectedStep);
const trip = computed(() => tripStore.selectedTrip);

const progressRatio = computed(() => progress.value / 100);

function resetState() {
  uploading.value = false;
  progress.value = 0;
  success.value = false;
  error.value = null;
}

function onRejected() {
  error.value = 'Fichier invalide';
}

async function startUpload() {
  if (!file.value || !step.value || !trip.value) return;
  resetState();
  uploading.value = true;
  error.value = null;
  success.value = false;

  const form = new FormData();
  form.append('file', file.value); // assuming backend expects 'file'
  console.log(name.value, description.value);
  if (name.value) form.append('name', name.value);
  if (description.value) form.append('description', description.value);

  try {
    const url = `/trips/${trip.value.id}/steps/${step.value.id}/photos/upload`;
    const response = await api.post(url, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (evt) => {
        if (evt.total) {
          progress.value = Math.round((evt.loaded / evt.total) * 100);
        }
      }
    });
    const photo = response.data; // assuming backend returns the created photo
    success.value = true;
    emit('uploaded', photo);
    // Reset file for next upload
    file.value = null;
    name.value = '';
    description.value = '';
    setTimeout(() => { success.value = false; }, 2500);
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      error.value = e.response?.data?.detail || 'Erreur upload';
    } else {
      error.value = 'Erreur upload';
    }
  } finally {
    uploading.value = false;
  }
}
</script>

<style lang="sass" scoped>
.photo-uploader
  background: rgba(0,0,0,0.02)
  border: 1px dashed rgba(0,0,0,0.15)
  border-radius: 6px
</style>

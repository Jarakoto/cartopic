<template>
  <q-page class="q-pa-md">
    <q-card>
      <q-card-section>
        <div class="text-h6">Trips</div>
        <q-list>
          <q-item v-for="trip in trips" :key="trip.id">
            <q-item-section>
              <div class="text-bold">{{ trip.name }}</div>
              <q-list>
                <q-item v-for="step in trip.steps" :key="step.id">
                  <q-item-section>{{ step.name }}</q-item-section>
                </q-item>
              </q-list>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getCurrentInstance } from 'vue';

interface Step {
  id: number;
  name: string;
}

interface Trip {
  id: number;
  name: string;
  steps: Step[];
}

const trips = ref<Trip[]>([]);



onMounted(async () => {
  const instance = getCurrentInstance();
  if (instance && instance.proxy) {
    const response = await instance.proxy.$api.get('/trips');
    trips.value = response.data;
  }
});
</script>

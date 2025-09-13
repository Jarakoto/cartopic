<template>
<div id="q-app">
  <div class="q-pa-md">
    <q-card
      class="slide-drawer slide-drawer--bottom text-white fixed-bottom column no-wrap"
      :class="`slide-drawer--open-${drawerMode}`"
      :style="drawerStyle"
    >
      <q-card-section class="slide-drawer__handler--horizontal row flex-center q-pa-sm q-gutter-x-md" v-touch-pan.mouse.vertical="slideDrawer">
        <div class="cursor-pointer" @click="cycleDrawer"></div>
      </q-card-section>
        <slot></slot>
    </q-card>
  </div>
</div>
</template>

<script lang="ts" setup>
import { ref, computed, onBeforeUnmount, nextTick } from 'vue'
import { useQuasar } from 'quasar'

const drawerMinHeight = 200
const drawerTopOffset = 100
const drawerOpenRatioHalf = 50

const $q = useQuasar()
const drawerPos = ref(drawerMinHeight)
let animateTimeout: ReturnType<typeof setTimeout> | undefined = undefined

const drawerMaxHeight = computed(() => {
  return Math.max(0, $q.screen.height - drawerTopOffset)
})

const drawerOpenRatio = computed(() => {
  return Math.round(Math.max(0, drawerPos.value - drawerMinHeight) / Math.max(1, drawerMaxHeight.value - drawerMinHeight) * 100)
})

const drawerStyle = computed(() => {
  return {
    height: `${drawerMaxHeight.value}px`,
    transform: `translateY(${-drawerPos.value}px)`
  }
})

const drawerMode = computed(() => {
  return drawerOpenRatio.value > drawerOpenRatioHalf ? 'full' : 'handler'
})

function slideDrawer(ev: {
  direction?: 'up' | 'down' | 'left' | 'right';
  delta?: { x?: number; y?: number };
  isFinal?: boolean;
}) {
  const direction = ev.direction ?? 'up'
  const deltaY = ev.delta?.y ?? 0
  const isFinal = ev.isFinal ?? false
  drawerPos.value = Math.max(drawerMinHeight, Math.min(drawerMaxHeight.value, drawerPos.value - deltaY))
  if (isFinal) {
    void nextTick().then(() => {
      const targetHeight = direction === 'up'
        ? drawerMaxHeight.value
        : drawerMinHeight
      animateDrawerTo(targetHeight)
    })
  }
}

function cycleDrawer() {
  const targetHeight = drawerMode.value === 'handler'
    ? drawerMaxHeight.value : drawerMinHeight
  animateDrawerTo(targetHeight)
}

function animateDrawerTo(height: number) {
  clearTimeout(animateTimeout)
  const diff = height - drawerPos.value
  if (diff !== 0) {
    drawerPos.value += Math.abs(diff) < 2 ? diff : Math.round(diff / 2)
    animateTimeout = setTimeout(() => {
      animateDrawerTo(height)
    }, 30)
  }
}

onBeforeUnmount(() => {
  clearTimeout(animateTimeout)
})
</script>

<style lang="sass">
// Only disable overscroll and touch-action when finger is on the panel
.slide-drawer
  overscroll-behavior: contain
  touch-action: none
  &--bottom
    border-bottom-left-radius: 0
    border-bottom-right-radius: 0
    background-color: #333
    background-image: radial-gradient(circle, rgba(0, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.4) 100%)
    bottom: unset
    top: 100%
    transition: background-color 0.3s ease-in-out

    > div:last-child,
    > img:last-child
      border-bottom-left-radius: 0
      border-bottom-right-radius: 0
    
    // Removed half state background
    
    &.slide-drawer--open-full
      background-color: #01884a
  &__handler
    &--horizontal
      cursor: grab
      > div
        width: 60px
        height: 8px
        border-radius: 4px
        background-color: rgba(200, 200, 200, 0.7)
</style>
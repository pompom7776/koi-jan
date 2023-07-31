<script setup>
const props = defineProps(["scale"]);
const width = 25 * props.scale;
const height = 150 * props.scale;
const borderRadius = 32 * props.scale;
const dotSize = 12 * props.scale;
</script>
<template>
  <div
    :style="{
      width: `${width}px`,
      height: `${height}px`,
      borderRadius: `${borderRadius}px`,
    }"
    class="riichi-stick"
  >
    <div
      :style="{ width: `${dotSize}px`, height: `${dotSize}px` }"
      class="dot"
    ></div>
  </div>
</template>

<style scoped>
.riichi-stick {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #000000;
  position: relative;
}

.dot {
  border-radius: 50%;
  background-color: #ff0000;
}
</style>

<script setup>
const props = defineProps(["scale"]);
const width = 25 * props.scale;
const height = 150 * props.scale;
const borderRadius = 32 * props.scale;
const dotSize = 4 * props.scale;
</script>

<template>
  <div
    :style="{
      width: `${width}px`,
      height: `${height}px`,
      borderRadius: `${borderRadius}px`,
    }"
    class="point-stick"
  >
    <div :style="{ gap: `${dotSize}px` }" class="dots-container">
      <div
        :style="{ width: `${dotSize}px`, height: `${dotSize}px` }"
        class="dot"
      ></div>
      <div
        :style="{ width: `${dotSize}px`, height: `${dotSize}px` }"
        class="dot"
      ></div>
      <div
        :style="{ width: `${dotSize}px`, height: `${dotSize}px` }"
        class="dot"
      ></div>
      <div
        :style="{ width: `${dotSize}px`, height: `${dotSize}px` }"
        class="dot"
      ></div>
      <div
        :style="{ width: `${dotSize}px`, height: `${dotSize}px` }"
        class="dot"
      ></div>
      <div
        :style="{ width: `${dotSize}px`, height: `${dotSize}px` }"
        class="dot"
      ></div>
      <div
        :style="{ width: `${dotSize}px`, height: `${dotSize}px` }"
        class="dot"
      ></div>
      <div
        :style="{ width: `${dotSize}px`, height: `${dotSize}px` }"
        class="dot"
      ></div>
    </div>
  </div>
</template>

<style scoped>
.point-stick {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #000000;
  position: relative;
}

.dots-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(4, 1fr);
  width: 50%;
  height: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.dot {
  border-radius: 50%;
  background-color: #000000;
  justify-self: center;
  align-self: center;
}
</style>

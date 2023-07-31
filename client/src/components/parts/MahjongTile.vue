<script setup>
import { computed, ref } from "vue";

const props = defineProps(["scale", "tile", "rotate"]);
const tile = props.tile;
const scale = props.scale;
const rotate = props.rotate;

const size = computed(() => ({
  width: `${4.3 * scale}vw`,
  height: `${5 * scale}vw`,
}));

const getStyle = computed(() => {
  var margin_width = 0;
  var margin_bottom = 0;
  if (rotate == 90 || rotate == 270) {
    margin_width = 8 * scale;
    margin_bottom = 8 * scale;
  }
  return {
    ...size.value,
    transform: `rotate(${rotate}deg)`,
    "margin-left": `${margin_width}px`,
    "margin-right": `${margin_width}px`,
    "margin-bottom": `-${margin_bottom}px`,
  };
});

const getTileClass = (tile) => {
  const classes = ["tile"];
  if (tile === "-") {
    classes.push("back-tile");
  }
  return classes.join(" ");
};

const tileStyle = ref({});
const handleTileHover = (hovered) => {
  if (hovered) {
    tileStyle.value = {
      transform: `rotate(${rotate}deg) translateY(-10px)`,
      transition: "0.3s",
      cursor: "pointer",
    };
  } else {
    tileStyle.value = {
      transform: `rotate(${rotate}deg)`,
      transition: "0.3s",
      cursor: "pointer",
    };
  }
};
const getImagePath = (tile) => {
  return `/parts/${tile}.png`;
};
</script>
<template>
  <div v-if="tile === '-'" :class="getTileClass(tile)" :style="{ ...getStyle, ...tileStyle }"
    @mouseover="handleTileHover(true)" @mouseleave="handleTileHover(false)">
    {{ tile }}
  </div>
  <div v-else :class="getTileClass(tile)" :style="{ ...getStyle, ...tileStyle }" @mouseover="handleTileHover(true)"
    @mouseleave="handleTileHover(false)">
    <img :style="{ ...getStyle }" :src="getImagePath(tile)" />
  </div>
</template>
<style>
.tile {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  border: 1px solid black;
  font-weight: bold;
  writing-mode: vertical-rl;
  background-color: white;
  color: black;
}

.back-tile {
  pointer-events: none;
  color: orange;
  background-color: orange;
}
</style>

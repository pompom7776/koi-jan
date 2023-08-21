<script setup>
import { computed, ref } from "vue";
import { useHoverStore } from "@/stores/hover";

const props = defineProps(["scale", "tile", "rotate", "limit"]);
const tile = props.tile;
const scale = props.scale;
const rotate = props.rotate;
const limit = props.limit;

const hovered = ref(false);

const tileNames = {
  "1m": "社長",
  "2m": "恋人",
  "3m": "愛人",
  "4m": "有名人",
  "5m": "幼馴染",
  "6m": "友達",
  "7m": "初対面",
  "8m": "先輩",
  "9m": "先生",
  "1p": "お金",
  "2p": "浴衣",
  "3p": "香水",
  "4p": "サングラス",
  "5p": "ゲーム",
  "6p": "学生証",
  "7p": "スマホ",
  "8p": "酒",
  "9p": "メガネ",
  "1s": "高級レストラン",
  "2s": "お祭り",
  "3s": "ホテル",
  "4s": "個室焼肉",
  "5s": "おうち",
  "6s": "カラオケ",
  "7s": "カフェ",
  "8s": "居酒屋",
  "9s": "ドライブ",
  east: "好き",
  south: "愛してる",
  west: "かわいい",
  north: "かっこいい",
  white: "デート行きませんか",
  green: "付き合ってください",
  red: "手繋ご？",
};

const size = computed(() => ({
  width: `${5 * scale}vw`,
  height: `${6 * scale}vw`,
}));

const getHighlight = computed(() => {
  const hoverTile = hoverStore.hoverTile;
  if (tile == hoverTile) {
    return {
      filter: "opacity(0.4) drop-shadow(0 0 0 red)",
    };
  }
  return {};
});

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

const hoverStore = useHoverStore();

const tileStyle = ref({});
const handleTileHover = (isHovered) => {
  hovered.value = isHovered;
  if (isHovered) {
    hoverStore.setHoverTile(tile);
    tileStyle.value = {
      transform: `rotate(${rotate}deg) translateY(-1.2vw)`,
      transition: "0.3s",
      cursor: "pointer",
    };
  } else {
    hoverStore.removeHoverTile();
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
  <div v-else>
    <div v-if="limit" class="limit-riichi getTileClass(tile)" :style="{ ...getStyle, ...tileStyle }"
      @mouseover="handleTileHover(true)" @mouseleave="handleTileHover(false)">
      <div v-show="hovered" class="tile-value">{{ tileNames[tile] }}</div>
      <img :style="{ ...getHighlight, ...getStyle }" :src="getImagePath(tile)" />
    </div>
    <div v-else class="getTileClass(tile)" :style="{ ...getStyle, ...tileStyle }" @mouseover="handleTileHover(true)"
      @mouseleave="handleTileHover(false)">
      <div v-show="hovered" class="tile-value">{{ tileNames[tile] }}</div>
      <img :style="{ ...getHighlight, ...getStyle }" :src="getImagePath(tile)" />
    </div>
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
  position: relative;
}

.back-tile {
  pointer-events: none;
  color: #ffc3cd;
  background-color: #ffc3cd;
}

.tile-value {
  position: absolute;
  top: -75%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  white-space: nowrap;
  background-color: pink;
  color: white;
  border-radius: 50%;
  padding: 10px;
  border: 2px solid white;
}

.limit-riichi {
  background: #000;
}

.limit-riichi img {
  opacity: 0.5;
}
</style>

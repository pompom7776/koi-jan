import { ref } from "vue";
import { defineStore } from "pinia";

export const useHoverStore = defineStore("hover", () => {
  const hoverTile = ref("");
  const setHoverTile = (name) => {
    hoverTile.value = name;
  };
  const removeHoverTile = () => {
    hoverTile.value = "";
  };

  return { hoverTile, setHoverTile, removeHoverTile };
});

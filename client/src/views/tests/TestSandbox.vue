<script setup>
import RiichiStickHorizontal from "@/components/parts/RiichiStickHorizontal.vue";
import PointStickHorizontal from "@/components/parts/PointStickHorizontal.vue";
import RiichiStickVertical from "@/components/parts/RiichiStickVertical.vue";
import PointStickVertical from "@/components/parts/PointStickVertical.vue";
import MahjongTile from "@/components/parts/MahjongTile.vue";
</script>
<template>
  <div>
    <div>
      <RiichiStickHorizontal :scale="0.5" />
    </div>
    <div>
      <PointStickHorizontal :scale="0.5" />
    </div>
    <div>
      <RiichiStickVertical :scale="0.5" />
    </div>
    <div>
      <PointStickVertical :scale="0.5" />
    </div>
    <div>
      <MahjongTile :tile="'一萬'" :scale="0.5" :rotate="0" />
      <MahjongTile :tile="'三筒'" :scale="1" :rotate="0" />
      <MahjongTile :tile="'五萬'" :isRedDora="true" :scale="1" :rotate="0" />
      <MahjongTile :tile="'東'" :scale="1.5" :rotate="0" />
      <MahjongTile :tile="'發'" :scale="1" :rotate="0" />
      <MahjongTile :tile="'中'" :scale="1" :rotate="0" />
      <MahjongTile :tile="'白'" :scale="1" :rotate="0" />
    </div>
    <div>
      <MahjongTile :tile="'一萬'" :scale="1" :rotate="90" />
    </div>
    <div>
      <MahjongTile :tile="'一萬'" :scale="1" :rotate="180" />
    </div>
    <div>
      <MahjongTile :tile="'一萬'" :scale="1" :rotate="270" />
    </div>
    <div>
      <MahjongTile :tile="'-'" :scale="1" :rotate="0" />
    </div>
  </div>
</template>
<style scoped></style>

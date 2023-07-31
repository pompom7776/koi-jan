<script setup>
import io from "socket.io-client";
import MahjongTile from "@/components/parts/MahjongTile.vue";
import { onMounted } from "vue";

const socket = io("http://localhost:8888");

const props = defineProps(["player", "isOther", "current"]);
const player = props.player;
const isOther = props.isOther;
const currentPlayerId = props.current;

const socketId = sessionStorage.getItem("socketId")

const discardTile = (tile) => {
  if (currentPlayerId == player.id) {
    socket.emit("discard_tile", socketId, tile.id);
  }
}

onMounted(() => {
})
</script>
<template>
  <div class="discarded">
    <p>河　 :
    <div class="tiles" v-for="tile in player.discarded_tiles">
      <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
    </div>
    </p>
  </div>
  <p>自風 : {{ player.seat_wind }} /
    名前 : {{ player.name }} / 立直 : {{ player.is_riichi }}</p>
  <div style="margin-left: 20px">
    <div class="tiles">
      <p>手牌 :</p>
      <div class="tiles">
        <div class="tiles" v-if="isOther" v-for="_ in player.hand.tiles">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" :isRedDora="false" />
        </div>
        <div class="tiles" v-else v-for="tile in player.hand.tiles">
          <MahjongTile @click="discardTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" :isRedDora="tile.bonus" />
        </div>
      </div>
      <p>ツモ :</p>
      <div class="tsumo" v-if="player.hand.tsumo && isOther">
        <MahjongTile tile="-" :scale="0.5" :rotate="0" :isRedDora="false" />
      </div>
      <div class="tsumo" v-if="player.hand.tsumo && !isOther">
        <MahjongTile @click="discardTile(player.hand.tsumo)" :tile="player.hand.tsumo.name" :scale="0.5" :rotate="0"
          :isRedDora="player.hand.tsumo.bonus" />
      </div>
      <p>鳴き :
      <div class="tiles" v-for="call in player.hand.calls">
        <div v-if="call.type == 'chi'">
          <div class="tiles" v-for="tile in call.tiles">
            <div v-if="call.from_tile.tile.id == tile.id">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="90" />
            </div>
            <div v-else>
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div v-if="call.type == 'pon'">
          <div class="tiles" v-for="tile in call.tiles">
            <div v-if="call.from_tile.tile.id == tile.id">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="90" />
            </div>
            <div v-else>
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div v-if="call.type == 'kan'">
          <div class="tiles" v-for="tile in call.tiles">
            <div v-if="call.from_tile.tile.id == tile.id">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="90" />
            </div>
            <div v-else>
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
      </div>
      </p>
    </div>
  </div>
</template>
<style>
.tiles {
  display: inline-block;
}

.tsumo {
  display: inline-block;
  margin-left: 20px;
}

.discarded {
  border: 1px solid #999;
  width: 80%;
  height: 40%;
}
</style>

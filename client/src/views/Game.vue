<script setup>
import io from "socket.io-client";
import { computed, nextTick, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import MahjongTile from "@/components/parts/MahjongTile.vue";

const socket = io("http://localhost:8888");

const socketId = ref("");
const playerId = ref("");
const host = ref(false);

const displayFlag = ref(true);

const roomId = ref("");
const players = ref({});
const table = ref({});
const currentPlayerId = ref(0);
const currentPlayerName = ref(0);
const dealer = ref("");
const doraTiles = ref([]);

const topPlayer = ref(null);
const leftPlayer = ref(null);
const rightPlayer = ref(null);
const bottomPlayer = ref(null);

const action = ref({
  riichi: false,
  chi: false,
  pon: false,
  kan: false,
  tsumo: false,
  ron: false,
});

const discardFlag = ref(false);
const riichiFlag = ref(false);
const endFlag = ref(false);
const voteFlag = ref(false);
const selectFlag = ref(0);

const getSeatByPlayerId = (playerId) => {
  const seatWinds = table.value["seat_winds"];
  for (const seat in table.value["seat_winds"]) {
    if (seatWinds[seat] == playerId) {
      return seat;
    }
  }
  return null;
};

const assignRelativeSeats = (mySeat) => {
  const seatWinds = table.value["seat_winds"];
  const seatOrder = ["east", "south", "west", "north"];
  const relativeSeats = {};
  const myIndex = seatOrder.indexOf(mySeat);

  relativeSeats.right = seatWinds[seatOrder[(myIndex + 1) % seatOrder.length]];
  relativeSeats.top = seatWinds[seatOrder[(myIndex + 2) % seatOrder.length]];
  relativeSeats.left = seatWinds[seatOrder[(myIndex + 3) % seatOrder.length]];

  return relativeSeats;
};

const discardTile = (tile) => {
  if (discardFlag.value) {
    socket.emit("discard_tile", tile.id);
    discardFlag.value = false;
    action.value = {
      riichi: false,
      chi: false,
      pon: false,
      kan: false,
      tsumo: false,
      ron: false,
    };
  }

  if (voteFlag.value && selectFlag.value < 3) {
    socket.emit("select_tile", tile.id);
  }
};

const cancelTile = (tile) => {
  socket.emit("cancel_tile", tile.id);
  selectFlag.value -= 1;
};

const riichi = () => {
  socket.emit("riichi");
};

const tsumo = () => {
  socket.emit("tsumo_agari");
};

const pon = () => {
  socket.emit("pon");
};

const skipPon = () => {
  socket.emit("skip_pon");
};

const daiMinKan = () => {
  socket.emit("dai_min_kan");
};

const skipDaiMinKan = () => {
  socket.emit("skip_dai_min_kan");
};

const ron = () => {
  socket.emit("ron");
};

const skipRon = () => {
  socket.emit("skip_ron");
};

const closeEndDisplay = () => {
  endFlag.value = false;
  if (host.value == "true") {
    socket.emit("close_score_result");
  }
};

const vote = (player_id) => {
  socket.emit("vote", player_id);
  voteFlag.value = false;
};
const windDirections = {
  east: "東",
  south: "南",
  west: "西",
  north: "北",
};

const getImgDirection = (pid) => {
  if (pid == currentPlayerId.value) {
    return {
      width: "6vw",
    };
  } else {
    return {
      width: "4vw",
    };
  }
};

const showModal = ref(false);
const closeModal = () => {
  showModal.value = false;
  closeEndDisplay();
};

const route = useRoute();

onMounted(() => {
  playerId.value = sessionStorage.getItem("playerId");
  socketId.value = sessionStorage.getItem("socketId");
  host.value = sessionStorage.getItem("host");
  socket.emit("connect_game", socketId.value);
  socket.on("reconnected", (socket_id) => {
    sessionStorage.setItem("socketId", socket_id);
  });

  roomId.value = route.params.roomId;

  if (host.value == "true") {
    socket.emit("setup_game");
  }
  socket.on("update_game", (game_info) => {
    console.log(game_info);
  });
});
</script>

<template>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@800&display=swap" rel="stylesheet" />
  <div class="body">
    <div class="container" v-if="displayFlag">
      <div class="top-content content" v-if="topPlayer">
        <div class="tiles" v-for="_ in topPlayer.value.hand.tiles">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" :isRedDora="false" />
        </div>
        <div class="tsumo" v-if="topPlayer.value.hand.tsumo">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" :isRedDora="false" />
        </div>
        <div class="calls" v-for="call in topPlayer.value.hand.calls">
          <div class="pon" v-if="call.type == 'pon'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
          <div class="kan" v-if="call.type == 'dai_min_kan'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="left-content content" v-if="leftPlayer">
        <div class="tiles" v-for="_ in leftPlayer.value.hand.tiles">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" :isRedDora="false" />
        </div>
        <div class="tsumo" v-if="leftPlayer.value.hand.tsumo">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" :isRedDora="false" />
        </div>
        <div class="calls" v-for="call in leftPlayer.value.hand.calls">
          <div class="pon" v-if="call.type == 'pon'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
          <div class="kan" v-if="call.type == 'dai_min_kan'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="right-content content" v-if="rightPlayer">
        <div class="tiles" v-for="_ in rightPlayer.value.hand.tiles">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" :isRedDora="false" />
        </div>
        <div class="tsumo" v-if="rightPlayer.value.hand.tsumo">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" :isRedDora="false" />
        </div>
        <div class="calls" v-for="call in rightPlayer.value.hand.calls">
          <div class="pon" v-if="call.type == 'pon'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
          <div class="kan" v-if="call.type == 'dai_min_kan'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="bottom-content content" v-if="bottomPlayer">
        <div v-if="!riichiFlag" class="tiles" v-for="tile in bottomPlayer.value.hand.tiles">
          <MahjongTile @click="discardTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" :isRedDora="tile.bonus"
            :limit="false" />
        </div>
        <div v-if="riichiFlag" class="tiles" v-for="tile in bottomPlayer.value.hand.tiles">
          <div v-if="tile.can_riichi">
            <MahjongTile @click="discardTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" :isRedDora="tile.bonus"
              :limit="false" />
          </div>
          <div v-if="!tile.can_riichi">
            <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" :isRedDora="tile.bonus" :limit="true" />
          </div>
        </div>
        <div v-if="bottomPlayer.value.hand.tsumo" class="tsumo">
          <div v-if="riichiFlag">
            <div v-if="!bottomPlayer.value.hand.tsumo.can_riichi">
              <MahjongTile :tile="bottomPlayer.value.hand.tsumo.name" :scale="0.5" :rotate="0"
                :isRedDora="bottomPlayer.value.hand.tsumo.bonus" :limit="true" />
            </div>
            <div v-if="bottomPlayer.value.hand.tsumo.can_riichi">
              <MahjongTile @click="discardTile(bottomPlayer.value.hand.tsumo)" :tile="bottomPlayer.value.hand.tsumo.name"
                :scale="0.5" :rotate="0" :isRedDora="bottomPlayer.value.hand.tsumo.bonus" :limit="false" />
            </div>
          </div>
          <div v-if="!riichiFlag">
            <MahjongTile @click="discardTile(bottomPlayer.value.hand.tsumo)" :tile="bottomPlayer.value.hand.tsumo.name"
              :scale="0.5" :rotate="0" :isRedDora="bottomPlayer.value.hand.tsumo.bonus" :limit="false" />
          </div>
        </div>
        <div class="calls" v-for="call in bottomPlayer.value.hand.calls">
          <div class="pon" v-if="call.type == 'pon'">
            <div class="tiles" v-for="tile in call.tiles">
              <div v-if="voteFlag">
                <MahjongTile @click="discardTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
              <div v-else>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
          <div class="kan" v-if="call.type == 'dai_min_kan'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="voteFlag">
        <div class="center-content-vote">
          <div v-for="player in players">
            <div v-if="player.id == playerId">
              <div class="three-tiles-vote">
                <div class="tiles" v-for="tile in player.selected_tiles">
                  <MahjongTile @click="cancelTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" />
                </div>
              </div>
              <button class="disable-vote" disabled>
                {{ player.name }}に投票
              </button>
            </div>
            <div v-else>
              <div class="three-tiles-vote">
                <div class="tiles" v-for="tile in player.selected_tiles">
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                </div>
              </div>
              <button @click="vote(player.id)">{{ player.name }}に投票</button>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div class="center-content">
          <!-- 局・本場・順目・残り・東西南北・ドラ -->
          <div class="all_tiles">
            <div class="tiles" v-for="tile in doraTiles">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
          <div class="round-wind">{{ windDirections[table.round_wind] }}</div>
          <div class="center-all">
            <div>部屋番号 : {{ roomId }}</div>
            <div>残り枚数 : {{ table.wall_num }}</div>
            <div>現在の番 : {{ currentPlayerName }}</div>
            <div>親 : {{ dealer }}</div>
            <div>局 : {{ table.round }}</div>
          </div>
        </div>
        <div class="top-discarded discarded" v-if="topPlayer">
          <div class="discarded">
            <div class="tiles" v-for="tile in topPlayer.value.discarded_tiles">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div class="left-discarded discarded" v-if="leftPlayer">
          <div class="discarded">
            <div class="tiles" v-for="tile in leftPlayer.value.discarded_tiles">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div class="right-discarded discarded" v-if="rightPlayer">
          <div class="discarded">
            <div class="tiles" v-for="tile in rightPlayer.value.discarded_tiles">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div class="bottom-discarded discarded" v-if="bottomPlayer">
          <div class="discarded">
            <div class="tiles" v-for="tile in bottomPlayer.value.discarded_tiles">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
      </div>
      <div class="all_direction">
        <div class="top-direction direction" v-if="topPlayer">
          <img :style="getImgDirection(topPlayer.value.id)" :src="`/${topPlayer.value.seat_wind}.png`" />
          <p class="name-direction">{{ topPlayer.value.name }}</p>
          <p class="score-direction">{{ topPlayer.value.score }}点</p>
        </div>
        <div class="left-direction direction" v-if="leftPlayer">
          <img :style="getImgDirection(leftPlayer.value.id)" :src="`/${leftPlayer.value.seat_wind}.png`" />
          <p class="name-direction">{{ leftPlayer.value.name }}</p>
          <p class="score-direction">{{ leftPlayer.value.score }}点</p>
        </div>
        <div class="right-direction direction" v-if="rightPlayer">
          <img :style="getImgDirection(rightPlayer.value.id)" :src="`/${rightPlayer.value.seat_wind}.png`" />
          <p class="name-direction">{{ rightPlayer.value.name }}</p>
          <p class="score-direction">{{ rightPlayer.value.score }}点</p>
        </div>
        <div class="bottom-direction direction" v-if="bottomPlayer">
          <img :style="getImgDirection(bottomPlayer.value.id)" :src="`/${bottomPlayer.value.seat_wind}.png`" />
          <p class="name-direction">{{ bottomPlayer.value.name }}</p>
          <p class="score-direction">{{ bottomPlayer.value.score }}点</p>
        </div>
      </div>
      <div class="all_button">
        <div class="button-container">
          <button @click="riichi" v-if="action.riichi && riichiFlag" class="riichi">
            リーチ: ON
          </button>
          <button @click="riichi" v-if="action.riichi && !riichiFlag" class="riichi">
            リーチ: OFF
          </button>
          <button @click="pon" v-if="action.pon">ポン</button>
          <button @click="skipPon" v-if="action.pon">スキップ</button>
          <button @click="daiMinKan" v-if="action.kan">カン</button>
          <button @click="skipDaiMinKan" v-if="action.kan">スキップ</button>
          <button @click="ron" v-if="action.ron">ロン</button>
          <button @click="skipRon" v-if="action.ron">スキップ</button>
          <button @click="tsumo" v-if="action.tsumo" class="tsumo">ツモ</button>
          <button @click="discardTile(bottomPlayer.value.hand.tsumo)" v-if="action.tsumo" class="tsumo">
            スキップ
          </button>
        </div>
      </div>
      <!-- モーダルウィンドウ-->
      <div class="modal" :class="{ 'show-modal': showModal }">
        <div class="modal-content">
          <span class="close-button" @click="closeModal">&times;</span>
          <h2>Final Score Results</h2>
          <div v-for="player in players">
            <p v-if="player.score_info">
              {{ player.name }}: {{ player.score_info.cost }}
            </p>
          </div>
          <button class="modal-close-button" @click="closeModal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #444444;
  margin: 0;
  font-family: "M PLUS Rounded 1c", sans-serif;
}

.container {
  position: relative;
  width: 100vw;
  height: 56.25vw;
  background-image: url("@/assets/rose_wallpaper.jpg");
  background-size: cover;
}

.top-content {
  top: 10%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(180deg);
}

.left-content {
  top: 50%;
  left: 5%;
  transform: translate(-50%, -50%) rotate(90deg);
}

.main-content {
  position: absolute;
  z-index: 10000;
}

.right-content {
  top: 50%;
  left: 95%;
  transform: translate(-50%, -50%) rotate(-90deg);
}

.bottom-content {
  top: 90%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.right-direction {
  top: 70%;
  left: 83%;
}

.bottom-direction {
  top: 76%;
  left: 20%;
}

.left-direction {
  top: 13%;
  left: 11%;
}

.top-direction {
  top: 13%;
  left: 73%;
}

img {
  width: 6vw;
}

.all_direction p {
  margin: 5px;
}

.name-direction {
  font-size: 1.5vw;
  color: black;
}

.score-direction {
  color: grey;
  font-size: 1.1vw;
}

.center-content-vote {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  position: absolute;
  display: flex;
  flex-direction: row;
  justify-content: center;
  border-radius: 20px;
}

.center-content {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  position: absolute;
  width: 30%;
  height: 30%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: left;
  background-color: #ffc3cd;
  border-radius: 20px;
}

.top-discarded {
  top: 34%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(180deg);
}

.left-discarded {
  top: 50%;
  left: 33%;
  transform: translate(-50%, -50%) rotate(90deg);
}

.right-discarded {
  top: 50%;
  left: 67%;
  transform: translate(-50%, -50%) rotate(-90deg);
}

.bottom-discarded {
  top: 66%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.content {
  position: absolute;
  width: 40%;
  height: 10%;
  display: flex;
  /* flex-direction: column; */
  justify-content: center;
  align-items: center;
  border: 7px solid #ffc3cd;
  background-color: #fff;
  border-radius: 20px;
  font-size: 1.1vw;
}

.discarded {
  position: absolute;
  width: 15vw;
  height: 10%;
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  font-size: 1.1vw;
  flex-direction: row;
}

.direction {
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.all_button {
  position: absolute;
  top: 75%;
  left: 55%;
}

.button-container {
  display: flex;
  flex-direction: row;
}

button {
  font-size: 1.1vw;
  border-radius: 5px;
  border: 3px solid transparent;
  background-color: #ffc3cd;
  color: #fff;
  padding: 0.8vw 2vw;
  cursor: pointer;
  user-select: none;
  margin: 5px;
  transition: 0.5s;
  border-color: #fff;
  font-family: "M PLUS Rounded 1c", sans-serif;
}

button input[type="radio"] {
  display: none;
}

button:hover {
  background-color: rgb(254, 244, 242, 0.5);
  color: rgb(107, 76, 83, 0.8);
  transition: 0.5s;
  border: 3px solid rgb(107, 76, 83, 0.8);
}

.all_tiles {
  display: flex;
  flex-direction: row;
  /* justify-content: center;
  align-items: right; */
  position: absolute;
  top: 2vw;
  left: 14vw;
}

.round-wind {
  position: absolute;
  top: 3.5vw;
  left: 15.8vw;
  font-size: 10vw;
  color: #fff;
}

.center-all {
  position: absolute;
  top: 2vw;
  left: 2vw;
  font-size: 1.3vw;
  color: #fff;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

/* Style for showing the modal */
.show-modal {
  opacity: 1;
  pointer-events: auto;
}

/* Style for the modal content */
.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 80%;
}

/* Style for the modal close button */
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.5rem;
  cursor: pointer;
}

.tsumo {
  /* display: inline-block; */
  margin-left: 1vw;
}

.calls {
  /* display: inline-block; */
  margin-left: 1vw;
}

.pon {
  display: flex;
  flex-direction: row;
}

.kan {
  display: flex;
  flex-direction: row;
}

.three-tiles-vote {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.selected {
  /* Add styles for the selected button */
  background-color: rgb(254, 244, 242, 0.5);
  color: rgb(107, 76, 83, 0.8);
  border: 3px solid rgb(107, 76, 83, 0.8);
}

.disable-vote {
  background-color: #ffe6f0;
}

.disable-vote:hover {
  background-color: #ffe6f0;
  color: #fff;
}
</style>

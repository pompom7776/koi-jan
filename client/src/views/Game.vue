<script setup>
import io from "socket.io-client";
import { computed, nextTick, onMounted, ref } from "vue";
import MahjongTile from "@/components/parts/MahjongTile.vue";

const socket = io("http://localhost:8888");
const displayFlag = ref(true);

const socketId = ref("");
const host = ref(false);
const roomId = ref(0);
const roomNumber = ref(0);
const players = ref([]);
const myId = ref(0);
const roundNumber = ref();
const roundWind = ref("");
const dealerName = ref(null);
const remainingNumber = ref(0);
const seatWinds = ref({});
const dora = ref([]);
const currentPlayerId = ref(0);

const drawFlag = ref(false);
const riichiFlag = ref(false);

const windDirections = {
  east: "東",
  south: "南",
  west: "西",
  north: "北",
};

const relativeSeats = ref({});

const bottomPlayer = ref(null);
const rightPlayer = ref(null);
const topPlayer = ref(null);
const leftPlayer = ref(null);

const bottomDiscarded = ref([]);
const rightDiscarded = ref([]);
const topDiscarded = ref([]);
const leftDiscarded = ref([]);

onMounted(() => {
  socketId.value = sessionStorage.getItem("socketId");
  socket.emit("connect_game", socketId.value);
  host.value = sessionStorage.getItem("host");
  if (host.value == "true") socket.emit("setup_game");
});

const reloadDisplay = async () => {
  displayFlag.value = false;
  await nextTick(() => {
    displayFlag.value = true;
  });
};

const getMyIdBySocketId = (players, socketId) => {
  for (var i = 0; i < players.length; i++) {
    if (players[i]["socket_id"] == socketId) return players[i]["id"];
  }
};
const getPlayerNameById = (playerId) => {
  const player = players.value.find((player) => player.id == playerId);
  if (player) {
    return player["name"];
  } else {
    return "";
  }
};

const setSeatPlayers = (myId) => {
  const myWind = getWindByPlayerId(myId);
  assignRelativeSeats(myWind);
  bottomPlayer.value = computed(() =>
    players.value.find((player) => player.id == relativeSeats.value["bottom"])
  );
  rightPlayer.value = computed(() =>
    players.value.find((player) => player.id == relativeSeats.value["right"])
  );
  topPlayer.value = computed(() =>
    players.value.find((player) => player.id == relativeSeats.value["top"])
  );
  leftPlayer.value = computed(() =>
    players.value.find((player) => player.id == relativeSeats.value["left"])
  );
};
const getWindByPlayerId = (playerId) => {
  for (var i = 0; i < seatWinds.value.length; i++) {
    if (seatWinds.value[i]["player_id"] == playerId)
      return seatWinds.value[i]["wind"];
  }
};
const assignRelativeSeats = (myWind) => {
  const winds = ["east", "south", "west", "north"];
  const myIndex = winds.indexOf(myWind);

  const assignedRelativeSeats = {};
  assignedRelativeSeats.bottom = myId.value;
  for (var i = 0; i < seatWinds.value.length; i++) {
    if (seatWinds.value[i]["wind"] == winds[(myIndex + 1) % winds.length]) {
      assignedRelativeSeats.right = seatWinds.value[i]["player_id"];
    } else if (
      seatWinds.value[i]["wind"] == winds[(myIndex + 2) % winds.length]
    ) {
      assignedRelativeSeats.top = seatWinds.value[i]["player_id"];
    } else if (
      seatWinds.value[i]["wind"] == winds[(myIndex + 3) % winds.length]
    ) {
      assignedRelativeSeats.left = seatWinds.value[i]["player_id"];
    }
  }

  relativeSeats.value = assignedRelativeSeats;
};

const getSeatByPlayerId = (playerId) => {
  for (const seat in relativeSeats.value) {
    if (relativeSeats.value[seat] == playerId) {
      return seat;
    }
  }
};

const discardTile = (tile) => {
  if (drawFlag.value) {
    socket.emit("discard_tile", tile.id);
    drawFlag.value = false;
  }
};

socket.on("reconnected", (socket_id) => {
  socketId.value = socket_id;
  sessionStorage.setItem("socketId", socket_id);
});

socket.on("update_game", (received_game) => {
  roomId.value = received_game["id"];
  roomNumber.value = received_game["number"];

  players.value = received_game["players"];
  roundNumber.value = received_game["game"]["round"]["round_number"];
  roundWind.value = received_game["game"]["round"]["round_wind"];
  dealerName.value = players.value.find(
    (player) => player.id == received_game["game"]["round"]["dealer_id"]
  ).name;
  remainingNumber.value =
    received_game["game"]["round"]["wall_remaining_number"];
  seatWinds.value = received_game["game"]["round"]["seat_winds"];
  dora.value = received_game["game"]["round"]["dora"];
  currentPlayerId.value = received_game["game"]["round"]["current_player_id"];

  myId.value = getMyIdBySocketId(players.value, socketId.value);
  setSeatPlayers(myId.value);

  reloadDisplay();
});

socket.on("update_players", (received_players) => {
  players.value = received_players;

  reloadDisplay();
});

socket.on("update_discardeds", (received_discardeds) => {
  for (var i = 0; i < received_discardeds.length; i++) {
    const seat = getSeatByPlayerId(received_discardeds[i]["player_id"]);
    if (seat == "bottom") {
      bottomDiscarded.value = received_discardeds[i]["tiles"];
    } else if (seat == "right") {
      rightDiscarded.value = received_discardeds[i]["tiles"];
    } else if (seat == "top") {
      topDiscarded.value = received_discardeds[i]["tiles"];
    } else if (seat == "left") {
      leftDiscarded.value = received_discardeds[i]["tiles"];
    }
  }
});

socket.on("notice_draw", () => {
  drawFlag.value = true;
});
</script>

<template>
  <div class="body">
    <div class="container" v-if="displayFlag">
      <div class="top-content content" v-if="topPlayer">
        <div class="tiles" v-for="_ in topPlayer.value.hand">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <div class="tsumo" v-if="topPlayer.value.tsumo">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <!-- <div class="calls" v-for="call in topPlayer.value.hand.calls"> -->
        <!--   <div class="pon" v-if="call.type == 'pon'"> -->
        <!--     <div class="tiles" v-for="tile in call.tiles"> -->
        <!--       <div> -->
        <!--         <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" /> -->
        <!--       </div> -->
        <!--     </div> -->
        <!--   </div> -->
        <!--   <div class="kan" v-if="call.type == 'dai_min_kan'"> -->
        <!--     <div class="tiles" v-for="tile in call.tiles"> -->
        <!--       <div> -->
        <!--         <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" /> -->
        <!--       </div> -->
        <!--     </div> -->
        <!--   </div> -->
        <!-- </div> -->
      </div>
      <div class="left-content content" v-if="leftPlayer">
        <div class="tiles" v-for="_ in leftPlayer.value.hand">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <div class="tsumo" v-if="leftPlayer.value.tsumo">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <!-- <div class="calls" v-for="call in leftPlayer.value.hand.calls"> -->
        <!--   <div class="pon" v-if="call.type == 'pon'"> -->
        <!--     <div class="tiles" v-for="tile in call.tiles"> -->
        <!--       <div> -->
        <!--         <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" /> -->
        <!--       </div> -->
        <!--     </div> -->
        <!--   </div> -->
        <!--   <div class="kan" v-if="call.type == 'dai_min_kan'"> -->
        <!--     <div class="tiles" v-for="tile in call.tiles"> -->
        <!--       <div> -->
        <!--         <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" /> -->
        <!--       </div> -->
        <!--     </div> -->
        <!--   </div> -->
        <!-- </div> -->
      </div>
      <div class="right-content content" v-if="rightPlayer">
        <div class="tiles" v-for="_ in rightPlayer.value.hand">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <div class="tsumo" v-if="rightPlayer.value.tsumo">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <!-- <div class="calls" v-for="call in rightPlayer.value.hand.calls"> -->
        <!--   <div class="pon" v-if="call.type == 'pon'"> -->
        <!--     <div class="tiles" v-for="tile in call.tiles"> -->
        <!--       <div> -->
        <!--         <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" /> -->
        <!--       </div> -->
        <!--     </div> -->
        <!--   </div> -->
        <!--   <div class="kan" v-if="call.type == 'dai_min_kan'"> -->
        <!--     <div class="tiles" v-for="tile in call.tiles"> -->
        <!--       <div> -->
        <!--         <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" /> -->
        <!--       </div> -->
        <!--     </div> -->
        <!--   </div> -->
        <!-- </div> -->
      </div>
      <div class="bottom-content content" v-if="bottomPlayer">
        <div v-if="!riichiFlag" class="tiles" v-for="tile in bottomPlayer.value.hand">
          <MahjongTile @click="discardTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" :limit="false" />
        </div>
        <div v-if="riichiFlag" class="tiles" v-for="tile in bottomPlayer.value.hand">
          <div v-if="tile.can_riichi">
            <MahjongTile @click="discardTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" :limit="false" />
          </div>
          <div v-if="!tile.can_riichi">
            <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" :limit="true" />
          </div>
        </div>
        <div v-if="bottomPlayer.value.tsumo" class="tsumo">
          <div v-if="riichiFlag">
            <div v-if="!bottomPlayer.value.tsumo.can_riichi">
              <MahjongTile :tile="bottomPlayer.value.tsumo.name" :scale="0.5" :rotate="0" :limit="true" />
            </div>
            <div v-if="bottomPlayer.value.tsumo.can_riichi">
              <MahjongTile @click="discardTile(bottomPlayer.value.tsumo)" :tile="bottomPlayer.value.tsumo.name"
                :scale="0.5" :rotate="0" :limit="false" />
            </div>
          </div>
          <div v-if="!riichiFlag">
            <MahjongTile @click="discardTile(bottomPlayer.value.tsumo)" :tile="bottomPlayer.value.tsumo.name" :scale="0.5"
              :rotate="0" :limit="false" />
          </div>
        </div>
        <!-- <div class="calls" v-for="call in bottomPlayer.value.hand.calls"> -->
        <!--   <div class="pon" v-if="call.type == 'pon'"> -->
        <!--     <div class="tiles" v-for="tile in call.tiles"> -->
        <!--       <div v-if="voteFlag"> -->
        <!--         <MahjongTile -->
        <!--           @click="discardTile(tile)" -->
        <!--           :tile="tile.name" -->
        <!--           :scale="0.5" -->
        <!--           :rotate="0" -->
        <!--         /> -->
        <!--       </div> -->
        <!--       <div v-else> -->
        <!--         <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" /> -->
        <!--       </div> -->
        <!--     </div> -->
        <!--   </div> -->
        <!--   <div class="kan" v-if="call.type == 'dai_min_kan'"> -->
        <!--     <div class="tiles" v-for="tile in call.tiles"> -->
        <!--       <div> -->
        <!--         <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" /> -->
        <!--       </div> -->
        <!--     </div> -->
        <!--   </div> -->
        <!-- </div> -->
      </div>
      <div v-if="voteFlag">
        <div class="center-content-vote">
          <div v-for="player in players">
            <div v-if="player.id == myId">
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
            <div class="tiles" v-for="tile in dora">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
          <div class="round-wind">{{ windDirections[roundWind] }}</div>
          <div class="center-all">
            <div>部屋番号 : {{ roomNumber }}</div>
            <div>残り枚数 : {{ remainingNumber }}</div>
            <div>現在の手番 : {{ getPlayerNameById(currentPlayerId) }}</div>
            <div>親 : {{ dealerName }}</div>
            <div>局 : {{ roundNumber }}</div>
          </div>
        </div>
        <div class="top-discarded discarded" v-if="topDiscarded">
          <div class="discarded">
            <div class="tiles" v-for="tile in topDiscarded">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div class="left-discarded discarded" v-if="leftDiscarded">
          <div class="discarded">
            <div class="tiles" v-for="tile in leftDiscarded">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div class="right-discarded discarded" v-if="rightDiscarded">
          <div class="discarded">
            <div class="tiles" v-for="tile in rightDiscarded">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div class="bottom-discarded discarded" v-if="bottomDiscarded">
          <div class="discarded">
            <div class="tiles" v-for="tile in bottomDiscarded">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
      </div>
      <div class="all_direction">
        <div class="top-direction direction" v-if="topPlayer">
          <!-- <img -->
          <!--   :style="getImgDirection(topPlayer.id)" -->
          <!--   :src="`/${topPlayer.seat_wind}.png`" -->
          <!-- /> -->
          <p class="name-direction">{{ topPlayer.name }}</p>
          <!-- <p class="score-direction">{{ topPlayer.score }}点</p> -->
        </div>
        <div class="left-direction direction" v-if="leftPlayer">
          <!-- <img -->
          <!--   :style="getImgDirection(leftPlayer.value.id)" -->
          <!--   :src="`/${leftPlayer.seat_wind}.png`" -->
          <!-- /> -->
          <p class="name-direction">{{ leftPlayer.name }}</p>
          <!-- <p class="score-direction">{{ leftPlayer.score }}点</p> -->
        </div>
        <div class="right-direction direction" v-if="rightPlayer">
          <!-- <img -->
          <!--   :style="getImgDirection(rightPlayer.id)" -->
          <!--   :src="`/${rightPlayer.seat_wind}.png`" -->
          <!-- /> -->
          <p class="name-direction">{{ rightPlayer.name }}</p>
          <!-- <p class="score-direction">{{ rightPlayer.score }}点</p> -->
        </div>
        <div class="bottom-direction direction" v-if="bottomPlayer">
          <!-- <img -->
          <!--   :style="getImgDirection(bottomPlayer.id)" -->
          <!--   :src="`/${bottomPlayer.seat_wind}.png`" -->
          <!-- /> -->
          <p class="name-direction">{{ bottomPlayer.name }}</p>
          <!-- <p class="score-direction">{{ bottomPlayer.score }}点</p> -->
        </div>
      </div>
      <!-- <div class="all_button"> -->
      <!--   <div class="button-container"> -->
      <!--     <button -->
      <!--       @click="riichi" -->
      <!--       v-if="action.riichi && riichiFlag" -->
      <!--       class="riichi" -->
      <!--     > -->
      <!--       リーチ: ON -->
      <!--     </button> -->
      <!--     <button -->
      <!--       @click="riichi" -->
      <!--       v-if="action.riichi && !riichiFlag" -->
      <!--       class="riichi" -->
      <!--     > -->
      <!--       リーチ: OFF -->
      <!--     </button> -->
      <!--     <button @click="pon" v-if="action.pon">ポン</button> -->
      <!--     <button @click="skipPon" v-if="action.pon">スキップ</button> -->
      <!--     <button @click="daiMinKan" v-if="action.kan">カン</button> -->
      <!--     <button @click="skipDaiMinKan" v-if="action.kan">スキップ</button> -->
      <!--     <button @click="ron" v-if="action.ron">ロン</button> -->
      <!--     <button @click="skipRon" v-if="action.ron">スキップ</button> -->
      <!--     <button @click="tsumo" v-if="action.tsumo" class="tsumo">ツモ</button> -->
      <!--     <button -->
      <!--       @click="discardTile(bottomPlayer.value.hand.tsumo)" -->
      <!--       v-if="action.tsumo" -->
      <!--       class="tsumo" -->
      <!--     > -->
      <!--       スキップ -->
      <!--     </button> -->
      <!--   </div> -->
      <!-- </div> -->
      <!-- モーダルウィンドウ-->
      <!-- <div class="modal" :class="{ 'show-modal': showModal }"> -->
      <!--   <div class="modal-content"> -->
      <!--     <span class="close-button" @click="closeModal">&times;</span> -->
      <!--     <h2>Final Score Results</h2> -->
      <!--     <div v-for="player in players"> -->
      <!--       <p v-if="player.score_info"> -->
      <!--         {{ player.name }}: {{ player.score_info.cost }} -->
      <!--       </p> -->
      <!--     </div> -->
      <!--     <button class="modal-close-button" @click="closeModal">Close</button> -->
      <!--   </div> -->
      <!-- </div> -->
    </div>
  </div>
</template>

<style scoped>
.body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  font-family: "M PLUS Rounded 1c", sans-serif;
}

.container {
  position: relative;
  width: 100vw;
  height: 56.25vw;
  background-size: cover;
  background: linear-gradient(45deg,
      rgba(250, 208, 196, 0.5),
      rgba(255, 209, 255, 0.5),
      rgba(168, 237, 234, 0.5));
  background-size: 200% 200%;
  animation: bggradient 5s ease infinite;
}

@keyframes bggradient {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
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
  background-color: #fff;
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
  /* border: 7px solid #ffc3cd; */
  /* background-color: #fff; */
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
  color: #ffc3cd;
}

.center-all {
  position: absolute;
  top: 2vw;
  left: 2vw;
  font-size: 1.3vw;
  color: #ffc3cd;
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

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 80%;
}

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

.tiles {
  margin: 0 0.15vw;
}
</style>

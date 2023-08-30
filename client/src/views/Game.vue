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
const chatMessage = ref("");
const chats = ref([]);

const drawFlag = ref(false);
const riichiFlag = ref(false);
const voteFlag = ref(false);
const votedFlag = ref(false);
const selectCount = ref(0);
const chatFlag = ref(false);

const showModal = ref(false);

const canPon = ref(false);
const canKan = ref(false);
const canRon = ref(false);
const canRiichi = ref(false);
const canTsumo = ref(false);

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

onMounted(() => {
  socketId.value = sessionStorage.getItem("socketId");
  host.value = sessionStorage.getItem("host");
  socket.emit("connect_game", socketId.value);
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

const clickTile = (tile) => {
  if (drawFlag.value) {
    socket.emit("discard_tile", tile.id, riichiFlag.value);
    drawFlag.value = false;
    canRiichi.value = false;
    canTsumo.value = false;
  }

  if (voteFlag.value && selectCount.value < 3) {
    socket.emit("select_tile", tile.id);
  }
};

const cancelTile = (tile) => {
  socket.emit("cancel_tile", tile.id);
};

const skip = () => {
  if (canTsumo.value) {
    canRiichi.value = false;
    canTsumo.value = false;
  } else {
    socket.emit("skip");
    canPon.value = false;
    canKan.value = false;
    canRon.value = false;
  }
};
const call = (callType) => {
  socket.emit("call", callType);
  canPon.value = false;
  canKan.value = false;
  canRon.value = false;
  canRiichi.value = false;
  canTsumo.value = false;
};
const riichi = () => {
  riichiFlag.value = !riichiFlag.value;
  if (riichiFlag.value == true) {
    socket.emit("riichi");
  }
};
const ron = () => {
  socket.emit("agari", "ron");
  canPon.value = false;
  canKan.value = false;
  canRon.value = false;
  canRiichi.value = false;
  canTsumo.value = false;
};
const tsumo = () => {
  socket.emit("agari", "tsumo");
  canPon.value = false;
  canKan.value = false;
  canRon.value = false;
  canRiichi.value = false;
  canTsumo.value = false;
};

const closeModal = () => {
  showModal.value = false;
  if (host.value == "true") {
    socket.emit("close_result");
  }
};

const vote = (targetPlayerId) => {
  socket.emit("vote", targetPlayerId);
  votedFlag.value = true;
};

const sendMessage = () => {
  socket.emit("send_message", chatMessage.value);
  chatMessage.value = "";
};

socket.on("reconnected", (socket_id) => {
  socketId.value = socket_id;
  sessionStorage.setItem("socketId", socket_id);
  if (host.value == "true") socket.emit("setup_round");
  socket.emit("get_messages");
  socket.emit("get_round");
});

socket.on("update_game", (received_game) => {
  console.log(received_game);
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

socket.on("update_player", (received_player) => {
  console.log(received_player);
  for (var i = 0; i < players.value.length; i++) {
    if (players.value[i]["id"] == received_player["id"]) {
      players.value[i] = received_player;
    }
  }
  setSeatPlayers(myId.value);

  reloadDisplay();
});

socket.on("update_remaining_number", (received_remaining_number) => {
  remainingNumber.value = received_remaining_number;

  reloadDisplay();
});

socket.on("update_current_player", (received_player_id) => {
  currentPlayerId.value = received_player_id;

  reloadDisplay();
});

socket.on("notice_drew", () => {
  drawFlag.value = true;
});

socket.on("notice_next_draw", () => {
  socket.emit("draw_tile");
});

socket.on("notice_can_pon", () => {
  canPon.value = true;
});

socket.on("notice_can_kan", () => {
  canKan.value = true;
});

socket.on("notice_can_ron", () => {
  canRon.value = true;
});

socket.on("notice_can_riichi", () => {
  riichiFlag.value = false;
  canRiichi.value = true;
});

socket.on("notice_can_tsumo", () => {
  canTsumo.value = true;
  drawFlag.value = false;
});

socket.on("notice_agari", () => {
  console.log("agari");
  riichiFlag.value = false;

  reloadDisplay();
});

socket.on("notice_end_round", () => {
  showModal.value = true;
  drawFlag.value = false;
  riichiFlag.value = false;

  reloadDisplay();
});

socket.on("notice_start_vote", () => {
  voteFlag.value = true;
  selectCount.value = 0;
});

socket.on("notice_end_vote", () => {
  voteFlag.value = false;
  selectCount.value = 0;

  if (host.value == "true") {
    socket.emit("next_round");
  }
});

socket.on("notice_selected", () => {
  selectCount.value += 1;
});

socket.on("notice_unselected", () => {
  selectCount.value -= 1;
});

socket.on("notice_end_game", () => {
  voteFlag.value = false;
  selectCount.value = 0;

  console.log("end");
});

socket.on("update_chat", (received_chats) => {
  chats.value = received_chats;
});
</script>

<template>
  <div class="body">
    <div class="container" v-if="displayFlag">
      <div v-if="chatFlag">
        <div id="chat-container">
          <div id="messages-container">
            <div id="chat-header">
              <div id="chat-title">チャット</div>
              <button id="chat-close-button" @click="chatFlag = false">
                &#9661;
              </button>
            </div>
            <div id="messages">
              <div v-for="chat in chats">
                <div class="message ms-left">
                  <div class="sender-name">{{ chat.player_name }}</div>
                  <div class="message-box">
                    <div class="message-content">
                      <div class="message-text">{{ chat.message }}</div>
                    </div>
                  </div>
                </div>
                <div class="ms-clear"></div>
              </div>
            </div>
            <div id="ms-send">
              <textarea id="send-message" v-model="chatMessage"></textarea>
              <button id="send-btn" @click="sendMessage">送信</button>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div id="chat-close-container">
          <div id="chat-header">
            <div id="chat-title">チャット</div>
            <button id="chat-close-button" @click="chatFlag = true">
              &#9651;
            </button>
          </div>
        </div>
      </div>
      <div class="top-content content" v-if="topPlayer">
        <div class="tiles" v-for="_ in topPlayer.value.hand">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <div class="tsumo" v-if="topPlayer.value.tsumo">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <div class="calls" v-for="call in topPlayer.value.call">
          <div class="pon" v-if="call.type == 'pon'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
          <div class="kan" v-if="call.type == 'kan'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="left-content content" v-if="leftPlayer">
        <div class="tiles" v-for="_ in leftPlayer.value.hand">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <div class="tsumo" v-if="leftPlayer.value.tsumo">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <div class="calls" v-for="call in leftPlayer.value.call">
          <div class="pon" v-if="call.type == 'pon'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
          <div class="kan" v-if="call.type == 'kan'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="right-content content" v-if="rightPlayer">
        <div class="tiles" v-for="_ in rightPlayer.value.hand">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <div class="tsumo" v-if="rightPlayer.value.tsumo">
          <MahjongTile tile="-" :scale="0.5" :rotate="0" />
        </div>
        <div class="calls" v-for="call in rightPlayer.value.call">
          <div class="pon" v-if="call.type == 'pon'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
          <div class="kan" v-if="call.type == 'kan'">
            <div class="tiles" v-for="tile in call.tiles">
              <div>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="bottom-content content" v-if="bottomPlayer">
        <div v-if="!riichiFlag" class="tiles" v-for="tile in bottomPlayer.value.hand">
          <MahjongTile @click="clickTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" :limit="false" />
        </div>
        <div v-if="riichiFlag" class="tiles" v-for="tile in bottomPlayer.value.hand">
          <div v-if="tile.can_riichi">
            <MahjongTile @click="clickTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" :limit="false" />
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
              <MahjongTile @click="clickTile(bottomPlayer.value.tsumo)" :tile="bottomPlayer.value.tsumo.name" :scale="0.5"
                :rotate="0" :limit="false" />
            </div>
          </div>
          <div v-if="!riichiFlag">
            <MahjongTile @click="clickTile(bottomPlayer.value.tsumo)" :tile="bottomPlayer.value.tsumo.name" :scale="0.5"
              :rotate="0" :limit="false" />
          </div>
        </div>
        <div class="calls" v-for="call in bottomPlayer.value.call">
          <div class="pon" v-if="call.type == 'pon'">
            <div class="tiles" v-for="tile in call.tiles">
              <div v-if="voteFlag">
                <MahjongTile @click="clickTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
              <div v-else>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
          <div class="kan" v-if="call.type == 'kan'">
            <div class="tiles" v-for="tile in call.tiles">
              <div v-if="voteFlag">
                <MahjongTile @click="clickTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
              <div v-else>
                <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="voteFlag">
        <div class="center-content-vote">
          <div v-for="player in players">
            <div v-if="player.id == myId">
              <div class="three-tiles-vote">
                <div class="tiles" v-for="tile in player.selected">
                  <MahjongTile @click="cancelTile(tile)" :tile="tile.name" :scale="0.5" :rotate="0" />
                </div>
              </div>
              <button class="disable-vote" disabled>
                {{ player.name }}に投票
              </button>
            </div>
            <div v-else>
              <div class="three-tiles-vote">
                <div class="tiles" v-for="tile in player.selected">
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                </div>
              </div>
              <div v-if="votedFlag">
                <button class="disable-vote" disabled>
                  {{ player.name }}に投票
                </button>
              </div>
              <div v-else>
                <button @click="vote(player.id)">
                  {{ player.name }}に投票
                </button>
              </div>
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
        <div class="top-discarded discarded" v-if="topPlayer">
          <div class="discarded">
            <div class="tiles" v-for="tile in topPlayer.value.discarded">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div class="left-discarded discarded" v-if="leftPlayer">
          <div class="discarded">
            <div class="tiles" v-for="tile in leftPlayer.value.discarded">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div class="right-discarded discarded" v-if="rightPlayer">
          <div class="discarded">
            <div class="tiles" v-for="tile in rightPlayer.value.discarded">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
            </div>
          </div>
        </div>
        <div class="bottom-discarded discarded" v-if="bottomPlayer">
          <div class="discarded">
            <div class="tiles" v-for="tile in bottomPlayer.value.discarded">
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
          <p class="name-direction">{{ topPlayer.value.name }}</p>
          <!-- <p class="score-direction">{{ topPlayer.score }}点</p> -->
        </div>
        <div class="left-direction direction" v-if="leftPlayer">
          <!-- <img -->
          <!--   :style="getImgDirection(leftPlayer.value.id)" -->
          <!--   :src="`/${leftPlayer.seat_wind}.png`" -->
          <!-- /> -->
          <p class="name-direction">{{ leftPlayer.value.name }}</p>
          <!-- <p class="score-direction">{{ leftPlayer.score }}点</p> -->
        </div>
        <div class="right-direction direction" v-if="rightPlayer">
          <!-- <img -->
          <!--   :style="getImgDirection(rightPlayer.id)" -->
          <!--   :src="`/${rightPlayer.seat_wind}.png`" -->
          <!-- /> -->
          <p class="name-direction">{{ rightPlayer.value.name }}</p>
          <!-- <p class="score-direction">{{ rightPlayer.score }}点</p> -->
        </div>
        <div class="bottom-direction direction" v-if="bottomPlayer">
          <!-- <img -->
          <!--   :style="getImgDirection(bottomPlayer.id)" -->
          <!--   :src="`/${bottomPlayer.seat_wind}.png`" -->
          <!-- /> -->
          <p class="name-direction">{{ bottomPlayer.value.name }}</p>
          <!-- <p class="score-direction">{{ bottomPlayer.score }}点</p> -->
        </div>
      </div>
      <div class="all_button">
        <div class="button-container">
          <button @click="call('pon')" v-if="canPon">ポン</button>
          <button @click="call('kan')" v-if="canKan">カン</button>
          <button @click="riichi" v-if="canRiichi && riichiFlag && !canTsumo">
            リーチ: ON
          </button>
          <button @click="riichi" v-if="canRiichi && !riichiFlag && !canTsumo">
            リーチ: OFF
          </button>
          <button @click="tsumo" v-if="canTsumo">ツモ</button>
          <button @click="ron" v-if="canRon">ロン</button>
          <button @click="skip" v-if="canPon || canKan || canRon || canTsumo">
            スキップ
          </button>
        </div>
      </div>
      <div class="modal" :class="{ 'show-modal': showModal }">
        <div class="modal-content">
          <h2>Final Score Results</h2>
          <div v-for="player in players">
            <div v-if="player.score">
              <p>{{ player.name }}: {{ player.score.score }}</p>
              <p>{{ player.score.han }}翻　{{ player.score.fu }}符</p>
              <p v-for="yaku in player.score.yaku">{{ yaku }}</p>
              <hr />
            </div>
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

#chat-container {
  height: 40vh;
  width: 30vw;
  max-width: 400px;
  position: fixed;
  bottom: 12%;
  left: 2%;
}

#chat-close-container {
  position: fixed;
  width: 30vw;
  max-width: 400px;
  bottom: 5%;
  left: 2%;
}

#messages-container {
  height: 100%;
  width: 100%;
}

#chat-header {
  padding: 6px;
  font-size: 16px;
  height: 3vh;
  background: #ffc0cb;
  border: 1px solid #ea384955;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#chat-title {
  color: rgb(234, 56, 73, 0.8);
  float: left;
  display: flex;
  justify-content: left;
}

#chat-close-button {
  width: 8px;
  height: 8px;
  font-size: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
}

#messages {
  overflow: auto;
  height: 100%;
  border-right: 1px solid #ea384955;
  border-left: 1px solid #ea384955;
  background-color: #fff5;
}

.message {
  margin: 0px;
  padding: 0 14px;
  font-size: 16px;
  word-wrap: break-word;
  white-space: normal;
}

.sender-name {
  margin-top: 15px;
  font-size: 4px;
}

.message-box {
  max-width: 100%;
  font-size: 12px;
}

.message-content {
  padding: 15px;
}

.ms-left {
  float: left;
  line-height: 1em;
}

.ms-left .message-box {
  background: #fff5;
  border: 2px solid #efb0bb;
  border-radius: 30px 30px 30px 0px;
  margin-right: 50px;
}

.ms-right {
  float: right;
  line-height: 1em;
}

.ms-right .message-box {
  background: #fff5;
  border: 2px solid #efb0bb;
  border-radius: 30px 30px 0px 30px;
  margin-left: 50px;
}

.ms-clear {
  clear: both;
}

#ms-send {
  background-color: #fffa;
  border-right: 1px solid #ea384955;
  border-left: 1px solid #ea384955;
  border-bottom: 1px solid #ea384955;
  height: 48px;
  padding: 4px;
}

#send-message {
  resize: none;
  width: calc(100% - 75px);
  line-height: 16px;
  height: 48px;
  padding: 14px 6px 0px 6px;
  border: 1px solid #ea384955;
  border-radius: 8px;
  text-align: left;
  box-sizing: border-box;
}

#send-btn {
  width: 64px;
  height: 40px;
  font-size: 16px;
  float: right;
  background: #ffc0cb;
  border: 1px solid;
}

#send-btn:hover {
  background: #ea3849cc;
  color: #fff;
  cursor: pointer;
}

button {
  display: inline-block;
  background-color: rgb(234, 56, 73, 0.8);
  color: #fff;
  width: 140px;
  border: 3px solid transparent;
  font-family: "M PLUS Rounded 1c", sans-serif;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  user-select: none;
  margin: 5px;
  transition: 0.5s;
  font-size: 20px;
}

button:disabled {
  background-color: rgb(245, 235, 240);
}

button:enabled:hover {
  background-color: #fff;
  color: rgb(234, 56, 73, 0.8);
  transition: 0.5s;
  border: 3px solid rgb(234, 56, 73, 0.8);
}
</style>

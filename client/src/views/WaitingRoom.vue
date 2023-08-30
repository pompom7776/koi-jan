<script setup>
import io from "socket.io-client";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import router from "@/router";

const socket = io("http://localhost:8888");

const socketId = ref("");
const roomId = ref("");
const players = ref([]);
const message = ref("");
const readyPlayers = ref({});
const host = ref("false");
const ready = ref(false);

const chatFlag = ref(false);
const chatMessage = ref("");
const chats = ref([]);

const route = useRoute();
onMounted(() => {
  sessionStorage.setItem("ready", false);
  host.value = sessionStorage.getItem("host");
  socketId.value = sessionStorage.getItem("socketId");
  socket.emit("connect_waiting_room", socketId.value);

  roomId.value = route.params.roomId;
});

const startGame = () => {
  socket.emit("start_game");
  message.value = "";
};

const readyGame = () => {
  sessionStorage.setItem("ready", true);
  ready.value = true;
  socket.emit("ready_game");
  message.value = "";
};

const cancelGame = () => {
  sessionStorage.setItem("ready", false);
  ready.value = false;
  socket.emit("unready_game");
  message.value = "";
};

const leaveRoom = () => {
  socket.emit("leave_room");
  sessionStorage.removeItem("socketId");
  router.push(`/`);
  message.value = "";
};

const isButtonEnabled = computed(() => {
  const keys = Object.keys(readyPlayers.value);
  return keys.length === 4 && keys.every((key) => readyPlayers.value[key]);
});

const addKeyIfNotExists = (obj, key, value) => {
  if (!(key in obj)) {
    obj[key] = value;
  }
};

const sendMessage = () => {
  socket.emit("send_message", chatMessage.value);
  chatMessage.value = "";
};

socket.on("reconnected", (socket_id) => {
  sessionStorage.setItem("socketId", socket_id);
  socket.emit("get_messages");
});

socket.on("joined_room", (player) => {
  players.value.push(player);
  readyPlayers.value[player] = false;
});

socket.on("readied_game", (player_name) => {
  console.log("a", player_name);
  readyPlayers.value[player_name] = true;
});

socket.on("unreadied_game", (player_name) => {
  console.log("a", player_name);
  readyPlayers.value[player_name] = false;
});

socket.on("started_game", () => {
  router.push(`/room/${roomId.value}/game`);
});

socket.on("left_room", (player_name) => {
  const index = players.value.indexOf(player_name);
  players.value.splice(index, 1);
  delete readyPlayers.value[player_name];
});

socket.on("players_info", (player_names) => {
  players.value = player_names;
  players.value.forEach((playerName) => {
    addKeyIfNotExists(readyPlayers.value, playerName, false);
  });
});

socket.on("update_chat", (received_chats) => {
  chats.value = received_chats;
});
</script>
<template>
  <div id="app">
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
    <div class="center">
      <div class="alert-message">
        {{ message }}
      </div>

      <!-- socketId : {{ socketId }} -->
      <div class="roomid">ルームID : {{ roomId }}</div>

      <ul>
        <p v-for="(player, index) in players" :key="index">
          Player{{ index + 1 }} : {{ player }}
          <img v-if="!readyPlayers[player]" src="@/assets/pose_ng_woman.png" alt="Pose NG Woman" class="np_woman" />
          <img v-if="readyPlayers[player]" src="@/assets/pose_heart_man.png" alt="Pose heart Man" class="heart_man" />
        </p>
      </ul>
      <div class="button-group">
        <div v-if="!ready">
          <button @click="readyGame">準備完了</button>
        </div>
        <div v-if="ready">
          <button @click="cancelGame">一旦離席</button>
        </div>
        <button @click="leaveRoom">退出</button>
      </div>
      <div v-if="host == 'true'">
        <button @click="startGame" :disabled="!isButtonEnabled">
          ゲーム開始
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
#app {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  /* background-image: url("@/assets/rose_wallpaper.jpg"); */
  background: linear-gradient(45deg,
      rgba(250, 208, 196, 0.5),
      rgba(255, 209, 255, 0.5),
      rgba(168, 237, 234, 0.5));
  background-size: 200% 200%;
  animation: bggradient 5s ease infinite;

  /* background-size: cover; */
  color: rgb(234, 56, 73, 0.8);
  font-family: "M PLUS Rounded 1c", sans-serif;
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

.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

ul {
  display: flex;
  padding: 25px;
}

.roomid {
  text-align: center;
  font-size: 30px;
  width: 90%;
  color: rgb(234, 56, 73, 0.8);
  border-bottom: 5px solid rgb(234, 56, 73, 0.8);
}

p {
  width: 200px;
  height: 300px;
  background-color: #fff;
  border-radius: 25px;
  margin: 0 10px;
  text-align: center;
  line-height: 100px;
  font-size: 20px;
  border: 5px solid rgb(234, 56, 73, 0.8);
}

.button-group div {
  display: inline-block;
}

button:disabled {
  background-color: rgb(245, 235, 240);
}

button input[type="radio"] {
  display: none;
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

button:enabled:hover {
  background-color: #fff;
  color: rgb(234, 56, 73, 0.8);
  transition: 0.5s;
  border: 3px solid rgb(234, 56, 73, 0.8);
}

button:checked+label {
  background-color: red;
}

img.np_woman {
  margin: -20px;
  width: 90%;
  height: 70%;
  animation-name: fadeInAnime;
  animation-duration: 1s;
  animation-fill-mode: forwards;
  opacity: 0;
}

img.heart_man {
  margin: -20px;
  width: 90%;
  height: 70%;
  object-fit: cover;
  animation-name: fadeInAnime;
  animation-duration: 1s;
  animation-fill-mode: forwards;
  opacity: 0;
}

@keyframes fadeInAnime {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.alert-message {
  color: red;
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
</style>

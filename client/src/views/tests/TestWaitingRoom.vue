<script setup>
import io from "socket.io-client";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import router from "@/router";

const socketId = ref("");
const roomId = ref("");
const players = ref([]);
const message = ref("");
const readyPlayers = ref({});
const host = ref("false");
const ready = ref(false);


const socket = io("http://localhost:8888");

socket.on("players_info", (members) => {
  players.value = members;
  players.value.forEach((playerName) => {
    addKeyIfNotExists(readyPlayers.value, playerName, false);
  });
});

const startGame = () => {
  
  socket.emit("startGame", roomId.value);
  message.value = "";
};

// ここからreadyGameの定義をする
const readyGame = () => {
  sessionStorage.setItem('ready', true);
  ready.value = true
  socket.emit("readyGame");
  message.value = "";
};

const cancelGame = () => {
  sessionStorage.setItem('ready', false);
  ready.value = false
  socket.emit("cancelGame");
  message.value = "";
};

const getoutGame = () => {
  socket.emit("getoutGame");
  sessionStorage.removeItem("socketId")
  router.push(`/test/room`);
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

const route = useRoute();
onMounted(() => {
  host.value = sessionStorage.getItem("host");
  socketId.value = sessionStorage.getItem("socketId");
  socket.emit("reconnect", socketId.value);
  socket.on("reconnected", (newSocketId) => {
    sessionStorage.setItem("socketId", newSocketId);
    socketId.value = newSocketId;
  });

  roomId.value = route.params.roomId;
  socket.emit("get_players", roomId.value);

  socket.on("player_joined", (player) => {
    players.value.push(player);
    readyPlayers.value[player] = false;
  });

  // serverからreadiedを受け取ってreadyPlayers[p_name]をtrueにする
  socket.on("readied", (player) => {
    readyPlayers.value[player] = true;
  });

  socket.on("canceled", (player) => {
    readyPlayers.value[player] = false;
  });

  // hostがゲーム開始ボタンを押したら、roomIDの人全員がそのリンクに飛ぶ
  socket.on("started", () => {
    router.push(`/test/room/${roomId.value}/game`);  
  });

  socket.on("getout", (player) => {
    const index = players.value.indexOf(player)
    players.value.splice(index, 1)
    delete readyPlayers.value[player]
  });

});

</script>
<template>
  <div class="alert-message">
    {{ message }}
  </div>

  socketId : {{ socketId }}
  <div>ルームID : {{ roomId }}</div>
  <div v-if="!ready">
    <button @click="readyGame">準備完了</button>
  </div>
  <div v-if="ready">
    <button @click="cancelGame">一旦離席</button>
  </div>
  <button @click="getoutGame">退出</button>
  <div v-if="host == 'true'">
    <button @click="startGame" :disabled="!isButtonEnabled">ゲーム開始</button>
  </div>
  <ul>
    <li v-for="(player, index) in players" :key="index">
      Player{{ index + 1 }} : {{ player }} => {{ readyPlayers[player] }}
    </li>
  </ul>
</template>
<style>
.alert-message {
  color: red;
}
</style>

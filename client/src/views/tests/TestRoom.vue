<script setup>
import { onMounted, ref } from "vue";
import io from "socket.io-client";
import router from "@/router";

const socketId = ref("");
const playerName = ref("");
const joinType = ref(1);
const roomId = ref("");
const message = ref("");

const socket = io("http://localhost:8888");

const createRoom = () => {
  // sessionStorage.setItem("ready", true);
  sessionStorage.setItem("host", true);
  socket.emit("create_room", playerName.value);
  message.value = "";
};

const joinRoom = () => {
  // sessionStorage.setItem("ready", true);
  socket.emit("join_room", playerName.value, roomId.value);
  message.value = "";
};

onMounted(() => {
  socket.on("connect", () => {
    socketId.value = socket.id;
  });

  socket.on("notify_error", (error) => {
    message.value = error;
  });

  socket.on("player_joined", (player) => {
    console.log(player);
  });

  socket.on("update_room", (room) => {
    roomId.value = room.room_id;
    sessionStorage.setItem("socketId", socketId.value);
    message.value = "";

    router.push(`/test/room/${roomId.value}/waiting`);
  });
});
</script>
<template>
  <div id="app">
    <div class="alert-message">
      {{ message }}
    </div>

    socketId : {{ socketId }}
    <div>プレイヤー名 : <input v-model="playerName" type="text" /></div>

    <input type="radio" v-model="joinType" value="1" />ルーム作成
    <input type="radio" v-model="joinType" value="2" />ルーム参加

    <div v-if="joinType == 1">
      <button @click="createRoom">作成</button>
    </div>
    <div v-if="joinType == 2">
      <div>ルーム番号 : <input v-model="roomId" type="text" /></div>
      <button @click="joinRoom">参加</button>
    </div>
  </div>
</template>
<style scoped>
.alert-message {
  color: red;
}
</style>

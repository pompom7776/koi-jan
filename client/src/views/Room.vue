<script setup>
import { onMounted, ref } from "vue";
import io from "socket.io-client";
import router from "@/router";

const socketId = ref("");
const playerName = ref("");
const joinType = ref(null);
const roomId = ref("");
const message = ref("");

const socket = io("http://localhost:8888");

const createRoom = () => {
  sessionStorage.setItem("host", true);
  socket.emit("create_room", playerName.value);
  message.value = "";
};

const joinRoom = () => {
  socket.emit("join_room", playerName.value, roomId.value);
  message.value = "";
};

onMounted(() => {
  sessionStorage.setItem("host", false);

  socket.on("connect", () => {
    socketId.value = socket.id;
  });

  socket.on("notify_error", (error) => {
    message.value = error;
  });

  socket.on("player_joined", (player) => {
    console.log(player);
  });

  socket.on("update_room", (room_id) => {
    roomId.value = room_id;
    sessionStorage.setItem("socketId", socketId.value);
    message.value = "";

    router.push(`/room/${roomId.value}/waiting`);
  });
});
</script>

<template>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@800&display=swap"
    rel="stylesheet"
  />
  <div id="app">
    <img src="@/assets/koi-jan.png" alt="logo" />
    <div class="center">
      <div class="input-group">
        <input
          required
          placeholder="プレイヤー名"
          v-model="playerName"
          type="text"
          maxlength="8"
          id="playerName"
        />
      </div>
      <div class="radio-d">
        <label class="radio-button">
          <input type="radio" v-model="joinType" value="1" />
          ルーム作成
        </label>
        <label class="radio-button">
          <input type="radio" v-model="joinType" value="2" />
          ルーム参加
        </label>
      </div>
      <div v-if="joinType == 1" class="join1">
        <label class="radio-button">
          <input @click="createRoom" type="radio" />
          作成
        </label>
      </div>
      <div v-if="joinType == 2" class="join2">
        <input
          class="join2-input"
          required
          placeholder="ルーム番号"
          v-model="roomId"
          maxlength="4"
          type="text"
        />
        <label class="radio-button">
          <input @click="joinRoom" type="radio" />
          参加
        </label>
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
  background-image: url("@/assets/heartsimple59.png");
  color: rgb(12, 30, 58);
  font-family: "M PLUS Rounded 1c", sans-serif;
  flex-direction: column;
}

.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 600px;
  height: 350px;
  padding: 1rem;
  border: 10px solid rgba(107, 76, 83, 0.8);
  border-radius: 25px;
  background-color: #fff;
}

.input-group {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 1rem;
}

.input-group label {
  text-align: center;
  margin-bottom: 0.5rem;
}

input {
  outline: none;
  border: none;
  border-bottom: rgb(107, 76, 83, 0.8) solid 5px;
  padding-bottom: 5px;
  font-size: 1.5rem;
  font-family: "M PLUS Rounded 1c", sans-serif;
}

input::placeholder {
  color: rgb(107, 76, 83, 0.5);
}

img {
  width: 30vw;
  margin-bottom: 2vw;
}

.join1 {
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: center;
  margin: 0.6rem;
}

.join2 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 1rem;
}

.join2-input {
  margin-bottom: 16px;
}

.radio-d {
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: center;
  margin: 1rem;
  font-size: 20px;
}

.radio-button {
  display: inline-block;
  background-color: rgb(245, 196, 204);
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  user-select: none;
  margin: 5px;
  transition: 0.5s;
  font-size: 20px;
  border: 3px solid transparent;
}

.radio-button input[type="radio"] {
  display: none;
}

.radio-button:hover {
  background-color: rgb(254, 244, 242, 0.5);
  color: rgb(107, 76, 83, 0.8);
  transition: 0.5s;
  border: 3px solid rgb(107, 76, 83, 0.8);
}

/* To show the selected state */
.radio-button input[type="radio"]:checked + span {
  background-color: #2196f3;
  color: #fff;
}
</style>

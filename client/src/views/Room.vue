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
  socket.emit("enter_room", playerName.value, roomId.value);
  message.value = "";
};

const showPopup = ref(false); // ポップアップの表示状態を管理する変数

const openPopup = () => {
  showPopup.value = true;
};

const closePopup = () => {
  showPopup.value = false;
};

onMounted(() => {
  sessionStorage.setItem("host", false);

  socket.on("connected", () => {
    socketId.value = socket.id;
    sessionStorage.setItem("socketId", socketId.value);
  });

  socket.on("notify_error", (error) => {
    message.value = error;
  });

  socket.on("entered_room", (room_id) => {
    roomId.value = room_id;
    sessionStorage.setItem("socketId", socketId.value);
    message.value = "";

    router.push(`/room/${roomId.value}/waiting`);
  });
});
</script>

<template>
  <div id="app">
    <img class="logo-img" src="@/assets/koijan_1.png" alt="logo" />
    <div class="center">
      <div class="input-group">
        <input required placeholder="プレイヤー名" v-model="playerName" type="text" maxlength="8" id="playerName" />
      </div>
      <div class="radio-d">
        <label class="radio-button">
          <input @click="createRoom" type="radio" />
          ルーム作成
        </label>
        <label class="radio-button">
          <input @click="openPopup" type="radio" />
          ルーム参加
        </label>
      </div>
      <div v-if="showPopup" class="popup-overlay" @click="closePopup">
        <div class="popup-content" @click.stop>
          <div class="input-group">
            <input required placeholder="ルーム番号" v-model="roomId" maxlength="4" type="text" />
          </div>
          <button @click="joinRoom">参加する</button>
        </div>
      </div>
      <div v-if="joinType == 2" class="join2">
        <input class="join2-input" required placeholder="ルーム番号" v-model="roomId" maxlength="4" type="text" />
        <label class="radio-button">
          <input @click="enterRoom" type="radio" />
          参加
        </label>
      </div>
      <div class="date-image">
        <img src="@/assets/date-2.png" alt="date" />
      </div>
      <div class="date2-image">
        <img src="@/assets/date-3.png" alt="date" />
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
  /* background-image: url("@/assets/heartsimple59.png"); */

  background: linear-gradient(45deg,
      rgba(221, 214, 243, 0.5),
      rgba(250, 172, 168, 0.5),
      rgba(255, 252, 220, 0.5));
  background-size: 200% 200%;
  animation: bggradient 5s ease infinite;

  color: rgb(12, 30, 58);
  font-family: "M PLUS Rounded 1c", sans-serif;
  flex-direction: column;
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
  width: 600px;
  /* height: 350px; */
  padding: 1rem;
  /* border: 5px solid rgba(234, 56, 73, 0.8); */
  /* border-radius: 25px; */
  /* background-color: #fff; */
  margin-top: 30px;
}

.input-group {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 1rem;
  position: relative;
}

.input-group label {
  text-align: center;
  margin-bottom: 0.5rem;
}

input {
  outline: none;
  border: none;
  padding-bottom: 5px;
  font-size: 2rem;
  font-family: "M PLUS Rounded 1c", sans-serif;
  background: transparent;
  color: rgb(234, 56, 73, 0.8);
  width: 370px;
}

.input-group::after {
  content: "";
  position: absolute;
  bottom: -5px;
  /* 線を下にオフセットして要素内に配置 */
  left: 0;
  width: 100%;
  height: 5px;
  background-color: rgb(234, 56, 73, 0.8);
  border-radius: 5px;
}

input::placeholder {
  /* color: rgb(107, 76, 83, 0.5); */
  color: rgb(234, 56, 73, 0.8);
}

.logo-img {
  width: 400px;
  /* margin-bottom: 2vw; */
  opacity: 0.8;
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
  position: relative;
  /* 要素の位置を相対的に設定 */
}

.join2-input::before {
  content: "";
  position: absolute;
  top: -5px;
  /* 要素内の上部に線を配置 */
  left: 0;
  width: 100%;
  height: 5px;
  background-color: rgb(234, 56, 73, 0.8);
  /* 線色 */
  border-radius: 5px;
  /* 線幅の半分 */
}

.join2-input input {
  border: none;
  outline: none;
  background: transparent;
  font-size: 2rem;
  font-family: "M PLUS Rounded 1c", sans-serif;
  color: rgb(234, 56, 73, 0.8);
  width: 320px;
  padding-bottom: 10px;
  /* 下部の余白を追加 */
}

.join2-input input::placeholder {
  color: rgb(234, 56, 73, 0.8);
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
  background-color: rgb(234, 56, 73, 0.8);
  color: #fff;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
  user-select: none;
  margin: 20px 10px 5px 10px;
  transition: 0.5s;
  font-size: 20px;
  border: 3px solid transparent;
}

.radio-button input[type="radio"] {
  display: none;
}

.radio-button:hover {
  background-color: #fff;
  color: rgb(234, 56, 73, 0.8);
  transition: 0.5s;
  border: 3px solid rgb(234, 56, 73, 0.8);
}

/* To show the selected state */
.radio-button input[type="radio"]:checked+span {
  background-color: #2196f3;
  color: #fff;
}

.date-image {
  position: absolute;
  bottom: -5vh;
  right: -2vw;
  /* margin: 0px; */
}

.date-image img {
  width: 35vw;
  /* opacity: 0.8; */
}

.date2-image {
  position: absolute;
  bottom: -5vh;
  left: -1vw;
  /* margin: 0px; */
}

.date2-image img {
  width: 35vw;
  /* opacity: 0.8; */
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  z-index: 2;
}

.popup-content {
  background-color: #fff;
  padding: 70px 110px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.popup-content h2 {
  color: rgb(234, 56, 73, 0.8);
  font-size: 30px;
  margin-bottom: 20px;
}

.popup-input {
  width: 100%;
  padding: 5px;
  margin: 10px 0;
}

.popup-content button {
  display: inline-block;
  background-color: rgb(234, 56, 73, 0.8);
  color: #fff;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
  user-select: none;
  margin: 30px 10px 10px 10px;
  transition: 0.5s;
  font-size: 20px;
  border: 3px solid transparent;
  font-family: "M PLUS Rounded 1c", sans-serif;
}

.popup-content button:hover {
  background-color: #fff;
  color: rgb(234, 56, 73, 0.8);
  transition: 0.5s;
  border: 3px solid rgb(234, 56, 73, 0.8);
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  color: rgb(234, 56, 73, 0.8);
  text-decoration: none;
  cursor: pointer;
}
</style>

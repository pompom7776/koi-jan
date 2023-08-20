<script setup>
import io from "socket.io-client";
import { useRoute } from "vue-router";
import { computed, nextTick, onMounted, ref } from "vue";

const socket = io("http://localhost:8888");

const socketId = ref("");
const playerId = ref("");
const host = ref(false);

const roomId = ref("");
const route = useRoute();

const reactions = {1: "いいね", 2: "おこ", 3: "悲しい", 4: "最高", 5: "うぇい"}

onMounted(() => {
  playerId.value = sessionStorage.getItem("playerId");
  socketId.value = sessionStorage.getItem("socketId");
  host.value = sessionStorage.getItem("host");
  socket.emit("reconnect", socketId.value);
  socket.on("reconnected", (idInfo) => {
    sessionStorage.setItem("socketId", idInfo["sid"]);
    sessionStorage.setItem("playerId", idInfo["pid"]);
    socketId.value = sessionStorage.getItem("socketId");
  });
  roomId.value = route.params.roomId;

  socket.on("reacted", (reaction_info) => {
    var messageElement = document.getElementById("message");
    const player_id = reaction_info.player_id
    const reaction_number = reaction_info.reaction_number

    messageElement.textContent = `${player_id}が${reactions[reaction_number]}を押しました`;
    
  })
});

const Click_Sub = () => {
    const div1 = document.getElementById("div1");
    if (div1.style.display == "none") {
        div1.style.display = "block";
    } else {
        div1.style.display = "none";
    }
}

const showMessage = (reaction_number) => {
    socket.emit("reaction", roomId.value, reaction_number)
}
</script>

<template>
    <p id="message"></p>
    <button @click="Click_Sub">リアクションスタンプ</button>
    <div id="div1" style="display: none;" >
        <div v-for="num in Object.keys(reactions)">
            <button @click="showMessage(num)">{{ reactions[num] }}</button>
        </div>
    </div>
</template>

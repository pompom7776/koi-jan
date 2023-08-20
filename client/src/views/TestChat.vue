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

const inputMessage = ref("");
const messages = ref([]);


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
    
    socket.on("receiveMessage", (chats) => {
        messages.value = chats
    });
});
    
const sendMessage = () => {
    socket.emit("sendMessage", inputMessage.value);
    inputMessage.value = '';
};


</script>

<template>
    <h1>Chat</h1>
    <input v-model="inputMessage" type="text">
    <button @click="sendMessage()" :disabled="!inputMessage.length">Send</button>
    <div v-for="message in messages">
        <p>{{ message.player_id }}: {{ message.text }}</p>
    </div>
</template>
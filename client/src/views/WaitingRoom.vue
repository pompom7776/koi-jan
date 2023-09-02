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
const displayFlag = ref(true);

const chatFlag = ref(false);
const reactionFlag = ref(false);
const chatMessage = ref("");
const chats = ref([]);
const ruleFlag = ref(false);

const closeRule = () => {
  ruleFlag.value = false;
};
const currentRuleSection = ref(1);
const showPreviousRuleSection = () => {
      currentRuleSection.value = currentRuleSection.value === 1 ? 4 : currentRuleSection.value - 1;
    };
const showNextRuleSection = () => {
      currentRuleSection.value = currentRuleSection.value === 4 ? 1 : currentRuleSection.value + 1;
    };

const reloadDisplay = async () => {
displayFlag.value = false;
  await nextTick(() => {
    displayFlag.value = true;
  });
};

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
  router.push(`/room`);
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
</script><template>
  <div id="app">
    <div class="container" v-if="displayFlag">
      <div v-if="chatFlag">
        <div id="chat-container">
          <div id="messages-container">
            <div id="chat-header">
              <div id="chat-title">チャット</div>
              <a id="chat-close-btn" @click="chatFlag = false">×</a>
            </div>
            <div id="messages">
              <div v-for="chat in chats" :key="chat.id" class="message ms-left">
                <div class="sender-name">{{ chat.player_name }}</div>
                <div class="message-box">
                  <div class="message-content">
                    <div class="message-text">{{ chat.message }}</div>
                  </div>
                </div>
              </div>
              <div class="ms-clear"></div>
            </div>
            <div id="ms-send">
              <textarea id="send-message" v-model="chatMessage"></textarea>
              <button id="send-btn" @click="sendMessage">送信</button>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="reactionFlag">
        <div id="re-container">
          <div id="messages-container">
            <div id="chat-header">
              <div id="chat-title">スタンプ</div>
              <a id="chat-close-btn" @click="reactionFlag = false">×</a>
            </div>
            <div id="reaction">
              <div>
                <img src="/src/assets/face-happy.PNG" alt="face-happy">
                <img src="/src/assets/face-straight.PNG" alt="face-straight">
              </div>
              <div>
                <img src="/src/assets/face-beef.PNG" alt="face-beef">
                <img src="/src/assets/face-woah.PNG" alt="face-woah">
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="ruleFlag" class="ru-Flag">
        <img src="/src/assets/icons8-left.png" alt="left" @click="showPreviousRuleSection" class="chevron">
        <div id="ru-container">
          <div id="rule-header">
            <div id="rule-title">ルール説明</div>
            <div id="rule-close-btn" @click="ruleFlag = false">×</div>
          </div>
          <!-- ルール説明のセクション -->
          <div class="rule-div-sec">
            <div v-if="currentRuleSection === 1" id="rule1" class="rule1 ru-section">
              <ol>
                <li>勝利を目指してアガリを目指す</li>
                <li>手牌の中から3つの牌を選択</li>
              </ol>
              
            </div>
            <div v-else-if="currentRuleSection === 2" id="rule2" class="rule2 ru-section">
              <ol start="3">
                <li>選択した牌から理想のデートプランを考える</li>
                <li>作成した文章をチャットに送信</li>
              </ol>
            </div>
            <div v-else-if="currentRuleSection === 3" id="rule3" class="rule3 ru-section">
              <ol start="5">
                <li>一番キュンときた文章を作った人に投票</li>
                <li>麻雀点数 × 票数で点数が換算される</li>
              </ol>
            </div>
            <div v-else-if="currentRuleSection === 4" id="rule4" class="rule4 ru-section">
              <ol start="7">
                <li>4ラウンドやって最も点数が高い人が勝ち</li>
              </ol>
            </div>
          </div>
          <div class="dot-num">
            <ul>
              <li class="dot1" :class="{ 'active': currentRuleSection === 1 }"></li>
              <li class="dot2" :class="{ 'active': currentRuleSection === 2 }"></li>
              <li class="dot3" :class="{ 'active': currentRuleSection === 3 }"></li>
              <li class="dot4" :class="{ 'active': currentRuleSection === 4 }"></li>
            </ul>
          </div>
        </div>
        <img src="/src/assets/icons8-right.png" alt="right" @click="showNextRuleSection" class="chevron">
    </div>
      
    <div v-else class="fade-in">
      <div @click="reactionFlag= true" class="btn re-btn">スタンプ</div>
      <div @click="chatFlag= true" class="btn chat-btn">チャット</div>
      <div @click="ruleFlag = true" class="btn rule-btn">?</div>
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
          <img
            v-if="!readyPlayers[player]"
            src="@/assets/ready.png"
            alt="Pose NG Woman"
            class="ready"
          />
          <img
            v-if="readyPlayers[player]"
            src="@/assets/ready_go.png"
            alt="readygo"
            class="readygo"
          />
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
  </div>
</template>

<style scoped>
#app {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  /* background-image: url("@/assets/rose_wallpaper.jpg"); */
  background: linear-gradient(
    45deg,
    rgba(250, 208, 196, 0.5),
    rgba(255, 209, 255, 0.5),
    rgba(168, 237, 234, 0.5)
  );
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

button:checked + label {
  background-color: red;
}

img.ready {
  margin: -0px;
  width: 90%;
  height:55%;
  animation-name: fadeInAnime;
  animation-duration: 1s;
  animation-fill-mode: forwards;
  opacity: 0;
}

img.readygo {
  margin: 7px;
  width: 95%;
  height:50%;
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
  width: 23.5vw;
  max-width: 400px;
  position: fixed;
  top: 0%;
  right: 2%;
  animation-name: fadeInAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  /* opacity: 0; */
  z-index: 1;
}

#re-container{
  height: 40vh;
  width: 23.5vw;
  max-width: 400px;
  position: fixed;
  top: 0%;
  right: 2%;
  animation-name: fadeInAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  /* opacity: 0; */
  z-index: 1;
}

#ru-container {
  width: 50vw;
  height: 50vh;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  animation-name: fadeInAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  z-index: 10; /* 他の要素よりも手前に表示 */
  box-shadow: 0 2.5rem 2rem -2rem hsl(200 50% 20% / 40%);
  position: relative;
}
.ru-Flag{
  display:flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  font-family: "M PLUS Rounded 1c", sans-serif;
}

.chevron{
  width: 5vw;
  height: 8vh;
}
.dot-num {
  position: absolute; /* ドットを絶対位置に配置 */
  bottom: 10px; /* 下部からの位置調整（必要に応じて調整） */
  left: 50%; /* 左からの位置調整 */
  transform: translateX(-50%); /* 中央配置 */
}

/* 以下は前回のスタイルを維持 */
.dot-num ul {
  display: flex;
  list-style-type: none;
  padding: 0;
  justify-content: center;
}

.rule-div-sec ol{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.ru-section li{
  /* list-style: none; */
  /* position: absolute; */
  font-size: 2rem;
  color: #ffc3cd;
}

.dot-num li {
  width: 20px;
  height: 20px;
  background-color: #ffc0cb;
  border-radius: 50%;
  margin: 0.5vw;
  opacity: 0.3;
}

.dot-num li.active {
  opacity: 1;
}

#chat-close-container {
  position: fixed;
  width: 60px;
  height: 60px;
  bottom: 5%;
  right: 150px;
  background: #fff;
  border: 3.5px solid #efb0bb;
  border-radius: 50px;
  margin-right: 50px;
  animation-name: fadeInAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  /* opacity: 0; */
  cursor: pointer;
  z-index: 1;
}

#re-close-container {
  position: fixed;
  width: 60px;
  height: 60px;
  bottom: 5%;
  right: 230px;
  background: #fff;
  border: 3.5px solid #efb0bb;
  border-radius: 50px;
  margin-right: 50px;
  animation-name: fadeInAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  /* opacity: 0; */
  cursor: pointer;
  z-index: 1;
}

#messages-container {
  height: 100%;
  width: 100%;
}

#chat-header {
  padding: 6px 10px 6px 10px;
  font-size: 1.5rem;
  height: 5vh;
  background: #ffc0cb;
  border: 1px solid #ea384955;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#rule-header{
  padding: 10px;
  height: 5vh;
  font-size: 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #ffc3cd;
}

#chat-title {
  float: left;
  display: flex;
  justify-content: left;
  color: #fff;
}

#rule-tile{
  float: left;
  display: flex;
  justify-content: left;
  color: #fff;
}

#chat-close-btn{
  font-size: 2rem;
  cursor: pointer;
  position: absolute;
  top: 1px;
  right: 10px;
  color: #fff;
}

#rule-close-btn{
  font-size: 5rem;
  cursor: pointer;
  position: absolute;
  top: -2.5vh;
  right:2.5vw;
}

.chat-btn{
  position: absolute;
  top: 0px;
  right: 9.5vw;
  font-size: 1.5vw;
}
.re-btn{
  position: absolute;
  top: 0px;
  right: 18vw;
  font-size: 1.5vw;
}
.rule-btn{
  position: absolute;
  top: 0px;
  right: 1vw;
  font-size: 2rem;
}
.btn{
  width: 7vw;
  height: 5vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.62);
  border: 2px solid #ffc3cd;
  border-radius: 0px 0px 20px 20px;
  cursor: pointer;
  color:#ffc3cd;
}
.message-img{
  display: block;
  margin: 0 auto; 
  width: 3.5vw;
  height: 3.5vw; 
  position: absolute;
  top: 55%; 
  left: 50%;
  transform: translate(-50%, -50%); 
}

.face-img{
  display: block;
  margin: 0 auto; 
  width: 3.5vw;
  height: 3.5vw;
  position: absolute;
  top: 52%; 
  left: 50%;
  transform: translate(-50%, -50%); 
}

#messages {
  overflow: auto;
  height: 90%;
  border-right: 1px solid #ea384955;
  border-left: 1px solid #ea384955;
  background-color: #ffffffc1;
}

#reaction{
  overflow: auto;
  height: 90%;
  border-right: 1px solid #ea384955;
  border-left: 1px solid #ea384955;
  border-bottom: 1px solid #ea384955;
  background-color: #ffffffc1;
  border-radius: 0px 0px 10px 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

#reaction img{
  width: 8vw;
  height: 8vw;
  margin: 10px;
  display: block;
  cursor: pointer;
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
  height: 6vh;
  padding: 4px;
  border-radius: 0px 0px 10px 10px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

#send-message {
  resize: none;
  width: calc(100% - 75px);
  line-height: 16px;
  height: 41px;
  padding: 10px 6px 0px 6px;
  border: 1px solid #ea384955;
  border-radius: 8px;
  text-align: left;
  box-sizing: border-box;
}

#send-btn {
  width: 62px;
  height: 40px;
  font-size: 16px;
  float: right;
  background: #ffc3cd;
  text-align: center;
  padding: 5px 10px;
}

#send-btn:hover {
  background-color: #fff;
  color: #ffc3cd;
  transition: 0.5s;
  border: 2px solid #ffc3cd;
}
</style>

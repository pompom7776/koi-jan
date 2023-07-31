<script setup>
import { ref } from "vue";

const showModal = ref(false);

const openModal = () => {
    showModal.value = true;
};
const closeModal = () => {
    showModal.value = false;
};
</script>

<template>
    <div class="body">
        <div class="container">
            <div class="top-content content">
                <p>牌</p>
            </div>
            <div class="left-content content">
                <p>牌</p>
            </div>
            <div class="main-content"></div>
        <div class="right-content content">
            <p>牌</p>
            </div>
            <div class="bottom-content content">
                <p>牌</p>
            </div>
        <div class="center-content">
            <p>牌</p>
                <!-- 局・本場・順目・残り・東西南北・ドラ -->
            </div>
            <div class="top-discarded discarded">
                <p>test</p>
            <!-- <div class="tiles" v-for="tile in topPlayer.value.discarded_tiles">
                    <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                                    </div> -->
            </div>
            <div class="left-discarded discarded">
                <p>test</p>
            <!-- <div class="tiles" v-for="tile in leftPlayer.value.discarded_tiles">
                    <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                                    </div> -->
            </div>
            <div class="right-discarded discarded">
                <p>test</p>
                <!-- <div class="tiles" v-for="tile in rightPlayer.value.discarded_tiles">
                                        <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                                    </div> -->
            </div>
            <div class="bottom-discarded discarded">
                <p>test</p>
                <!-- <div class="tiles" v-for="tile in bottomPlayer.value.discarded_tiles">
                                        <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                                    </div> -->
            </div>
            <div class="all_direction">
                <div class="east-direction direction">
                    <img src="@/assets/east.png" alt="東" width="100%" height="100%" />
                    <p>名前</p>
                </div>
                <div class="south-direction direction">
                    <img src="@/assets/south.png" alt="東" width="100%" height="100%" />
                    <p>名前</p>
                </div>
                <div class="west-direction direction">
                    <img src="@/assets/west.png" alt="東" width="100%" height="100%" />
                    <p>名前</p>
                </div>
                <div class="north-direction direction">
                    <img src="@/assets/north.png" alt="東" width="100%" height="100%" />
                    <p>名前</p>
                </div>
            </div>
            <div class="all_button">
                <div class="button-container">
                    <button class="pon_button">ポン</button>
                    <button class="pon_button">スキップ</button>
                </div>
            </div>
        <button class="result-button" @click="openModal">Show Final Score</button>

            <!-- モーダルウィンドウ-->
            <div class="modal" :class="{ 'show-modal': showModal }">
                <div class="modal-content">
                    <span class="close-button" @click="closeModal">&times;</span>
                    <h2>Final Score Results</h2>
                    <!-- 簡易モーダルウィンドウ -->
                    <p>東家: 25000</p>
                    <p>南家: 25000</p>
                    <p>西家: 25000</p>
                    <p>北家: 25000</p>
                    <!-- <div v-for="(player, index) in sortedScoreResults" :key="index">
                                            <p :style="`font-size: ${14 - index}px`">{{ player.name }}: {{ player.score }}</p>
                                        </div> -->
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
    background-color: #444444;
    margin: 0;
}

.container {
    position: relative;
    width: 100vw;
    height: 56.25vw;
    background-image: url("@/assets/rose_wallpaper.jpg");
    background-size: cover;
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

.east-direction {
    top: 70%;
    left: 83%;
}

.south-direction {
    top: 76%;
    left: 20%;
}

.west-direction {
    top: 13%;
    left: 11%;
}

.north-direction {
    top: 13%;
    left: 73%;
}

img {
    width: 6vw;
}

.all_direction p {
    font-size: 1.5vw;
    color: #000;
    margin: 5px;
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
    align-items: center;
    background-color: #ffc3cd;
    border-radius: 20px;
}

.top-discarded {
    top: 32%;
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
    top: 68%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.content {
    position: absolute;
    width: 40%;
    height: 10%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 7px solid #ffc3cd;
    background-color: #fff;
    border-radius: 20px;
    font-size: 1.1vw;
}

.discarded {
    position: absolute;
    width: 30%;
    height: 10%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 1.1vw;
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

/* Style for the modal content */
.modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    max-width: 400px;
    width: 80%;
}

/* Style for the modal close button */
.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 1.5rem;
    cursor: pointer;
}
</style>

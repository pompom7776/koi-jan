<script>
export default {
    data() {
        return {
            selectedButton: null,
        };
    },
    methods: {
        selectButton(button) {
            this.selectedButton = button;
            // Add additional logic here if needed
        },
        // Your other methods and code here...
    },
};
</script>

<template>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@800&display=swap" rel="stylesheet" />
    <div class="body">
        <div class="container">
            <div class="top-content content">
                <p>牌</p>
            </div>
            <div class="left-content content">
                <p>牌</p>
            </div>
            <div class="main-content">
            </div>
            <div class="right-content content">
                <p>牌</p>
            </div>
            <div class="bottom-content content">
                <p>牌</p>
            </div>
            <div class="center-content">
                <div class="center-content">
                    <button class="button" :class="{ 'selected': selectedButton === '東' }" @click="selectButton('東')">東</button>
                    <button class="button" :class="{ 'selected': selectedButton === '西' }" @click="selectButton('西')">西</button>
                    <button class="button" :class="{ 'selected': selectedButton === '南' }" @click="selectButton('南')">南</button>
                    <button class="button" :class="{ 'selected': selectedButton === '北' }" @click="selectButton('北')">北</button>
                </div>
                <!-- 局・本場・順目・残り・東西南北・ドラ -->
            </div>
            <div class="all_direction">
                <div class="east-direction direction">
                    <img src="@/assets/east.png" alt="東" width="100%" height="100%">
                    <p>名前</p>
                </div>
                <div class="south-direction direction">
                    <img src="@/assets/south.png" alt="東" width="100%" height="100%">
                    <p>名前</p>
                </div>
                <div class="west-direction direction">
                    <img src="@/assets/west.png" alt="東" width="100%" height="100%">
                    <p>名前</p>
                </div>
                <div class="north-direction direction">
                    <img src="@/assets/north.png" alt="東" width="100%" height="100%">
                    <p>名前</p>
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
  font-family: "M PLUS Rounded 1c", sans-serif; 
}

.container {
  position: relative;
  width: 100vw;
  height: 56.25vw;
  background-image: url("@/assets/rose_wallpaper.jpg");
  background-size: cover;
}

.top-content{
    top: 10%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(180deg);
}
.left-content{
    top: 50%;
    left: 5%;
    transform: translate(-50%, -50%) rotate(90deg);
}
.main-content{
    position: absolute;
    z-index: 10000;
}
.right-content{
    top: 50%;
    left: 95%;
    transform: translate(-50%, -50%) rotate(-90deg);
}
.bottom-content{
    top: 90%;
    left: 50%;
    transform: translate(-50%, -50%);
}
.east-direction{
    top: 70%;
    left: 83%;
}
.south-direction{
    top: 76%;
    left: 20%;
}
.west-direction{
    top: 13%;
    left: 11%;
}
.north-direction{
    top: 13%;
    left: 73%;
}
img{
    width: 6vw;
}
.all_direction p{
    font-size: 1.5vw;
    color: #000;
    margin: 5px;
}
.center-content{
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    position: absolute;
    display: flex;
    flex-direction: row;
    justify-content: center;
    border-radius: 20px;
}
.top-discarded{
    top: 32%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(180deg);
}
.left-discarded{
    top: 50%;
    left: 33%;
    transform: translate(-50%, -50%) rotate(90deg);
}

.right-discarded{
    top: 50%;
    left: 67%;
    transform: translate(-50%, -50%) rotate(-90deg);
}

.bottom-discarded{
    top: 68%;
    left: 50%;
    transform: translate(-50%, -50%);
}
.content{
    position: absolute;
    width:40%;
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
.discarded{
    position: absolute;
    width: 30%;
    height: 10%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 1.1vw;
}

.direction{
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
    font-size: 2vw;
    border-radius: 5px;
    border: 3px solid transparent;
    background-color: #ffc3cd;
    color: #fff;
    padding: 1vw 3vw;
    cursor: pointer;
    user-select: none;
    margin: 2vw;
    transition: 0.5s;
    border-color:#fff;
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
.selected {
    /* Add styles for the selected button */
    background-color: rgb(254, 244, 242, 0.5);
    color: rgb(107, 76, 83, 0.8);
    border: 3px solid rgb(107, 76, 83, 0.8);
}

</style>
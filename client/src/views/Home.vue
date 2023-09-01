<template>
    <div id="app">
      <transition name="fade">
        <!-- loadingのみの画面 -->
        <div v-if="!showText" class="center">
          <div class="back"></div>
          <div class="heart-container">
            <transition-group name="heart-transition">
              <div v-for="(item, index) in heartItems" :key="index" class="heart" :class="{ heartgrow: item.grow }"></div>
            </transition-group>
          </div>
        </div>
        <div v-else id="container" class="fade-in">
            <!-- <img src="/src/assets/koijan_1.png" alt="logo" class="img-logo"> -->
            <div class="p-con">
                <p>恋愛 × 麻雀</p>
                <!-- <p>麻雀</p>
                <p>×</p>
                <p>恋愛</p> -->
            </div>
            <button @click="StartGamge">スタート</button>
            <img src="/src/assets/home-img.PNG" alt="home" class="img-home">
        </div>
      </transition>
    </div>
  </template>
  
  <script>
    import router from "../router";

  export default {
    data() {
      return {
        heartItems: [{ grow: false }],
        showText: false
      };
    },
    methods: {
      StartGamge() {
        router.push("/room");
      }
    },
    mounted() {
      // beatアニメーションが完了した後、grow-heartアニメーションを開始
      setTimeout(() => {
        this.heartItems[0].grow = true;
        setTimeout(() => {
          // 3秒後にloading画面を非表示にし、テキストを表示
          this.showText = true;
        }, 1000); // テキストの表示を1秒後に設定
      }, 3000);
    }
  };
  </script>
  
  <style scoped>
  .center {
    display: flex;
  }
  .back {
    position: fixed;
    padding: 0;
    margin: 0;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: white;
    animation-name: backdiv;
    animation-duration: 0.8s;
    animation-iteration-count: 3; /* 背景のアニメーションを3回繰り返す */
  }
  
  .heart-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  .heart {
  background-color: #ffc0cb;
  height: 50px;
  width: 50px;
  transform: rotate(-45deg);
  animation-name: beat;
  animation-duration: 0.8s;
  animation-iteration-count: 3; /* beatアニメーションを3回繰り返す */
}

.heartgrow {
  background-color: #ffc0cb;
  height: 50px;
  width: 50px;
  transform: rotate(-45deg);
  animation-name: grow-heart;
  animation-duration: 1s;
  animation-iteration-count: 1; /* grow-heartアニメーションは1回だけ再生 */
  animation-fill-mode: forwards; /* アニメーション終了時のスタイルを保持 */
}
  .heart:after,
  .heart:before {
    background-color: #ffc0cb;
    content: "";
    border-radius: 50%;
    position: absolute;
    width: 50px;
    height: 50px;
  }
  
  .heart:after {
    top: 0px;
    left: 25px;
  }
  
  .heart:before {
    top: -25px;
    left: 0px;
  }
  
  .heartgrow:after,
  .heartgrow:before {
    background-color: #ffc0cb;
    content: "";
    border-radius: 50%;
    position: absolute;
    width: 50px;
    height: 50px;
  }
  
  .heartgrow:after {
    top: 0px;
    left: 25px;
  }
  
  .heartgrow:before {
    top: -25px;
    left: 0px;
  }
  
  .text {
    position: absolute;
    top: 70px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 24px;
    font-weight: bold;
    display: none; /* 最初は非表示 */
    z-index: 1;
  }

  .fade-in {
  animation-name: fadeInAnime;
  animation-duration: 1.5s;
  animation-fill-mode: forwards; /* アニメーション終了時のスタイルを保持 */
}
  
  /* ハートの大きくなるアニメーションを定義 */
  @keyframes grow-heart {
    0% {
      transform: scale(1) rotate(-45deg);
    }
    100% {
      transform: scale(40) rotate(-45deg);
    }
  }
  
  @keyframes backdiv {
    50% {
      background: #ffe6f2;
    }
  }
  
  @keyframes beat {
  0% {
    transform: scale(1) rotate(-45deg);
  }
  50% {
    transform: scale(0.6) rotate(-45deg);
  }
}
@keyframes fadeInAnime {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
#container {
  /* loading画面後の表示のスタイルを定義 */
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.p-con{
    color: rgb(253, 243, 249);
    font-size: 4.5vw;
    font-family: "M PLUS Rounded 1c", sans-serif;
    position: absolute;
    /* top: 30%; */
    bottom: 13%;
    right: 7vw;
    z-index: 1;
}

.img-logo{
    width: 20vw;
    position: absolute;
    top: 15%;
    right: 2%;
    z-index: 1;
}

.img-home {
    width: 100vw;
    height: 56.25vw;
    object-fit: cover;
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0.9;
}

#container button{
    z-index: 1;
    position: absolute;
    width: 23vw;
    height: 8.5vh;
    bottom: 10%;
    right: 7%;
    background-color: rgb(253, 243, 249);
    color:rgb(243, 177, 188);
    border-radius: 10px;
    border: none;
    font-size: 3vw;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: "M PLUS Rounded 1c", sans-serif;
}

  </style>
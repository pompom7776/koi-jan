<script setup>
import { computed, onMounted, ref } from "vue";
import RiichiStickHorizontal from "@/components/parts/RiichiStickHorizontal.vue";
import PointStickHorizontal from "@/components/parts/PointStickHorizontal.vue";
import MahjongTile from "@/components/parts/MahjongTile.vue";

const tiles = [
  "1m",
  "2m",
  "3m",
  "4m",
  "5m",
  "6m",
  "7m",
  "8m",
  "9m",
  "1s",
  "2s",
  "3s",
  "4s",
  "5s",
  "6s",
  "7s",
  "8s",
  "9s",
  "1p",
  "2p",
  "3p",
  "4p",
  "5p",
  "6p",
  "7p",
  "8p",
  "9p",
  "east",
  "south",
  "west",
  "north",
  "white",
  "green",
  "red",
];

// テスト用
const getRandomTiles = (num) => {
  const randomTiles = [];
  while (randomTiles.length < num) {
    const randomIndex = Math.floor(Math.random() * tiles.length);
    const randomTile = tiles[randomIndex];
    tiles.splice(randomIndex, 0);

    randomTiles.push(randomTile);
  }
  return randomTiles;
};

// テスト用
sessionStorage.setItem("player_id", 1);

const playerId = sessionStorage.getItem("player_id");
const topPlayer = ref()
const leftPlayer = ref()
const rightPlayer = ref()
const bottomPlayer = ref()

const roundWind = ref("東");
const round = ref(1);
const riichiStickCount = ref(0);
const pointStickCount = ref(0);
const remainingTiles = ref(50);
const doraTiles = ref(["4m", "-", "-", "-", "-"]);
const scores = ref({ 東: 25000, 南: 25000, 西: 25000, 北: 25000 });
const seatWinds = ref({
  east: 1,
  south: 2,
  west: 3,
  north: 4,
});
const seatOrder = ["east", "south", "west", "north"];
const assignRelativeSeats = (mySeat) => {
  const relativeSeats = {};
  const myIndex = seatOrder.indexOf(mySeat);
  console.log("my", myIndex);

  relativeSeats.right =
    seatWinds.value[seatOrder[(myIndex + 1) % seatOrder.length]];
  relativeSeats.top =
    seatWinds.value[seatOrder[(myIndex + 2) % seatOrder.length]];
  relativeSeats.left =
    seatWinds.value[seatOrder[(myIndex + 3) % seatOrder.length]];

  return relativeSeats;
};

const getSeatByPlayerId = (playerId) => {
  for (const seat in seatWinds.value) {
    if (seatWinds.value[seat] == playerId) {
      return seat;
    }
  }
  return null;
};

const players = ref([
  {
    id: 1,
    name: "kita",
    hands: {
      tiles: [
        {
          id: 1,
          suit: "manzu",
          rank: 1,
          name: "1m",
          bonus: false,
        },
        {
          id: 5,
          suit: "manzu",
          rank: 2,
          name: "2m",
          bonus: false,
        },
        {
          id: 9,
          suit: "manzu",
          rank: 3,
          name: "3m",
          bonus: false,
        },
        {
          id: 61,
          suit: "pinzu",
          rank: 7,
          name: "7p",
          bonus: false,
        },
        {
          id: 65,
          suit: "pinzu",
          rank: 8,
          name: "8p",
          bonus: false,
        },
        {
          id: 69,
          suit: "pinzu",
          rank: 9,
          name: "9p",
          bonus: false,
        },
        {
          id: 109,
          suit: "wind",
          rank: 1,
          name: "east",
          bonus: false,
        },
        {
          id: 110,
          suit: "wind",
          rank: 1,
          name: "east",
          bonus: false,
        },
        {
          id: 111,
          suit: "wind",
          rank: 1,
          name: "east",
          bonus: false,
        },
        {
          id: 129,
          suit: "dragon",
          rank: 2,
          name: "green",
          bonus: false,
        },
      ],
      calls: [
        {
          type: "chi",
          tiles: [
            {
              id: 73,
              suit: "souzu",
              rank: 1,
              name: "1s",
              bonus: false,
            },
            {
              id: 77,
              suit: "souzu",
              rank: 2,
              name: "2s",
              bonus: false,
            },
            {
              id: 81,
              suit: "souzu",
              rank: 3,
              name: "3s",
              bonus: false,
            },
          ],
          from_tile: {
            tile: {
              id: 77,
              suit: "souzu",
              rank: 2,
              name: "2s",
              bonus: false,
            },
            player_id: 2,
          },
        },
      ],
      tsumo: {
        id: 130,
        suit: "dragon",
        rank: 2,
        name: "green",
        bonus: false,
      },
    },
    discardedTiles: getRandomTiles(10),
  },
  {
    id: 2,
    name: "pom",
    hands: {
      tiles: [
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
      ],
      calls: [
        {
          type: "chi",
          tiles: [
            {
              id: 73,
              suit: "souzu",
              rank: 1,
              name: "1s",
              bonus: false,
            },
            {
              id: 77,
              suit: "souzu",
              rank: 2,
              name: "2s",
              bonus: false,
            },
            {
              id: 81,
              suit: "souzu",
              rank: 3,
              name: "3s",
              bonus: false,
            },
          ],
          from_tile: {
            tile: {
              id: 77,
              suit: "souzu",
              rank: 2,
              name: "2s",
              bonus: false,
            },
            player_id: 1,
          },
        },
      ],
      tsumo: null,
    },
    discardedTiles: getRandomTiles(10),
  },

  {
    id: 3,
    name: "hwa",
    hands: {
      tiles: [
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
      ],
      calls: [
        {
          type: "chi",
          tiles: [
            {
              id: 73,
              suit: "souzu",
              rank: 1,
              name: "1s",
              bonus: false,
            },
            {
              id: 77,
              suit: "souzu",
              rank: 2,
              name: "2s",
              bonus: false,
            },
            {
              id: 81,
              suit: "souzu",
              rank: 3,
              name: "3s",
              bonus: false,
            },
          ],
          from_tile: {
            tile: {
              id: 77,
              suit: "souzu",
              rank: 2,
              name: "2s",
              bonus: false,
            },
            player_id: 1,
          },
        },
      ],
      tsumo: null,
    },
    discardedTiles: getRandomTiles(10),
  },
  {
    id: 4,
    name: "pen",
    hands: {
      tiles: [
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
        {
          id: 0,
          suit: "-",
          rank: 0,
          name: "-",
          bonus: false,
        },
      ],
      calls: [
        {
          type: "chi",
          tiles: [
            {
              id: 73,
              suit: "souzu",
              rank: 1,
              name: "1s",
              bonus: false,
            },
            {
              id: 77,
              suit: "souzu",
              rank: 2,
              name: "2s",
              bonus: false,
            },
            {
              id: 81,
              suit: "souzu",
              rank: 3,
              name: "3s",
              bonus: false,
            },
          ],
          from_tile: {
            tile: {
              id: 77,
              suit: "souzu",
              rank: 2,
              name: "2s",
              bonus: false,
            },
            player_id: 1,
          },
        },
      ],
      tsumo: null,
    },
    discardedTiles: getRandomTiles(10),
  },
]);

onMounted(() => {
  const mySeat = getSeatByPlayerId(playerId);
  const relativeSeats = assignRelativeSeats(mySeat);
  topPlayer.value = computed(() => players.value.find(player => player.id == relativeSeats["top"]))
  leftPlayer.value = computed(() => players.value.find(player => player.id == relativeSeats["left"]))
  rightPlayer.value = computed(() => players.value.find(player => player.id == relativeSeats["right"]))
  bottomPlayer.value = computed(() => players.value.find(player => player.id == playerId))
});
</script>
<template>
  <div class="body">
    <div class="container">
      <div class="top-content" v-if="topPlayer">
        <p>{{ topPlayer.value.name }} :</p>
        <div style="margin-left: 20px;">
          <p>手牌 :
          <div class="tiles">
            <div class="tiles" v-for="tile in topPlayer.value.hands.tiles">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" :isRedDora="tile.bonus" />
            </div>
            <div class="tsumo" v-if="topPlayer.value.hands.tsumo">
              <MahjongTile :tile="topPlayer.value.hands.tsumo.name" :scale="0.5" :rotate="0"
                :isRedDora="topPlayer.value.hands.tsumo.bonus" />
            </div>
          </div>
          </p>
          <p>鳴き :
          <div class="tiles" v-for="call in topPlayer.value.hands.calls">
            <div v-if="call.type == 'chi'">
              <div class="tiles" v-for="tile in call.tiles">
                <div v-if="call.from_tile.tile.id == tile.id">
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="90" />
                </div>
                <div v-else>
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                </div>
              </div>
            </div>
            <div v-if="call.type == 'pon'">
              ポン
            </div>
            <div v-if="call.type == 'kan'">
              カン
            </div>
          </div>
          </p>
          <p>河　 :
          <div class="tiles" v-for="tile in topPlayer.value.discardedTiles">
            <MahjongTile :tile="tile" :scale="0.5" :rotate="0" />
          </div>
          </p>
        </div>
      </div>
      <div class="left-content" v-if="leftPlayer">
        <p>{{ leftPlayer.value.name }} :</p>
        <div style="margin-left: 20px;">
          <p>手牌 :
          <div class="tiles">
            <div class="tiles" v-for="tile in leftPlayer.value.hands.tiles">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" :isRedDora="tile.bonus" />
            </div>
            <div class="tsumo" v-if="leftPlayer.value.hands.tsumo">
              <MahjongTile :tile="leftPlayer.value.hands.tsumo.name" :scale="0.5" :rotate="0"
                :isRedDora="leftPlayer.value.hands.tsumo.bonus" />
            </div>
          </div>
          </p>
          <p>鳴き :
          <div class="tiles" v-for="call in leftPlayer.value.hands.calls">
            <div v-if="call.type == 'chi'">
              <div class="tiles" v-for="tile in call.tiles">
                <div v-if="call.from_tile.tile.id == tile.id">
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="90" />
                </div>
                <div v-else>
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                </div>
              </div>
            </div>
            <div v-if="call.type == 'pon'">
              ポン
            </div>
            <div v-if="call.type == 'kan'">
              カン
            </div>
          </div>
          </p>
          <p>河　 :
          <div class="tiles" v-for="tile in leftPlayer.value.discardedTiles">
            <MahjongTile :tile="tile" :scale="0.5" :rotate="0" />
          </div>
          </p>
        </div>
      </div>
      <div class="main-content">
        <div>{{ roundWind }}{{ round }}局</div>
        <div>
          <RiichiStickHorizontal class="stick" :scale="0.5" />
          {{ riichiStickCount }}
        </div>
        <div>
          <PointStickHorizontal class="stick" :scale="0.5" />
          {{ pointStickCount }}
        </div>
        <div>残り牌数: {{ remainingTiles }}</div>
        <div class="tiles" v-for="tile in doraTiles">
          <MahjongTile :tile="tile" :scale="0.5" :rotate="0" />
        </div>
        <div v-for="(v, k) in scores">{{ k }}: {{ v }}</div>
      </div>
      <div class="right-content" v-if="rightPlayer">
        <p>{{ rightPlayer.value.name }} :</p>
        <div style="margin-left: 20px;">
          <p>手牌 :
          <div class="tiles">
            <div class="tiles" v-for="tile in rightPlayer.value.hands.tiles">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" :isRedDora="tile.bonus" />
            </div>
            <div class="tsumo" v-if="rightPlayer.value.hands.tsumo">
              <MahjongTile :tile="rightPlayer.value.hands.tsumo.name" :scale="0.5" :rotate="0"
                :isRedDora="rightPlayer.value.hands.tsumo.bonus" />
            </div>
          </div>
          </p>
          <p>鳴き :
          <div class="tiles" v-for="call in rightPlayer.value.hands.calls">
            <div v-if="call.type == 'chi'">
              <div class="tiles" v-for="tile in call.tiles">
                <div v-if="call.from_tile.tile.id == tile.id">
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="90" />
                </div>
                <div v-else>
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                </div>
              </div>
            </div>
            <div v-if="call.type == 'pon'">
              ポン
            </div>
            <div v-if="call.type == 'kan'">
              カン
            </div>
          </div>
          </p>
          <p>河　 :
          <div class="tiles" v-for="tile in rightPlayer.value.discardedTiles">
            <MahjongTile :tile="tile" :scale="0.5" :rotate="0" />
          </div>
          </p>
        </div>
      </div>
      <div class="bottom-content" v-if="bottomPlayer">
        <p>{{ bottomPlayer.value.name }} :</p>
        <div style="margin-left: 20px;">
          <p>手牌 :
          <div class="tiles">
            <div class="tiles" v-for="tile in bottomPlayer.value.hands.tiles">
              <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" :isRedDora="tile.bonus" />
            </div>
            <div class="tsumo" v-if="bottomPlayer.value.hands.tsumo">
              <MahjongTile :tile="bottomPlayer.value.hands.tsumo.name" :scale="0.5" :rotate="0"
                :isRedDora="bottomPlayer.value.hands.tsumo.bonus" />
            </div>
          </div>
          </p>
          <p>鳴き :
          <div class="tiles" v-for="call in bottomPlayer.value.hands.calls">
            <div v-if="call.type == 'chi'">
              <div class="tiles" v-for="tile in call.tiles">
                <div v-if="call.from_tile.tile.id == tile.id">
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="90" />
                </div>
                <div v-else>
                  <MahjongTile :tile="tile.name" :scale="0.5" :rotate="0" />
                </div>
              </div>
            </div>
            <div v-if="call.type == 'pon'">
              ポン
            </div>
            <div v-if="call.type == 'kan'">
              カン
            </div>
          </div>
          </p>
          <p>河　 :
          <div class="tiles" v-for="tile in bottomPlayer.value.discardedTiles">
            <MahjongTile :tile="tile" :scale="0.5" :rotate="0" />
          </div>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.tiles {
  display: inline-block;
}

.tsumo {
  display: inline-block;
  margin-left: 20px;
}

.body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #444444;
}

.container {
  width: 100vw;
  max-width: 160vh;
  height: 56.25vw;
  background-color: #f0f0f0;
  display: grid;
  grid-template-rows: 1fr 1.5fr 1fr;
  grid-template-columns: 1fr 1.5fr 1fr;
  font-size: calc(0.5vw);
}

.top-content {
  grid-row: 1;
  grid-column: 2;
  border: 1px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
}

.left-content {
  grid-row: 2;
  grid-column: 1;
  border: 1px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
}

.main-content {
  grid-row: 2;
  grid-column: 2;
}

.right-content {
  grid-row: 2;
  grid-column: 3;
  border: 1px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
}

.bottom-content {
  grid-row: 3;
  grid-column: 2;
  border: 1px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";
import Room from "../views/Room.vue";
import WaitingRoom from "../views/WaitingRoom.vue";
import Game from "../views/Game.vue";
import TestHome from "../views/tests/TestHome.vue";
import TestRoom from "../views/tests/TestRoom.vue";
import TestWaitingRoom from "../views/tests/TestWaitingRoom.vue";
import TestGame from "../views/tests/TestGame.vue";
import TestSandbox from "../views/tests/TestSandbox.vue";
import ga_design from "../views/Game_design.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/room", component: Room },
  { path: "/room/:roomId/waiting", component: WaitingRoom },
  { path: "/room/:roomId/game", component: Game },
  { path: "/test", component: TestHome },
  { path: "/test/room", component: TestRoom },
  { path: "/test/room/:roomId/waiting", component: TestWaitingRoom },
  { path: "/test/room/:roomId/game", component: TestGame },
  { path: "/test/sandbox", component: TestSandbox },
  { path: "/ga_design", component: ga_design },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;

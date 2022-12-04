import {createRouter, createWebHistory} from "vue-router";
import Home from '@/views/Home.vue'
import ChessBoard from '@/views/ChessBoard.vue'
import Ping from '@/views/Ping.vue';

const routes = [
    {path: '/', name: 'Home', component: Home},
    {path: '/ping', name: 'Ping', component: Ping},
    {path: '/chessboard', name: 'ChessBoard', component: ChessBoard}
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})
export default router;
import {createRouter, createWebHistory} from "vue-router";
import Home from '@/views/Home.vue'
import Ping from '@/views/Ping.vue';

const routes = [
    {path: '/', name: 'Home', component: Home},
    {path: '/ping', name: 'Ping', component: Ping}
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})
export default router;
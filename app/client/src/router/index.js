import {createRouter, createWebHistory} from "vue-router";
import Chess from "@/views/Chess.vue";

const routes = [
    {path: '/', name: 'Chess', component: Chess},
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})
export default router;
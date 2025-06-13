// src/router/index.ts

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('@/views/Home.vue'),
    },
    {
        path: '/demo',
        name: 'demo',
        // ✨ 修改：将 /demo 路由指向 Demo.vue，以便直接测试
        component: () => import('@/views/Demo-test5-refresh4.vue')
    },
    // {
    //     path: '/enhance',
    //     name: 'enhance',
    //     component: () => import('../../old_files/Enhance2.vue'),
    // },
    {
        path: '/about',
        name: 'about',
        component: () => import('@/views/About.vue')
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
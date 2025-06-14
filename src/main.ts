// src/main.ts (唯一入口文件)

import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import naive from 'naive-ui'

// 所有的 import 语句都应该放在文件顶部
import 'vfonts/Lato.css'
import 'vfonts/FiraCode.css'
import './assets/main.css'

const app = createApp(App)

// 依次注册插件
app.use(router)
app.use(naive)

// 最后挂载应用
app.mount('#app')
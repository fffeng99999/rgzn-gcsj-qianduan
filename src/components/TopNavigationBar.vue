
<template>
  <n-layout-header bordered class="header">
    <!-- Logo区域 -->
    <n-flex align="center">
      <n-icon size="40" :component="GameController" />
    </n-flex>

    <!-- 导航按钮区域 -->
    <n-flex align="center" class="nav-links">
      <n-button
          v-for="item in navItems"
          :key="item.path"
          text
          size="large"
          class="nav-button"
          :class="{ 'active-nav': route.path === item.path }"
          @click="router.push(item.path)"
      >
        {{ item.label }}
      </n-button>
    </n-flex>

    <div class="spacer" />

    <!-- 工具栏区域 -->
    <n-flex align="center">
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-button circle quaternary @click="toggleTheme">
            <template #icon>
              <n-icon>
                <component :is="isDark ? WeatherSunny20Filled : DarkTheme20Filled" />
              </n-icon>
            </template>
          </n-button>
        </template>
        切换至{{ isDark ? '亮色' : '暗色' }}模式
      </n-tooltip>

      <n-dropdown trigger="click" :options="dropdownOptions" @select="handleSelect">
        <n-avatar
            round
            size="medium"
            src="https://em-content.zobj.net/source/telegram/386/face-with-raised-eyebrow_1f928.webp"
            style="cursor: pointer;"
        />
      </n-dropdown>
    </n-flex>
  </n-layout-header>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import { inject, h } from 'vue';
import {
  NLayoutHeader, NButton, NFlex, NIcon, NTooltip, NAvatar, NDropdown, useMessage
} from 'naive-ui';
import {
  DarkTheme20Filled, WeatherSunny20Filled, Person16Filled, Settings16Filled, SignOut20Filled
} from '@vicons/fluent';
import { GameController } from '@vicons/ionicons5';

const isDark = inject('isDark');
const toggleTheme = inject('toggleTheme');
const message = useMessage();
const router = useRouter();
const route = useRoute();

// ✅ 导航项数组统一管理
const navItems = [
  { label: '首页', path: '/' },
  { label: '演示', path: '/demo' },
  // { label: '增强', path: '/enhance' },
  { label: '关于', path: '/about' }
];

const renderIcon = (icon) => () => h(NIcon, null, { default: () => h(icon) });

const dropdownOptions = [
  { label: '个人中心', key: 'profile', icon: renderIcon(Person16Filled) },
  { label: '设置', key: 'settings', icon: renderIcon(Settings16Filled) },
  { type: 'divider', key: 'd1' },
  { label: '退出登录', key: 'logout', icon: renderIcon(SignOut20Filled) }
];

const handleSelect = (key) => {
  message.info(`点击了选项，key: ${key}`);
};
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: var(--card-color);
  border-bottom: 1px solid var(--border-color);
  padding: 0 20px;
  height: 64px;
  display: flex;
  align-items: center;
}

.nav-links {
  margin-left: 16px;
}

.spacer {
  flex-grow: 1;
}

.nav-button {
  font-weight: 500;
  margin: 0 4px;
  padding: 6px 12px;
  border-radius: 6px;
  background-color: transparent !important;
  transition: all 0.3s ease-in-out;
}

.nav-button:hover {
  background-color: var(--n-color-embedded) !important;
}

.nav-button.active-nav {
  color: var(--n-primary-color);
  font-weight: 600;
  background-color: var(--n-color-embedded) !important;
}
</style>

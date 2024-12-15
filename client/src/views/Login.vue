<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import useUserStore from "../stores/UserStore";
import axios from "axios";

// import VueCookies from 'vue-cookies';  // Добавляем импорт

const username = ref("");
const pass = ref("");

const userStore = useUserStore();
const router = useRouter();

// Проверка, вошел ли пользователь в систему
const isLoggedIn = computed(() => {
  return userStore.isAuthenticated; // Используем isAuthenticated из userStore
});

async function login() {
  let token = $cookies.get("csrftoken");
  console.log(token);
// async function login() {
//   let token = VueCookies.get("csrftoken");  // Используем VueCookies для получения токена
//   console.log(token);

  try {
    const response = await axios.post(
      "/api/users/login/",
      {
        user: username.value,
        pass: pass.value,
      },
      {
        headers: {
          "X-CSRFToken": token,
        },
      }
    );
    await userStore.fetchUser();
    router.push("/");
  } catch (error) {
    console.error("Ошибка при входе:", error);
  }
}

async function logout() {
  try {
    await axios.get("/api/users/logout/");
    await userStore.fetchUser();
    router.push("/users");
  } catch (error) {
    console.error("Ошибка при выходе:", error);
  }
}
</script>

<template>
  <div class="container mt-5">
    <!--<h1 class="text-center">Вход</h1>-->
    <form v-if="!isLoggedIn" @submit.prevent="login" class="w-50 mx-auto">
      <h1 class="text-center">Вход</h1>
      <div class="mb-3">
        <label for="username" class="form-label">Имя пользователя:</label>
        <input type="text" class="form-control" id="username" v-model="username" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Пароль:</label>
        <input type="password" class="form-control" id="password" v-model="pass" required />
      </div>
      <button type="submit" class="btn btn-outline-dark w-100">Войти</button>
    </form>

    <form v-else @submit.prevent="logout" class="w-50 mx-auto">
      <h1 class="text-center">Выход</h1>
      <button type="submit" class="btn btn-outline-danger w-100">Выйти</button>
    </form>
  </div>
</template>

<style scoped>
</style>

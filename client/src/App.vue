<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import useUserStore from "@/stores/UserStore";
import axios from "axios"

const userStore = useUserStore();
const router = useRouter();

// Проверка, вошел ли пользователь в систему
const isLoggedIn = computed(() => userStore.isAuthenticated);

async function logout() {
  try {
    await userStore.fetchUser(); // Обновляем информацию о пользователе
    await userStore.logout();   // Выход
    router.push("/users");      // Перенаправляем на страницу входа
  } catch (error) {
    console.error("Ошибка при выходе:", error);
  }
}

async function exportCars() {
  try {
    const response = await axios.get('/api/cars/export/', {
      responseType: 'blob', // Получаем файл в виде бинарных данных
    });

    // Создаем ссылку для скачивания
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'ReportischeCars.xlsx'); // Устанавливаем имя файла
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link); // Удаляем ссылку после скачивания
  } catch (error) {
    console.error('Ошибка при экспорте данных:', error);
  }
}
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">
          JDM
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-beetween" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                Автомобили
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/drives">
                Типы приводов
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/engines">
                Типы двигателей
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/bodys">
                Типы кузовов
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/transmissions">
                Типы КПП
              </router-link>
            </li>
            <li class="nav-item">
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button"
                data-bs-toggle="dropdown" aria-expanded="false">
                Ещё
              </a>
              <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                <li><a class="dropdown-item" href="/admin"> Админка</a></li>
                <li><a class="dropdown-item" href="/important">Важно</a></li>
                <li v-if="isLoggedIn" class="nav-item">
                  <a href="#" class="dropdown-item text-danger" @click.prevent="logout"> Выход</a>
                </li>
                <li v-else class="nav-item">
                  <a class="dropdown-item text-primary" href="/users">Войти</a>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/users">
                {{ userStore.username }}
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <div class="container">
    <router-view />
  </div>

  <footer class="row row-cols-1 row-cols-sm-2 row-cols-md-5 pt-5 mt-5 border-top">
    <div class="col mb-3 mx-5">
      <p class="text-body-secondary mt-5">JDM © 2024</p>
    </div>

    <div class="col mb-3">
      <h5>Навигация</h5>
      <ul class="nav flex-column">
        <li class="nav-item mb-2">
          <router-link class="nav-link p-0 text-body-secondary" to="/">
            Автомобили
          </router-link>
        </li>
        <li class="nav-item mb-2">
          <router-link class="nav-link p-0 text-body-secondary" to="/drives">
            Типы приводов
          </router-link>
        </li>
        <li class="nav-item mb-2">
          <router-link class="nav-link p-0 text-body-secondary" to="/engines">
            Типы двигателей
          </router-link>
        </li>
        <li class="nav-item mb-2">
          <router-link class="nav-link p-0 text-body-secondary" to="/bodys">
            Типы кузовов
          </router-link>
        </li>
        <li class="nav-item mb-2">
          <router-link class="nav-link p-0 text-body-secondary" to="/transmissions">
            Типы КПП
          </router-link>
        </li>
      </ul>
    </div>

    <div class="col mb-3">
      <h5>О сайте</h5>
      Данный сайт повествует об автокультуре Японии 2000-х годов, а так же об обобщённых технических характеристиках
      автомобилей.
    </div>

    <div class="col mb-3 mx-4">
      <h5>Скачать в Excel-файл</h5>
      <ul class="nav flex-column">
        <button class="btn btn-outline-success" @click="exportCars">Тык</button>
      </ul>
    </div>


    <!--<div class="col mb-3">
            <h5>Section</h5>
            <ul class="nav flex-column">
                <li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">Home</a></li>
                <li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">Features</a></li>
                <li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">Pricing</a></li>
                <li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">FAQs</a></li>
                <li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">About</a></li>
            </ul>
        </div>-->
  </footer>
</template>

<style scoped>
footer {
    width: 100%; 
    overflow-x: hidden; 
}

.container, .row, .col {
    /*outline: 1px solid red;*/ /* Для отладки */
}
</style>
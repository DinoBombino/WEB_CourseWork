<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie';
// import { useUserStore } from "../stores/UserStore";
// import { useUserStore } from "@/stores/UserStore";

// const userStore = useUserStore();
// const users = ref([]);
// const selectedUser = ref("");
// const isSuperuser = ref(false);
// import { useUserStore } from '@/stores/UserStore';
// import useUserStore from "../stores/UserStore";

// const selectedUserFilter = ref("current");
// const { users } = useUserStore();
// const { users, isAuthenticated, userId, isAdmin } = useUserStore();

/////////////
const carsStats = ref(null); // Для хранения статистики

async function fetchStats() {
  try {
    const response = await axios.get("/api/cars/stats/");
    carsStats.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке статистики:", error);
  }
}
///////////

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const cars = ref([]);
const drives = ref([]);
const enginetypes = ref([]);
const bodytypes = ref([]);
const transmissiontypes = ref([]);
const loading = ref(false);

const carsPictureRef = ref();
const carAddImageUrl = ref();
const carEditImageUrl = ref();
const carsEditPictureRef = ref();
const selectedPicture = ref(null);  // для хранения выбранной картинки

const filter = ref(null); // Переменная для фильтрации, например, по user_id


async function fetchCars() {
    loading.value = true;

    const r = await axios.get("/api/cars/", {
        params: {
            user_id: filter === "all" ? null : filter,
            // user_id: userId,
        }
    });
    console.log(r.data)
    cars.value = r.data;
    loading.value = false;
}

async function fetchDrives() {
    loading.value = true;
    const r = await axios.get("api/drives/");
    console.log(r.data)
    drives.value = r.data;
    loading.value = false;
}

async function fetchEngines() {
    loading.value = true;
    const r = await axios.get("api/enginetypes/");
    console.log(r.data)
    enginetypes.value = r.data;
    loading.value = false;
}

async function fetchBodys() {
    loading.value = true;
    const r = await axios.get("api/bodytypes/");
    console.log(r.data)
    bodytypes.value = r.data;
    loading.value = false;
}

async function fetchTransmissions() {
    loading.value = true;
    const r = await axios.get("api/transmissiontypes/");
    console.log(r.data)
    transmissiontypes.value = r.data;
    loading.value = false;
}

async function carsAddPictureChange() {
    carAddImageUrl.value = URL.createObjectURL(carsPictureRef.value.files[0])
}

async function carsEditPictureChange() {
    carEditImageUrl.value = URL.createObjectURL(carsEditPictureRef.value.files[0])
}

async function onLoadClick() {
    await fetchCars()
}


onBeforeMount(async () => {
    await fetchDrives()
    await fetchCars()
    await fetchEngines()
    await fetchBodys()
    await fetchTransmissions()
    await fetchStats()
})


const carToAdd = ref({});
const carToEdit = ref({});

async function onCarAdd() {
    const formData = new FormData();

    formData.append('picture', carsPictureRef.value.files[0]);

    formData.set('name', carToAdd.value.name)
    formData.set('drive', carToAdd.value.drive)
    formData.set('etype', carToAdd.value.etype)
    formData.set('btype', carToAdd.value.btype)
    formData.set('trtype', carToAdd.value.trtype)

    await axios.post("/api/cars/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
        // ...carToAdd.value,
    });
    await fetchCars(); // переподтягиваю
}

async function onRemoveClick(car) {
    await axios.delete(`/api/cars/${car.id}/`);
    await fetchCars(); // переподтягиваю
}

async function onCarEditClick(car) {
    console.log(car)
    carToEdit.value = { ...car, drive: car.drive.id, etype: car.etype.id, btype: car.btype.id, trtype: car.trtype.id };
}

async function onUpdateCar() {
    const formData = new FormData();

    if (carsEditPictureRef.value.files[0]) {
        formData.append('picture', carsEditPictureRef.value.files[0]);
    }
    formData.set('name', carToEdit.value.name)
    formData.set('drive', carToEdit.value.drive)
    formData.set('etype', carToEdit.value.etype)
    formData.set('btype', carToEdit.value.btype)
    formData.set('trtype', carToEdit.value.trtype)

    await axios.put(`/api/cars/${carToEdit.value.id}/`, formData, {
        // ...carToEdit.value,

        headers: {
            'Content-Type': 'multipart/form-data'
        },
        drive: carToEdit.value.drive,
        etype: carToEdit.value.etype,
        btype: carToEdit.value.btype,
        trtype: carToEdit.value.trtype
    });
    await fetchCars();
}

function openImageModal(image) {
    selectedPicture.value = image;  // сохраняем картинку в переменную
}
</script>

<template>
    <div v-if="loading">Чё-та грузим, а чё грузим и куда - секрет</div>
    <!--########################Add#######################-->
    <!-- ТУТ ПОДКЛЮЧИЛ обработчик отправки формы -->
    <form @submit.prevent.stop="onCarAdd" class="p-3">
        <div class="row g-3">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="carToAdd.name" required placeholder=" " />
                    <label for="floatingInput">Название</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <select class="form-select" v-model="carToAdd.drive" required>
                        <option value="" disabled selected>Выберите привод</option>
                        <option :value="d.id" v-for="d in drives">{{ d.name }}</option>
                    </select>
                    <label for="floatingSelect">Привод</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <select class="form-select" v-model="carToAdd.etype" required>
                        <option value="" disabled selected>Выберите тип двигателя</option>
                        <option :value="e.id" v-for="e in enginetypes">{{ e.etype }}</option>
                    </select>
                    <label for="floatingSelect">Тип двигателя</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <select class="form-select" v-model="carToAdd.btype" required>
                        <option value="" disabled selected>Выберите тип кузова</option>
                        <option :value="b.id" v-for="b in bodytypes">{{ b.btype }}</option>
                    </select>
                    <label for="floatingSelect">Тип кузова</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <select class="form-select" v-model="carToAdd.trtype" required>
                        <option value="" disabled selected>Выберите тип КПП</option>
                        <option :value="tr.id" v-for="tr in transmissiontypes">{{ tr.trtype }}</option>
                    </select>
                    <label for="floatingSelect">Тип КПП</label>
                </div>
            </div>
            <div class="col-12 d-flex justify-content-between">
                <input class="form-control w-50" type="file" ref="carsPictureRef" @change="carsAddPictureChange" />
                <button class="btn btn-outline-dark">Добавить</button>
            </div>
            <div class="col">
                <img :src="carAddImageUrl" style="max-height: 60px;" alt="">
            </div>
        </div>
    </form>

    <!--########################Delete#######################-->
    <div class="modal fade" id="editCarModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header border-0">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактировать {{ carToEdit.name }}
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    <div class="row g-3">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="carToEdit.name"
                                    placeholder="Название" />
                                <label for="carName">Название</label>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="form-floating">
                                <select class="form-select" v-model="carToEdit.drive" id="driveSelect">
                                    <option :value="d.id" v-for="d in drives" :key="d.id">{{ d.name }}</option>
                                </select>
                                <label for="driveSelect">Привод</label>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="form-floating">
                                <select class="form-select" v-model="carToEdit.etype" id="engineTypeSelect">
                                    <option :value="e.id" v-for="e in enginetypes" :key="e.id">{{ e.etype }}</option>
                                </select>
                                <label for="engineTypeSelect">Тип двигателя</label>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="form-floating">
                                <select class="form-select" v-model="carToEdit.btype" id="bodyTypeSelect">
                                    <option :value="b.id" v-for="b in bodytypes" :key="b.id">{{ b.btype }}</option>
                                </select>
                                <label for="bodyTypeSelect">Тип кузова</label>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="form-floating">
                                <select class="form-select" v-model="carToEdit.trtype" id="transmissionTypeSelect">
                                    <option :value="tr.id" v-for="tr in transmissiontypes" :key="tr.id">{{ tr.trtype }}
                                    </option>
                                </select>
                                <label for="transmissionTypeSelect">Тип КПП</label>
                            </div>
                        </div>

                        <div class="col-12 mb-2">
                            <div class="form-floating">
                                <input type="file" class="form-control" @change="carsEditPictureChange"
                                    ref="carsEditPictureRef" />
                                <!--<input type="file" class="form-control" id="carImage" @change="onImageChange" accept="image/*" />-->
                            </div>
                        </div>

                        <div class="col-12 mb-2 text-center">
                            <img v-if="carToEdit.picture" :src="carToEdit.picture" class="img-fluid rounded"
                                style="max-height: 200px;" alt="" />
                        </div>
                    </div>
                </div>

                <div class="modal-footer border-0">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-outline-success" @click="onUpdateCar"
                        data-bs-dismiss="modal">Сохранить</button>
                </div>
            </div>
        </div>
    </div>

    <!--Карточка машинки-->
    <div class="row">
        <div v-for="item in cars" class="col-md-4 mb-2">
            <div class="card h-100 shadow-sm border "> <!-- Добавлен класс border -->
                <div class="card-body">
                    <h5 class="card-title text-dark fw-bold">{{ item.name }}</h5>

                    <!--<div v-show="item.picture" class="text-center mb-3">
                        <img :src="item.picture" class="rounded" style="max-height: 200px; max-width: 100%;" alt="">
                    </div>-->

                    <div v-show="item.picture" class="text-center mb-3">
                        <img :src="item.picture" class="rounded"
                            style="max-height: 200px; max-width: 100%; cursor: pointer;" alt=""
                            @click="openImageModal(item.picture)" />
                    </div>


                    <p class="card-text">
                        <span class="d-block">Тип двигателя: <strong>{{ item.etype.etype }}</strong></span>
                        <span class="d-block">Привод: <strong>{{ item.drive.name }}</strong></span>
                        <span class="d-block">Тип кузова: <strong>{{ item.btype.btype }}</strong></span>
                        <span class="d-block">Тип КПП: <strong>{{ item.trtype.trtype }}</strong></span>
                    </p>

                    <div class="mt-3 d-flex justify-content-between">
                        <button class="btn btn-outline-success btn-sm" @click="onCarEditClick(item)"
                            data-bs-toggle="modal" data-bs-target="#editCarModal">
                            <i class="bi bi-pencil"></i> Edit
                        </button>
                        <button class="btn btn-outline-danger btn-sm" @click="onRemoveClick(item)">
                            <i class="bi bi-x"></i> Remove
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Модальное окно -->
    <div v-if="selectedPicture" class="modal fade show d-block" id="imageModal" tabindex="-1" style="display: block;">
        <div class="modal-dialog modal-fullscreen">
            <div class="modal-content">
                <div class="modal-header">
                    <h6 class="modal-title">Просмотр картинки</h6>
                    <button type="button" class="btn-close" @click="selectedPicture = null" aria-label="Close"></button>
                </div>
                <div class="modal-body text-center">
                    <img :src="selectedPicture" class="img-fluid" style="max-height: 655px; width: auto;" />
                </div>
                <!--<div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary"
                        @click="selectedPicture = null">Закрыть</button>
                </div>-->
            </div>
        </div>
    </div>

    <!--#####################################################-->
    <div>
        <!--<div v-for="item in cars">
      {{ item.name }}
    </div>-->

        <!--<div v-for="item in drives">
      {{ item.name }}
    </div>-->

        <!--<div v-for="item in enginetypes">
      {{ item.etype }}
    </div>-->

        <!--<button @click="onLoadClick">Загрузить</button>-->

        <!-- Блок статистики -->
        <div class="stats">
            <h2>Статистика автомобилей</h2>
            <div v-if="carsStats" class="stats-grid">
                <div class="stat-card">
                    <h3>Общее количество автомобилей</h3>
                    <p>{{ carsStats.total_cars }}</p>
                </div>
                <div class="stat-card">
                    <h3>Типы привода</h3>
                    <p>{{ carsStats.total_drives }}</p>
                </div>
                <div class="stat-card">
                    <h3>Типы двигателей</h3>
                    <p>{{ carsStats.total_engine_types }}</p>
                </div>
                <div class="stat-card">
                    <h3>Типы кузовов</h3>
                    <p>{{ carsStats.total_body_types }}</p>
                </div>
                <div class="stat-card">
                    <h3>Типы трансмиссий</h3>
                    <p>{{ carsStats.total_transmission_types }}</p>
                </div>
            </div>
            <div v-else>
                <p>Загрузка статистики...</p>
            </div>
        </div>


    </div>
</template>

<style scoped>
/* Стили для блока статистики */
.stats {
  margin-top: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
}

/* Сетка карточек */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

/* Карточка для статистики */
.stat-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 8px;
}

.stat-card p {
  font-size: 1.6rem;
  font-weight: bold;
  color: #343638;
}
/* Модальное окно во весь экран */
.modal-dialog.modal-fullscreen {
    max-width: 100%;
    width: 100%;
    margin: 0;
    height: 100%;
    max-height: 100%;
}

img.img-fluid {
    object-fit: contain;
}
</style>
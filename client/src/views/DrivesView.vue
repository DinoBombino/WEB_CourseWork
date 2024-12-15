<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie';

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const cars = ref([]);
const drives = ref([]);
const enginetypes = ref([]);
const bodytypes = ref([]);
const transmissiontypes = ref([]);
const loading = ref(false);

const drivesPictureRef = ref();
const driveAddImageUrl = ref();
const driveEditImageUrl = ref();
const drivesEditPictureRef = ref();
const selectedPicture = ref(null);  // для хранения выбранной картинки

async function fetchCars() {
    loading.value = true;
    const r = await axios.get("api/cars/");
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

async function drivesAddPictureChange() {
    driveAddImageUrl.value = URL.createObjectURL(drivesPictureRef.value.files[0])
}

async function drivesEditPictureChange() {
    driveEditImageUrl.value = URL.createObjectURL(drivesEditPictureRef.value.files[0])
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
})

const driveToAdd = ref({});
const driveToEdit = ref({});

async function onDriveAdd() {
    const formData = new FormData();

    formData.append('picture', drivesPictureRef.value.files[0]);

    formData.set('name', driveToAdd.value.name)
    formData.set('description', driveToAdd.value.description)
    
    // formData.set('drive', driveToAdd.value.drive)
    // formData.set('etype', driveToAdd.value.etype)
    // formData.set('btype', driveToAdd.value.btype)
    // formData.set('trtype', driveToAdd.value.trtype)

    await axios.post("/api/drives/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
        // ...driveToAdd.value,
    });
    await fetchDrives(); // переподтягиваю
}

async function onRemoveClick(drive) {
    await axios.delete(`/api/drives/${drive.id}/`);
    await fetchDrives(); // переподтягиваю
}

async function onDriveEditClick(drive) {
    console.log(drive)
    driveToEdit.value = { ...drive/*, description: drive.id*/ };
}

async function onUpdateDrive() {
    const formData = new FormData();

    if (drivesEditPictureRef.value.files[0])
    {
        formData.append('picture', drivesEditPictureRef.value.files[0]);
    }
    formData.set('name', driveToEdit.value.name)
    formData.set('description', driveToEdit.value.description)
 

    await axios.put(`/api/drives/${driveToEdit.value.id}/`, formData, {
        // ...driveToEdit.value,
        
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        drive: driveToEdit.value.description,
        
    });
    await fetchDrives();
}

function openImageModal(image) {
    selectedPicture.value = image;  // сохраняем картинку в переменную
}
</script>
<template>
    <div v-if="loading">Чё-та грузим, а чё грузим и куда - секрет</div>
    <div><h1>Приводы</h1></div>
    <form @submit.prevent.stop="onDriveAdd" class="p-3">
        <div class="row g-3">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="driveToAdd.name" required placeholder=" " />
                    <label for="floatingInput">Название</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="driveToAdd.description" required placeholder=" " />
                    <label for="floatingInput">Описание</label>
                </div>
            </div>            
            <div class="col-12 d-flex justify-content-between">
                <input class="form-control w-50" type="file" ref="drivesPictureRef" @change="drivesAddPictureChange" />
                <button class="btn btn-outline-dark">Добавить</button>
            </div>
            <div class="col">
                <img :src="driveAddImageUrl" style="max-height: 60px;" alt="">
            </div>
        </div>
    </form>

    <!--########################Delete#######################-->
    <div class="modal fade" id="editCarModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header border-0">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактировать {{ driveToEdit.name }}
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    <div class="row g-3">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="driveToEdit.name"
                                    placeholder="Название" />
                                <label for="carName">Название</label>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="driveToEdit.description"
                                    placeholder="Название" />
                                <label for="driveSelect">Описание</label>
                            </div>
                        </div>

                        <div class="col-12 mb-2">
                            <div class="form-floating">
                                <input type="file" class="form-control" @change="drivesEditPictureChange"
                                    ref="drivesEditPictureRef" />
                                <!--<input type="file" class="form-control" id="carImage" @change="onImageChange" accept="image/*" />-->
                            </div>
                        </div>

                        <div class="col-12 mb-2 text-center">
                            <img v-if="driveToEdit.picture" :src="driveToEdit.picture" class="img-fluid rounded"
                                style="max-height: 200px;" alt="" />
                        </div>
                    </div>
                </div>

                <div class="modal-footer border-0">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-outline-success" @click="onUpdateDrive"
                        data-bs-dismiss="modal">Сохранить</button>
                </div>
            </div>
        </div>
    </div>

    <!--Карточка машинки-->
    <div class="row">
        <div v-for="item in drives" class="col-md-14 ms-2 mb-2">
            <div class="card h-100 shadow-sm border "> 
                <div class="card-body">
                    <h5 class="card-title text-dark fw-bold">{{ item.name }}</h5>

                    <!--<div v-show="item.picture" class="text-center mb-3">
                        <img :src="item.picture" class="rounded" style="max-height: 360px; max-width: 100%;" alt="">
                    </div>-->

                    <div v-show="item.picture" class="text-center mb-3">
                        <img :src="item.picture" class="rounded"
                            style="max-height: 360px; max-width: 100%; cursor: pointer;" alt=""
                            @click="openImageModal(item.picture)" />
                    </div>

                    <p class="card-text">
                        <!--<span class="d-block">Привод: <strong>{{ item.drive.name }}</strong></span>-->
                        <span class="d-block">Описание: {{ item.description }}</span>
                    </p>

                    <div class="mt-3 d-flex justify-content-between">
                        <button class="btn btn-outline-success btn-sm" @click="onDriveEditClick(item)"
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
                    <h5 class="modal-title">Просмотр картинки</h5>
                    <button type="button" class="btn-close" @click="selectedPicture = null" aria-label="Close"></button>
                </div>
                <div class="modal-body text-center">
                    <img :src="selectedPicture" class="img-fluid" style="max-height: 90vh; width: auto;"
                        alt="Увеличенная картинка" />
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="selectedPicture = null">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
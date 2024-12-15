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

const enginesPictureRef = ref();
const engineAddImageUrl = ref();
const engineEditImageUrl = ref();
const enginesEditPictureRef = ref();
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

async function enginesAddPictureChange() {
    engineAddImageUrl.value = URL.createObjectURL(enginesPictureRef.value.files[0])
}

async function enginesEditPictureChange() {
    engineEditImageUrl.value = URL.createObjectURL(enginesEditPictureRef.value.files[0])
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

const engineToAdd = ref({});
const engineToEdit = ref({});

async function onEngineAdd() {
    const formData = new FormData();

    formData.append('picture', enginesPictureRef.value.files[0]);

    formData.set('etype', engineToAdd.value.etype)
    formData.set('description', engineToAdd.value.description)
    
    // formData.set('drive', engineToAdd.value.drive)
    // formData.set('etype', engineToAdd.value.etype)
    // formData.set('btype', engineToAdd.value.btype)
    // formData.set('trtype', engineToAdd.value.trtype)

    await axios.post("/api/enginetypes/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
        // ...engineToAdd.value,
    });
    await fetchEngines(); // переподтягиваю
}

async function onRemoveClick(etype) {
    await axios.delete(`/api/enginetypes/${etype.id}/`);
    await fetchEngines(); // переподтягиваю
}

async function onEngineEditClick(etype) {
    console.log(etype)
    engineToEdit.value = { ...etype/*, description: drive.id*/ };
}

async function onUpdateEngine() {
    const formData = new FormData();

    if (enginesEditPictureRef.value.files[0])
    {
        formData.append('picture', enginesEditPictureRef.value.files[0]);
    }
    formData.set('etype', engineToEdit.value.etype)
    formData.set('description', engineToEdit.value.description)
 

    await axios.put(`/api/enginetypes/${engineToEdit.value.id}/`, formData, {
        // ...engineToEdit.value,
        
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        etype: engineToEdit.value.description,
        
    });
    await fetchEngines();
}

function openImageModal(image) {
    selectedPicture.value = image;  // сохраняем картинку в переменную
}
</script>
<template>
    <div v-if="loading">Чё-та грузим, а чё грузим и куда - секрет</div>
    <div><h1>Двигатели</h1></div>
    <form @submit.prevent.stop="onEngineAdd" class="p-3">
        <div class="row g-3">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="engineToAdd.etype" required placeholder=" " />
                    <label for="floatingInput">Название</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="engineToAdd.description" required placeholder=" " />
                    <label for="floatingInput">Описание</label>
                </div>
            </div>            
            <div class="col-12 d-flex justify-content-between">
                <input class="form-control w-50" type="file" ref="enginesPictureRef" @change="enginesAddPictureChange" />
                <button class="btn btn-outline-dark">Добавить</button>
            </div>
            <div class="col">
                <img :src="engineAddImageUrl" style="max-height: 60px;" alt="">
            </div>
        </div>
    </form>

    <!--########################Delete#######################-->
    <div class="modal fade" id="editCarModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header border-0">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактировать {{ engineToEdit.etype }}
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    <div class="row g-3">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="engineToEdit.etype"
                                    placeholder="Название" />
                                <label for="carName">Название</label>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="engineToEdit.description"
                                    placeholder="Название" />
                                <label for="driveSelect">Описание</label>
                            </div>
                        </div>

                        <div class="col-12 mb-2">
                            <div class="form-floating">
                                <input type="file" class="form-control" @change="enginesEditPictureChange"
                                    ref="enginesEditPictureRef" />
                                <!--<input type="file" class="form-control" id="carImage" @change="onImageChange" accept="image/*" />-->
                            </div>
                        </div>

                        <div class="col-12 mb-2 text-center">
                            <img v-if="engineToEdit.picture" :src="engineToEdit.picture" class="img-fluid rounded"
                                style="max-height: 200px;" alt="" />
                        </div>
                        
                    </div>
                </div>

                <div class="modal-footer border-0">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-outline-success" @click="onUpdateEngine"
                        data-bs-dismiss="modal">Сохранить</button>
                </div>
            </div>
        </div>
    </div>

    <!--Карточка машинки-->
    <div class="row">
        <div v-for="item in enginetypes" class="col-md-14 ms-2 mb-2">
            <div class="card h-100 shadow-sm border "> 
                <div class="card-body">
                    <h5 class="card-title text-dark fw-bold">{{ item.etype }}</h5>

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
                        <button class="btn btn-outline-success btn-sm" @click="onEngineEditClick(item)"
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
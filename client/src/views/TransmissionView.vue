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

const trmsPictureRef = ref();
const trmAddImageUrl = ref();
const trmEditImageUrl = ref();
const trmsEditPictureRef = ref();
// const selectedPicture = ref(null);  // для хранения выбранной картинки

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

async function trmsAddPictureChange() {
    trmAddImageUrl.value = URL.createObjectURL(trmsPictureRef.value.files[0])
}

async function trmsEditPictureChange() {
    trmEditImageUrl.value = URL.createObjectURL(trmsEditPictureRef.value.files[0])
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

const trmToAdd = ref({});
const trmToEdit = ref({});

async function onTrmAdd() {
    const formData = new FormData();

    formData.append('picture', trmsPictureRef.value.files[0]);

    formData.set('trtype', trmToAdd.value.trtype)
    formData.set('description', trmToAdd.value.description)

    await axios.post("/api/transmissiontypes/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
        // ...trmToAdd.value,
    });
    await fetchTransmissions(); // переподтягиваю
}

async function onRemoveClick(trtype) {
    await axios.delete(`/api/transmissiontypes/${trtype.id}/`);
    await fetchTransmissions(); // переподтягиваю
}

async function onTrmEditClick(trtype) {
    console.log(trtype)
    trmToEdit.value = { ...trtype/*, description: drive.id*/ };
}

async function onUpdateTransmission() {
    const formData = new FormData();

    if (trmsEditPictureRef.value.files[0])
    {
        formData.append('picture', trmsEditPictureRef.value.files[0]);
    }
    formData.set('trtype', trmToEdit.value.trtype)
    formData.set('description', trmToEdit.value.description)
 

    await axios.put(`/api/transmissiontypes/${trmToEdit.value.id}/`, formData, {
        // ...trmToEdit.value,
        
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        trtype: trmToEdit.value.description,
        
    });
    await fetchTransmissions();
}
</script>
<template>
    <div v-if="loading">Чё-та грузим, а чё грузим и куда - секрет</div>
    <div><h1>КПП</h1></div>
    <form @submit.prevent.stop="onTrmAdd" class="p-3">
        <div class="row g-3">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="trmToAdd.trtype" required placeholder=" " />
                    <label for="floatingInput">Название</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="trmToAdd.description" required placeholder=" " />
                    <label for="floatingInput">Описание</label>
                </div>
            </div>            
            <div class="col-12 d-flex justify-content-between">
                <input class="form-control w-50" type="file" ref="trmsPictureRef" @change="trmsAddPictureChange" />
                <button class="btn btn-outline-dark">Добавить</button>
            </div>
            <div class="col">
                <img :src="trmAddImageUrl" style="max-height: 60px;" alt="">
            </div>
        </div>
    </form>

    <!--########################Delete#######################-->
    <div class="modal fade" id="editCarModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header border-0">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактировать {{ trmToEdit.trtype }}
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    <div class="row g-3">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="trmToEdit.trtype"
                                    placeholder="Название" />
                                <label for="carName">Название</label>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="trmToEdit.description"
                                    placeholder="Название" />
                                <label for="driveSelect">Описание</label>
                            </div>
                        </div>

                        <div class="col-12 mb-2">
                            <div class="form-floating">
                                <input type="file" class="form-control" @change="trmsEditPictureChange"
                                    ref="trmsEditPictureRef" />
                                <!--<input type="file" class="form-control" id="carImage" @change="onImageChange" accept="image/*" />-->
                            </div>
                        </div>

                        <div class="col-12 mb-2 text-center">
                            <img v-if="trmToEdit.picture" :src="trmToEdit.picture" class="img-fluid rounded"
                                style="max-height: 200px;" alt="" />
                        </div>
                    </div>
                </div>

                <div class="modal-footer border-0">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-outline-success" @click="onUpdateTransmission"
                        data-bs-dismiss="modal">Сохранить</button>
                </div>
            </div>
        </div>
    </div>

    <!--Карточка машинки-->
    <div class="row">
        <div v-for="item in transmissiontypes" class="col-md-14 ms-2 mb-2">
            <div class="card h-100 shadow-sm border "> 
                <div class="card-body">
                    <h5 class="card-title text-dark fw-bold">{{ item.trtype }}</h5>

                    <div v-show="item.picture" class="text-center mb-3">
                        <img :src="item.picture" class="rounded" style="max-height: 360px; max-width: 100%;" alt="">
                    </div>

                    <p class="card-text">
                        <!--<span class="d-block">Привод: <strong>{{ item.drive.name }}</strong></span>-->
                        <span class="d-block">Описание: {{ item.description }}</span>
                    </p>

                    <div class="mt-3 d-flex justify-content-between">
                        <button class="btn btn-outline-success btn-sm" @click="onTrmEditClick(item)"
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
</template>

<style scoped>

</style>
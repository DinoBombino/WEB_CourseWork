import { onBeforeMount, ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

export const useUserStore = defineStore("UserStore", () => {
  const isAuthenticated = ref(false);
  const username = ref("");
  const userId = ref();
  //////////////////////
  const users = ref([]);
  //////////////////////

  async function fetchUser() {
    const r = await axios.get("/api/users/info/");
    isAuthenticated.value = r.data.is_authenticated;
    username.value = r.data.username;
    userId.value = r.data.user_id;
  }

  ////////////////////////
  async function fetchUsers() {
    try {
      const response = await axios.get("/api/users/info/");
      users.value = response.data; 
    } catch (error) {
      console.error("Ошибка при загрузке пользователей:", error);
    }
  }
  ///////////////////////

  onBeforeMount(() => {
    fetchUser();
    fetchUsers();
  });

  ////////////
  async function logout() {
    try {
      await axios.get("/api/users/logout/");
      isAuthenticated.value = false;
      username.value = "";
      userId.value = null;
    } catch (error) {
      console.error("Ошибка при выходе:", error);
    }
  }
  ///////////

  return {
    isAuthenticated,
    username,
    userId,
    fetchUser,
    logout,
    users, 
    fetchUsers, 
  };
});

export default useUserStore;
<template>
  <section class="home">
    <h1>Welcome</h1>

    <select class="select" v-model="selectedUser">
      <option :value="null" disabled>Selecciona un usuario</option>
      <option v-for="user in users" :value="user" :key="user.id">
        {{ user.user_name }}
      </option>
    </select>
    <button class="btn" @click="onButtonClicked">Ver eventos</button>
  </section>
</template>


<script>
import config from "@/config.js";
export default {
  data() {
    return {
      users: [],
      selectedUser: null,
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      let endpoint = `${config.API_PATH}/users`;
      let response = await fetch(endpoint);
      let loadData = await response.json();
      this.users = loadData;
    },
    onButtonClicked() {
      localStorage.userId = this.selectedUser.id;
      localStorage.userName = this.selectedUser.user_name;
      this.$router.push("/events");
    },
  },
};
</script>


<style scoped>
.home {
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
h1 {
  font-style: italic;
  font-size: 3rem;
}
.select {
  margin-top: 1rem;
  border: 2px solid transparent;
  border-radius: 5px;
  background: #7df5a5;
  box-shadow: 0px 0px 4px black;
  height: 1.5rem;
  width: 15rem;
  transition: 0.1s ease-in-out;
}
/* .select:hover {
  cursor: pointer;
} */
button {
  margin-top: 2rem;
}
.btn {
  margin-top: 1rem;
  border: 2px solid transparent;
  border-radius: 5px;
  background: #4bfa85;
  box-shadow: 0px 0px 4px black;
  height: 2rem;
  width: 15rem;
  transition: 0.1s ease-in-out;
}
/* .btn:hover {
  background: rgb(61, 58, 58);
  color: #42b983;
} */
</style>

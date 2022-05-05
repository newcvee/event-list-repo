<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/events">Events</router-link>
    <p class="user">{{ loggedUser }}</p>
  </div>
  <router-view />
</template>

<script>
export default {
  data() {
    return {
      loggedUser: localStorage.userName,
    };
  },
};
</script>
<style scoped>
#nav {
  background-color: #3eb466;
  align-content: center;
  top: 0px;
  height: 50%;
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.user {
  text-decoration: none;
  position: absolute;
  float: right;
  color: rgb(46, 42, 42) !important;
}
</style>

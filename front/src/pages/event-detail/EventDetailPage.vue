<template>
  <section class="events-main">
    <h1>Detalles del evento</h1>
    <h2>{{ event.name }}</h2>
    <p>{{ event.description }}</p>
    <p>{{ event.date }}</p>
    <p>{{ event.time }}</p>
    <ul v-for="cat in event.categories" :key="cat.id">
      <li>
        {{ cat.category_name }}
      </li>
    </ul>

    <p>{{ changeStatus(event.public) }}</p>

    <button
      class="btn"
      @click="onButtonClicked"
      v-show="loggedUser === event.user_id"
    >
      Modificar
    </button>
    <router-link to="/events" @click="removeEventInside"
      ><button class="btn btn-delete" v-show="loggedUser === event.user_id">
        Eliminar
      </button></router-link
    >
  </section>
</template>
<script>
import { getCategory, loadData, removeEventInside } from "@/services/api.js";
export default {
  name: "events",
  data() {
    return {
      loggedUser: localStorage.userId,
      event: {},
      categories: [],
    };
  },
  mounted() {
    this.loadData();
    this.getCategory();
  },
  methods: {
    changeStatus(status) {
      if (status === 0) {
        return "No Público";
      } else {
        return "Público";
      }
    },
    async getCategory() {
      this.categories = await getCategory();
    },
    getCategoryNameById(categoryId) {
      const result = this.categories
        .filter((c) => c.category_id == categoryId)
        .map((c) => c.category_name)[0];
      return result;
    },
    formatDate(targetEvent) {
      var datePart = targetEvent.date.match(/\d+/g),
        year = datePart[0].substring(0);
      let month = datePart[1];
      let day = datePart[2];
      month = config.months[month];
      targetEvent.date = `${day}-${month}-${year}`;
      return targetEvent;
    },

    async loadData() {
      let eventId = this.$route.params.id;
      this.event = await loadData(eventId);
    },
    onButtonClicked() {
      this.$router.push("/events/modify/" + this.$route.params.id);
    },
    async removeEventInside() {
      let removeEvent = this.$route.params.id;
      await removeEventInside(removeEvent);
    },
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}
.events-main {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  background: rgb(241, 237, 237);
  box-shadow: 0px 0px 8px rgb(184, 181, 181);
  border-radius: 10px;
  font-size: larger;
  color: rgb(34, 34, 34);
  font-family: Montserrat;
  margin: 30px;
  padding: 1em 0;
}
.events-main h2 {
  color: #02c242;
  font-weight: bold;
  text-transform: capitalize;
}
.events-main p {
  max-width: 80%;
}

/* .btn-delete:hover {
  background: rgb(61, 58, 58);
  box-shadow: 0px 0px 9px #ff3c00;
  color: #ff3c00;
  font-size: 1.25rem;
  font-weight: bold;
} */
</style>
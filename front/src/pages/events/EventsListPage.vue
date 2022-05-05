<template>
  <main class="events-main">
    <div>
      <button class="btn btn-add-event" @click="addNewEventClicked">
        ➕ Añadir Evento
      </button>
      <button class="btn-calendar" @click="onCalendarClicked">
        Calendario
      </button>
    </div>
    <button class="filtersButton" @click="onsidebarClicked">filtrar</button>
    <section v-if="showSidebar">
      <div class="filters">
        <form
          action="http://localhost:5000/api/orderedevents"
          method="get"
          class="form"
        >
          <ul class="btn-radio">
            <label
              ><input
                type="radio"
                name="filtros"
                value="allEvents"
                @click="allEvents"
              />Todas</label
            >
            <label
              ><input
                type="radio"
                name="filtros"
                value="filterByMonth"
                @click="filterByMonth"
              />Mes</label
            >

            <label
              ><input
                type="radio"
                name="filtros"
                value="filterByDay"
                @click="filterByDay"
              />Dia</label
            >
            <!-- <label
              ><input
                type="radio"
                name="filtros"
                value="filterByPublics"
                @click="filterByPublics"
              />Publicos</label
            > -->
            <label
              ><input
                type="radio"
                name="filtros"
                value="filterFromToday"
                @click="filterFromToday"
                checked
              />Desde hoy en adelante</label
            >
          </ul>

          <ul>
            <p>Filtra entre fechas:</p>
            <li>De <input type="date" v-model="dateFrom" /></li>
            <li>
              A
              <input
                type="date"
                v-model="dateTo"
                @change="getEventsBetweenTwoDates(dateFrom, dateTo)"
              />
            </li>
          </ul>

          <label>
            <!-- <div class="category-filter">
              <p class="category-text">Filtrar por categorias</p>
              <input type="checkbox" id="checkbox" v-model="checkedCategory" />
              <select
                class="category-select"
                name="filtros"
                v-model="selectedCategory"
              >
                <option
                  v-for="category in categories"
                  :key="category.category_id"
                  :value="category.category_id"
                >
                  {{ category.category_name }}
                </option>
              </select>
            </div> -->
            <div>
              <label
                ><input
                  type="checkbox"
                  name="filtros"
                  value="filterByPublics"
                  v-model="checkedPublic"
                />Publicos</label
              >
            </div>
          </label>
        </form>
      </div>
    </section>
    <section class="events-container">
      <article
        class="event"
        v-for="event in filteredData"
        :key="event.id"
        :style="{ backgroundColor: event.public ? 'darker' : 'snow' }"
      >
        <div class="text-article">
          <h2>{{ event.name }}</h2>
          <p>{{ event.date }}</p>
          <p>{{ event.time }}</p>
          <p>{{ getCategoryNameById(event.category_id) }}</p>
        </div>
        <section class="loggedInfo">
          <h1 v-if="event.public === 0">Privado</h1>
          <h1 v-else>Público</h1>
          <p>{{ getNameByUserId(event.user_id) }}</p>
          <p
            class="emogiDetail"
            @click="openEventDetail(event)"
            v-show="loggedUser === event.user_id"
          >
            ➕
          </p>
          <p
            class="emogiDelete"
            @click="removeEvent(event)"
            v-show="loggedUser === event.user_id"
          >
            🗑
          </p>
        </section>
      </article>
    </section>
  </main>
</template>

<script>
import config from "@/config.js";
import {
  getEventsBetweenTwoDates,
  loadUser,
  fetchApi,
  fetchAllEvents,
  getCategory,
  removeEvent,
  fetchMonthApiEventList,
  fetchFromTodayEvents,
  fetchPublicEvents,
} from "@/services/api.js";

export default {
  name: "events",
  data() {
    return {
      loggedUser: localStorage.userId,
      clicked: false,
      categories: [],
      eventList: [],
      users: [],
      dateFrom: "",
      result2: [],
      result: [],
      result2: [],
      dateTo: "",
      isShowingWeekEvents: "",
      nowCurrentDate: "",
      selectedCategory: "",
      checkedCategory: "",
      checkedPublic: "",
      users: [],
      showSidebar: false,
    };
  },
  mounted() {
    this.loadData();
    this.getCategory();
    this.loadUser();
  },
  methods: {
    getNameByUserId(userId) {
      const result2 = this.users
        .filter((u) => u.id == userId)
        .map((u) => u.user_name)[0];
      return result2;
    },

    onsidebarClicked() {
      this.showSidebar = !this.showSidebar;
    },

    formatDate(events) {
      let formatedEventList = [];
      for (let target_event of events) {
        if (target_event.date != "") {
          let datePart = target_event.date.match(/\d+/g),
            year = datePart[0];
          let month = datePart[1];
          let day = datePart[2];
          month = config.months[month];
          target_event.date = `${day}-${month}-${year}`;
        }
        formatedEventList.push(target_event);
      }
      return formatedEventList;
    },

    onCalendarClicked() {
      this.$router.push("/eventscalendar");
    },
    getUserNameById(userId) {
      const result2 = this.users
        .filter((u) => u.id == userId)
        .map((u) => u.user_name)[0];
      return result2;
    },
    getCategoryNameById(categoryId) {
      const result = this.categories
        .filter((c) => c.category_id == categoryId)
        .map((c) => c.category_name)[0];
      return result;
    },
    async getEventsBetweenTwoDates(eventDateFrom, eventDateTo) {
      let hello = await getEventsBetweenTwoDates(eventDateFrom, eventDateTo);
      this.eventList = this.formatDate(hello);
    },
    async loadUser() {
      this.users = await loadUser();
    },
    async loadData() {
      const settings = {
        methods: "GET",
        headers: {
          Authorization: localStorage.userId,
        },
      };

      this.fetchApi(settings);
    },

    async allEvents() {
      const settings = {
        methods: "GET",
        headers: {
          Authorization: localStorage.userId,
        },
      };

      this.fetchAllEvents(settings);
    },
    async fetchAllEvents(settings) {
      let apiFetchAllEvents = await fetchAllEvents(settings);
      this.eventList = this.formatDate(apiFetchAllEvents);
    },

    async getCategory() {
      this.categories = await getCategory();
    },

    async fetchApi(settings) {
      let apiReturn = await fetchApi(settings);
      this.eventList = this.formatDate(apiReturn);
      this.dateTo = "";
      this.dateFrom = "";
    },
    async removeEvent(event) {
      await removeEvent(event);
    },
    addNewEventClicked() {
      this.$router.push("/events/add");
    },

    openEventDetail(event) {
      this.$router.push("/events/" + event.id);
    },

    getCurrentDate() {
      let today = new Date();
      let mm = String(today.getMonth() + 1).padStart(2, "0");
      let yyyy = today.getFullYear();
      let currentDate = yyyy + "-" + mm;
      return currentDate;
    },
    async filterByMonth() {
      const settings = {
        methods: "GET",
        headers: {
          Authorization: localStorage.userId,
        },
      };

      this.fetchMonthApi(true, settings, this.getCurrentDate());
    },
    async fetchMonthApi(isShowingByMonth, settings, date) {
      this.isShowingByMonth = isShowingByMonth;
      let loadData = await fetchMonthApiEventList(
        isShowingByMonth,
        settings,
        date
      );
      this.eventList = this.formatDate(loadData);
    },
    async filterFromToday() {
      const settings = {
        methods: "GET",
        headers: {
          Authorization: localStorage.userId,
          "Content-Type": "application/json",
        },
      };
      this.fetchFromTodayEvents(settings);
    },
    async fetchFromTodayEvents(settings) {
      let loadData = await fetchFromTodayEvents(settings);
      this.eventList = this.formatDate(loadData);
    },
    async filterByPublics() {
      const settings = {
        methods: "GET",
        headers: {
          Authorization: localStorage.userId,
          "Content-Type": "application/json",
        },
      };

      this.fetchPublicEvents(settings);
    },
    async fetchPublicEvents(settings) {
      let loadPublic = await fetchPublicEvents(settings);
      this.eventList = this.formatDate(loadPublic);
    },
    async filterByDay() {
      let currentDate = new Date();
      let today = currentDate.getDate();
      let month = currentDate.getMonth() + 1;
      if (month.toString().length < 2) {
        month = "0" + month;
        month = config.months[month];
      }
      const settings = {
        methods: "GET",
        headers: {
          Authorization: localStorage.userId,
        },
      };

      const result = this.eventList.filter((target_event) => {
        let fecha = target_event.date.split("-");
        if (today == parseInt(fecha[0]) && month == fecha[1]) {
          return true;
        } else {
          return false;
        }
      });

      this.eventList = result;
      return result;
    },

    // eventFilteredData() {
    //   if (this.checkedCategory === false) {
    //     this.eventList = this.filteredData;
    //   } else {
    //     return this.eventList;
    //   }
    // },
  },
  computed: {
    filteredData() {
      var category = this.selectedCategory;

      if (this.checkedCategory === true && category != "") {
        return this.eventList.filter((e) => {
          return e.categories.category_id === category;
        });
      } else if (this.checkedPublic === true) {
        return this.eventList.filter((e) => {
          return e.public === 1;
        });
      } else {
        return this.eventList;
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600&display=swap");
.emogiDetail{
  border: 1px solid #4bfa85;
  border-radius: 3px;
  background-color:#4bfa85;
  width: fit-content;
  box-shadow: 0px 0px 4px rgb(36, 34, 34);

}
.emogiDelete{
  border: 1px solid #4bfa85;
  border-radius: 3px;
  background-color:#4bfa85;
  width: fit-content;
  box-shadow: 0px 0px 4px rgb(36, 34, 34);


}
.events-main {
  display: flex;
  flex-direction: column;
}
.title {
  text-align: center;
}
.filters {
  width: 100vw;
  display: flex;
  flex-direction: row;
}
.form {
  border: 2px groove black;
  padding-right: 2rem;
  width: 100%;
  margin: 0 2em;
  display: flex;
  justify-content: space-between;
}

.events-container {
  color: rgb(34, 34, 34);
  font-family: Montserrat;
  display: flex;
  flex-direction: row;
  gap: 1em;
  height: fit-content;
  grid-auto-rows: 18rem;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 50rem), 1fr));
  margin: 0em 2em 1.5em 1.5em;
  flex-wrap: wrap;
}
.category-text {
  margin-left: 2rem;
}
.category-select {
  width: auto;
  margin-left: 2rem;
}
.category-filter {
  margin-left: 2rem;
}
.events-container .event {
  background: rgb(241, 237, 237);
  box-shadow: 0px 0px 8px rgb(184, 181, 181);
  border-radius: 10px;
  font-size: larger;
  display: flex;
  flex-direction: row;
  width: 40%;

  margin: 1em;
}
.text-article {
  float: initial;
  width: 60%;
  margin: 2em;
}
.events-container .event h2 {
  color: #02c242;
  font-weight: bold;
  text-transform: capitalize;
}
.events-container .event p {
  max-width: 80%;
}

@media screen and (max-width: 800px) {
  .btn {
    width: 30%;
  }
}
.btn-add-event {
  margin-left: auto;
  margin-right: 1.5em;
  margin-top: 1rem;
  font-size: 1rem;
  border: 2px solid transparent;
  border-radius: 5px;
  background: #4bfa85;
  box-shadow: 0px 0px 4px rgb(36, 34, 34);
  height: 2.5rem;
  width: 20%;
  transition: 0.1s ease-in;
  margin: 1em;
  float: right;
}
.btn-calendar {
  margin-left: auto;
  margin-right: 1.5em;
  margin-top: 1rem;
  font-size: 1rem;
  border: 2px solid transparent;
  border-radius: 5px;
  background: #4bfa85;
  box-shadow: 0px 0px 4px rgb(36, 34, 34);
  height: 2.5rem;
  width: 20%;
  transition: 0.1s ease-in;
  margin: 1em;
  float: left;
}

ul {
  list-style: none;
}
ul li {
  margin: 0.5em;
}

button:focus {
  background-color: rgb(222, 230, 114);
}
.loggedInfo {
  display: flex;
  flex-direction: column;
  justify-content: left;
}

.filtersButton {
  width: fit-content;
}
.emogiDetail {
  border: 1px solid #4bfa85;
  border-radius: 3px;
  background-color: #4bfa85;
  width: fit-content;
  box-shadow: 0px 0px 4px rgb(36, 34, 34);
  
}
.emogiDelete {
  border: 1px solid #4bfa85;
  border-radius: 3px;
  background-color: #4bfa85;
  width: fit-content;
  box-shadow: 0px 0px 4px rgb(36, 34, 34);
}
</style>
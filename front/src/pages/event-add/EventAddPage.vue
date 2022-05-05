<template>
  <main>
    <h1>Añadir evento</h1>
    <form class="event-add-form">
      <label for="event-name"> Nombre</label>
      <input
        type="text"
        id="event-name"
        placeholder="Escribe el nombre del evento"
        v-model="event.name"
      />
      <label for="event-description"> Descripción</label>
      <input
        type="text"
        id="event-description"
        placeholder="Escribe la descripción del evento"
        v-model="event.description"
      />
      <label for="event-categories">Selecciona las categorias</label>
      <div
        v-for="category in categories"
        :value="category.category_id"
        :key="category.category_id"
      >
        <input
          type="checkbox"
          :id="category.category_id"
          v-model="event.categories"
          :value="category.category_id"
        />
        <label for="event-categories">{{ category.category_name }}</label>
      </div>

      <label> Elige si es público o no: </label>
      <select id="event-public" v-model="this.event.public">
        Elige si es público o no:
        <option
          v-for="option in statusPublic"
          :value="option.value"
          :key="option.id"
        >
          {{ option.text }}
        </option>
      </select>

      <label for="event-date"> Fecha</label>
      <input type="date" id="event-date" v-model="event.date" />
      <label for="event-time"> Hora</label>
      <input type="time" id="event-time" v-model="event.time" />
      <button class="btn add-event-btn" @click.prevent="addNewEventForm">
        Guardar
      </button>
    </form>
  </main>
</template>

<script>
import { getCategory, addNewEvent } from "@/services/api.js";

export default {
  name: "add-event",
  data() {
    return {
      statusPublic: [
        { text: "Si", value: true },
        { text: "No", value: false },
      ],
      categories: {},
      selectedCategory: null,
      event: {
        name: "",
        description: "",
        date: "",
        time: "",
        categories: [],
        public: false,
      },
    };
  },
  mounted() {
    this.getCategory();
  },
  computed: {},
  methods: {
    changeStatus() {
      let statusevent = this.statusPublic;
      if (statusevent === "si") {
        return (this.event.public = true);
      } else {
        return (this.event.public = false);
      }
    },

    isValidEventForm() {
      if (
        this.event.name === "" ||
        this.event.description === "" ||
        this.event.date === "" ||
        this.event.time === "" ||
        this.event.categories === ""
      ) {
        return false;
      } else {
        return true;
      }
    },

    async getCategory() {
      this.categories = await getCategory();
    },

    async addNewEventForm() {
      if (!this.isValidEventForm()) {
        alert("Se deben rellaner todos los campos");
        return;
      }
      await addNewEvent(this.event);
      alert("Evento guardado correctamente");
      this.$router.push("/events");
    },
  },
};
</script>

<style scoped>
main {
  padding: 2em;
}
#event-time {
  width: 5em;
}
#event-date {
  width: 10em;
}
.event-add-form {
  display: flex;
  flex-direction: column;
}
.event-add-form label {
  text-align: left;
}

.event-add-form > * {
  margin-bottom: 0.5em;
}
.event-add-form input {
  padding: 0.5em 0;
}
.add-event-btn {
  padding: 0.5em;
  margin-top: 1em;
  width: fit-content;
}
</style>
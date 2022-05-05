<template>
  <section class="events-main">
    <h3>Modifica tu evento</h3>
    <label for="event-name">Nombre</label>
    <input
      type="text"
      id="event-name"
      placeholder="Escribe el nombre del evento"
      v-model="event.name"
    />
    <label for="event-description">Descripcion:</label>
    <input
      type="text"
      id="event-description"
      placeholder="Escribe la descripción del evento"
      v-model="event.description"
    />

    <label for="event-category">Categoria</label>

    <select id="event-category" v-model="event.categories" multiple>
      <option disabled value="">
        Seleccione las categorias:(Pulsando CTRL)
      </option>
      <option
        v-for="category in categoriesLoaded"
        :value="category.category_id"
        :key="category.id"
      >
        {{ category.category_name }}
      </option>
    </select>
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
    <label for="event-date">Fecha:</label>
    <input type="date" id="event-date" v-model="event.date" />
    <label for="event-time">Hora:</label>
    <input type="time" id="event-time" v-model="event.time" />
    <button class="btn" @click.prevent="modifyEvent">Guardar</button>
    <button class="btn" @click.prevent="cancelModifyEvent">Cancelar</button>
  </section>
</template>





<script>
import { getCategory, loadData, modifyEvent } from "@/services/api.js";

export default {
  name: "eventsModifyPage",
  data() {
    return {
      statusPublic: [
        { text: "Si", value: 1 },
        { text: "No", value: 0 },
      ],
      categoriesLoaded: {},
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
    this.loadData();
    this.getCategory();
  },
  methods: {
    async loadData() {
      this.event = await loadData(this.$route.params.id);
    },
    async getCategory() {
      this.categoriesLoaded = await getCategory();
    },

    isValidEventForm() {
      if (
        this.event.name === "" ||
        this.event.description === "" ||
        this.event.date === "" ||
        this.event.time === "" ||
        this.event.category_id === ""
      ) {
        return false;
      } else {
        return true;
      }
    },

    async modifyEvent() {
      if (!this.isValidEventForm()) {
        alert("Se deben rellaner todos los campos");
        return;
      }

      if (confirm("¿Estas seguro de querer modificar este evento?")) {
        let eventId = this.$route.params.id;
        await modifyEvent(this.event, eventId);
        alert("Evento guardado correctamente");
        this.$router.push("/events");
      } else {
        this.$router.push("/events/modify/" + this.$route.params.id);
      }
    },
    cancelModifyEvent() {
      this.$router.push("/events/" + this.$route.params.id);
    },
  },
};
</script>

<style scoped>
h3 {
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
.events-main label {
  margin-bottom: 0.6em;
}
.events-main h2 {
  color: #02c242;
  font-weight: bold;
  text-transform: capitalize;
}

.events-main input {
  padding: 0.4em;
  font-size: 1em;
  margin-bottom: 0.4em;
}

#event-date {
  width: 10em;
  height: 1.5;
}
#event-time {
  width: 6em;
  height: 1.5em;
}
</style> 
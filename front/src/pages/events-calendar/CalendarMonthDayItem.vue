<template>
  <li
    class="calendar-day"
    :class="{
      'calendar-day--not-current': !day.isCurrentMonth,
      'calendar-day--today': isToday,
    }"
  >
    <span>{{ label }}</span>
    <div class="event" v-for="event in matchevent" :key="event.id">
      <p @click="openEventDetail(event)" class="clicked_event">
        {{ event.name }}
      </p>
    </div>
  </li>
</template>

<script>
import dayjs from "dayjs";
import {fetchMonthApi} from "@/services/api.js"


export default {
  name: "CalendarMonthDayItem",

  props: {
    day: {
      type: Object,
      required: true,
    },

    isCurrentMonth: {
      type: Boolean,
      default: false,
    },

    isToday: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      eventList: [],
    };
  },
  mounted() {
    this.fetchMonthApi();
  },
  computed: {
    matchevent() {
      let monthDays = dayjs(this.day.date).format("DD");
      return this.eventList

        .filter((e) => {
          return e.date.slice(8, 10) == monthDays;
        })
        .filter((e) => {
          return e.date.slice(5, 7) == dayjs(this.day.date).format("MM");
        })
        .map((e) => ({ name: e.name, id: e.id }));
    },
    label() {
      return dayjs(this.day.date).format("D");
    },
  },
  methods: {
    openEventDetail(event) {
      this.$router.push("/events/" + event.id);
    },
    async fetchMonthApi() {
      this.eventList = await fetchMonthApi();
    },
  },
};
</script>

<style scoped>
.event {
  color: rgb(0, 0, 0);
  font-size: 1rem;
}
.btn {
  width: 75%;
  height: 75%;
}
.calendar-day {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  min-height: 100%;
  font-size: 16px;
  background-color: #fff;
  border-top: 2px solid rgb(51, 150, 42);
  color: var(--grey-800);
  padding: 5px;
}

.calendar-day > span {
  display: flex;
  margin: 2px;
  justify-content: center;
  align-items: center;
  position: absolute;
  right: 2px;

  width: var(--day-label-size);
  height: var(--day-label-size);
}

.calendar-day--not-current {
  background-color: var(--grey-100);
  color: var(--grey-300);
}

.calendar-day--today {
  padding-top: 4px;
}
.clicked_event {
  cursor: pointer;
}
.clicked_event:hover {
  text-decoration: underline;
}
.calendar-day--today > span {
  color: #fff;
  border-radius: 9999px;
  background-color: var(--grey-800);
}
</style>

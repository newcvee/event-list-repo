<template>
  <div class="calendar" id="app">
    <CalendarMonth />
  </div>
</template>

<script>
import CalendarMonth from "./CalendarMonth";

export default {
  name: "App",

  components: {
    CalendarMonth,
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* background-color: #3eb466; */
}

body {
  font-family: sans-serif;
  font-weight: 100;
  --grey-100: #b5f1c9;
  --grey-200: #cfd7e3;
  --grey-300: #b5c0cd;
  --grey-800: #3e4e63;
  --grid-gap: 1px;
  --day-label-size: 20px;
}

ol,
li {
  padding: 0;
  margin: 0;
  list-style: none;
}

.calendar-month-header {
  display: flex;
  justify-content: space-between;
  background-color: #fff;
  padding: 10px;
}
.calendar {
  /* top: 0px; */
  height: 60vh;
  padding-left: 2px;
}
</style>

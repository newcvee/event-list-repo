<template>
  <div class="calendar-date-indicator">{{ selectedMonth }} {{selectedYear}}</div>
</template>

<script>
import dayjs from 'dayjs';
import localeES from 'dayjs/locale/es'

const spanishDayjs = dayjs.locale(localeES) 

export default {
  props: {
    selectedDate: {
      type: Object,
      required: true,
    },
  },

  computed: {
    selectedMonth() {
      let monthSelected = this.selectedDate;
      let formateo = monthSelected.set().format('MMMM')
      let formateo1 = formateo.charAt(0).toUpperCase() + formateo.slice(1)
      return formateo1
      },
    
    selectedYear(){
      return this.selectedDate.format("YYYY");
 
    },
  },
};
</script>

<style scoped>
.calendar-date-indicator {
  font-size: 24px;
  font-weight: 600;
  color: #3eb466;
}
</style>


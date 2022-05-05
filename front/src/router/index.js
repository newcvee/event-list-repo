import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/home/HomePage.vue'),
  },

  {
    path: '/events',
    name: 'Events',
    component: () => import('@/pages/events/EventsListPage.vue'),
  },

  {
    path: '/events/:id',
    name: 'EventsDetailPage',
    component: () => import('@/pages/event-detail/EventDetailPage.vue'),
  },
  {
    path: '/events/add',
    name: 'EventsAddPage',
    component: () => import('@/pages/event-add/EventAddPage.vue'),
  },

  {
    path: '/events/modify/:id',
    name: 'EventModifyPage',
    component: () => import('@/pages/event-modify/EventModifyPage.vue'),
  },
  {
    path: '/eventscalendar',
    name: 'EventsCalendarPage',
    component: () => import('@/pages/events-calendar/EventsCalendarPage.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router

import { v4 as uuidv4 } from "uuid";
import config from "@/config.js";

export async function getCategory() {
  const settings = {
    methods: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  };
  let endpoint = "http://localhost:5000/api/categories";
  let response = await fetch(endpoint, settings);
  let loadData = await response.json();
  return loadData
}


export async function fetchMonthApi() {
  const settings = {
    methods: "GET",
    headers: {
      Authorization: localStorage.userId,
    },
  };
  let response = await fetch(`http://localhost:5000/api/events`, settings);
  let loadData = await response.json();
  return loadData

}

export async function loadData(id) {
  const settings = {
    methods: "GET",
    headers: {
      Authorization: localStorage.userId,
    },
  };


  let response = await fetch(`${config.API_PATH}/events/${id}`, settings);
  let loadData = await response.json();

  return loadData;
}

export async function removeEventInside(id) {
  if (confirm("¿Deseas eliminar este evento?")) {
    await fetch(`${config.API_PATH}/events/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: localStorage.userId,
        "Content-Type": "application/json",
      },
    });
  } else {
    this.$router.push(this.$route.params.id);
  }
  location.reload(true);
}

export async function addNewEvent(event) {
  event.id = uuidv4();
  const settings = {
    method: "POST",
    body: JSON.stringify(event),
    headers: {
      Authorization: localStorage.userId,
      "Content-Type": "application/json",
    },
  };
  await fetch(`${config.API_PATH}/events`, settings);
}


export async function modifyEvent(event, id) {
  const settings = {
    method: "PUT",
    body: JSON.stringify(event, id),
    headers: {
      Authorization: localStorage.userId,
      "Content-Type": "application/json",
    },
  };
  await fetch(
    `${config.API_PATH}/events/${id}`,
    settings
  );

}

export async function getEventsBetweenTwoDates(eventDateFrom, eventDateTo) {
  const settings = {
    methods: "GET",
    headers: {
      Authorization: localStorage.userId,
    },
  };
  let endpoint = `${config.API_PATH}/events/eventsbetween/${eventDateFrom}/${eventDateTo}`;

  let response = await fetch(endpoint, settings);
  let loadData = await response.json();
  return loadData;
}


export async function loadUser() {
  let endpoint = `${config.API_PATH}/users`;
  let response = await fetch(endpoint);
  let userData = await response.json();
  return userData;
}
export async function fetchApi(settings) {
  let endpoint = `${config.API_PATH}/orderedevents`;

  let response = await fetch(endpoint, settings);
  let loadData = await response.json();
  return loadData;
}
export async function fetchAllEvents(settings) {
  let endpoint = `${config.API_PATH}/events`;
  let response = await fetch(endpoint, settings);
  let loadData = await response.json();
  return loadData;
}

export async function removeEvent(event) {
  if (confirm("¿Deseas eliminar este evento?")) {
    await fetch("http://localhost:5000/api/events/" + event.id, {
      method: "DELETE",
      headers: {
        Authorization: localStorage.userId,
        "Content-Type": "application/json",
      },
    });
  } else {
    return "";
  }
  location.reload(true);
}

export async function fetchMonthApiEventList(isShowingByMonth, settings, date) {
  let endpoint = "";

  endpoint = `${config.API_PATH}/monthlyevent/${date}`;

  let response = await fetch(endpoint, settings);
  let loadData = await response.json();
  return loadData
}
export async function fetchFromTodayEvents(settings) {
  let endpoint = `${config.API_PATH}/orderedevents`;
  let response = await fetch(endpoint, settings);
  let loadData = await response.json();
  return loadData
}

export async function fetchPublicEvents(settings) {
  let endpoint = `${config.API_PATH}/events/publicevents`;
  let response = await fetch(endpoint, settings);
  let loadData = await response.json();
  return loadData

}
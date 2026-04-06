import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faPhone,
  faTriangleExclamation,
  faEnvelope,
  faBan,
  faClock,
  faCircle,
  faXmark,
  faCircleCheck,
  faCalendar,
  faUser,
  faUserCheck,
  faUserSlash,
  faWandMagicSparkles
} from "@fortawesome/free-solid-svg-icons";

library.add(
  faPhone,
  faTriangleExclamation,
  faEnvelope,
  faBan,
  faClock,
  faCircle,
  faXmark,
  faCircleCheck,
  faCalendar,
  faUser,
  faUserCheck,
  faUserSlash,
  faWandMagicSparkles
);

const app = createApp(App);
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");

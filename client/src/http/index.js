import axios from "axios";
export const API_URL = `http://${window.location.hostname}:8000/api`;

const $api = axios.create({
  baseURL: API_URL,
});
$api.interceptors.response.use(
  (config) => {
    return config;
  },
  async (error) => {
    console.log(error);
    throw error;
  }
);
export default $api;

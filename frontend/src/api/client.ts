import axios from "axios";
import { getToken } from "../store/authStorage";

export const API_BASE_URL = "http://192.168.29.63:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

api.interceptors.request.use(async (config) => {
  const token = await getToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

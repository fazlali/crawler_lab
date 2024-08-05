import axios from 'axios'
import {ref} from "vue";

const api = axios.create({
    baseURL: '/api/',
    headers: {'X-Requested-With': 'XMLHttpRequest'}
})

export const pendingRequests = ref(0)

api.interceptors.request.use( (config) => {
    pendingRequests.value++;
    return config;
},  Promise.reject);

api.interceptors.response.use(({data}) => {
    pendingRequests.value--;
    return data;
},  (error) => {
    pendingRequests.value--;
    return Promise.reject(error);
});


export async function saveWebsite(domain, website) {
    return await api.post(`websites/${domain}`, website)
}

export async function loadWebsite(domain) {
    return await api.get(`websites/${domain}`)
}

export async function loadWebsites() {
    return await api.get(`websites`)
}

export async function scrape(urls, selectors) {
    return await api.post(`scrape`, {urls, selectors})
}

export async function extract(start_urls, config) {
    return await api.post(`extract`, {start_urls, config})
}

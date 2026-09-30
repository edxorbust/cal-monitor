import api from './api';

export function today() {
  const date = new Date();
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

export function errorMessage(error) {
  const data = error.response?.data;
  if (!data) return 'No se pudo conectar. Comprueba tu conexión y que el backend esté iniciado.';
  const flatten = (value) => typeof value === 'object' && value !== null ? Object.values(value).flatMap(flatten) : [String(value)];
  return flatten(data).join(' ');
}

export async function listAll(path) {
  let page = 1;
  let rows = [];
  while (true) {
    const { data } = await api.get(path, { params: { page, page_size: 200 } });
    rows = rows.concat(data.results);
    if (!data.next) return rows;
    page += 1;
  }
}

export const number = (value) => Number(value || 0).toLocaleString('es', { maximumFractionDigits: 1 });

// Вспомогательные функции для Open-Meteо (без ключа)
const GEO_URL = "https://geocoding-api.open-meteo.com/v1/search";
const WX_URL  = "https://api.open-meteo.com/v1/forecast";

// округлялка
const rnd = (n) => (typeof n === "number" ? Math.round(n) : null);

export async function fetchWeatherByCity(city = "Almaty", lang = "en") {
  // 1) Геокодинг города -> lat/lon/timezone
  const geoRes = await fetch(`${GEO_URL}?name=${encodeURIComponent(city)}&count=1&language=${lang}&format=json`);
  if (!geoRes.ok) throw new Error("Geocoding failed");
  const geo = await geoRes.json();
  if (!geo?.results?.length) throw new Error("Город не найден");
  const { latitude, longitude, timezone, name } = geo.results[0];

  // 2) Текущая и дневной прогноз
  const q = new URLSearchParams({
    latitude, longitude,
    current: "temperature_2m,relative_humidity_2m,pressure_msl,precipitation_probability",
    daily: "temperature_2m_max,weather_code",
    timezone
  });
  const wRes = await fetch(`${WX_URL}?${q.toString()}`);
  if (!wRes.ok) throw new Error("Weather fetch failed");
  const w = await wRes.json();

  // 3) Нормализация под твой компонент
  const pressureMm = Math.round((w.current?.pressure_msl ?? 0) * 0.750062); // гПа -> мм рт. ст.

  const payload = {
    now: {
      city: name,
      timeLocal: new Date(w.current?.time ?? Date.now()).toLocaleString("ru-RU", {
        hour: "2-digit", minute: "2-digit", day: "2-digit", month: "short", year: "numeric"
      }),
      tempC: rnd(w.current?.temperature_2m) ?? 0,
      pressureMm,
      humidity: rnd(w.current?.relative_humidity_2m) ?? 0,
      pop: rnd(w.current?.precipitation_probability) ?? 0,
      unitTemp: "C",
    },
    forecast: (w.daily?.time ?? []).slice(0, 4).map((t, i) => ({
      label: i === 0 ? "Сегодня" : new Date(t).toLocaleDateString("en-EN", { weekday: "short" }),
      tempC: rnd(w.daily.temperature_2m_max[i]) ?? 0,
      weatherCode: w.daily.weather_code[i],
    })),
  };

  return payload;
}

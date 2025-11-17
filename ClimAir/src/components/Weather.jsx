import { useEffect, useState } from "react";
import { fetchWeatherByCity } from "./api/WeatherClient";


// WMO code -> emoji (можно заменить на свои SVG)
const codeToEmoji = { 0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️", 45: "🌫️", 48: "🌫️", 51: "🌦️", 61: "🌧️", 71: "🌨️", 80: "🌦️", 95: "⛈️" };
const t = n => (typeof n === "number" ? Math.round(n) : "–");

export default function Weather({ city = "Almaty", className = "" }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [err, setErr] = useState(null);

    useEffect(() => {
        let dead = false;
        (async () => {
            try {
                setLoading(true); setErr(null);
                const payload = await fetchWeatherByCity(city, "ru");
                if (!dead) setData(payload);
            } catch (e) {
                if (!dead) setErr(e.message || "Ошибка");
            } finally {
                if (!dead) setLoading(false);
            }
        })();
        return () => { dead = true; };
    }, [city]);



    if (loading) return <Skeleton className={className} />;
    if (err || !data) return <ErrorBox msg={err || "Нет данных"} className={className} />;

    const { now, forecast } = data;
    const unit = now.unitTemp || "C";

    return (
        <div className={`rounded-2xl p-5 sm:p-5 text-white shadow-lg
                     bg-gradient-to-r from-rose-300/70 via-fuchsia-400/70 to-indigo-400/70
                     backdrop-blur w-full max-w-6xl mx-auto ${className}`}>
            <div className="grid grid-cols-12 items-center gap-4">
                <div className="col-span-12 sm:col-span-3">
                    <div className="font-semibold text-lg">{now.city}</div>
                    <div className="text-xs opacity-90 mt-1">{now.timeLocal}</div>
                </div>

                <div className="col-span-6 sm:col-span-2 flex items-baseline gap-1">
                    <div className="text-5xl font-extrabold">{t(now.tempC)}</div>
                    <div className="text-sm font-semibold opacity-90">°{unit}</div>
                </div>

                <div className="col-span-6 sm:col-span-4 grid grid-cols-3 gap-2 text-[11px] sm:text-xs">
                    <Metric label="Давление" value={`${t(now.pressureMm)} мм`} icon="🧭" />
                    <Metric label="Влажность" value={`${t(now.humidity)}%`} icon="💧" />
                    <Metric label="Вер. осадков" value={`${t(now.pop)}%`} icon="🌧️" />
                </div>

                <div className="col-span-12 sm:col-span-3 flex justify-end gap-4">
                    {forecast?.slice(0, 4).map((d, i) => (
                        <div key={i} className="text-right">
                            <div className="text-[10px] sm:text-xs opacity-90">{d.label}</div>
                            <div className="flex items-center gap-1 justify-end">
                                <span className="text-base">{d.weatherCode != null ? (codeToEmoji[d.weatherCode] || "🌡️") : "🌡️"}</span>
                                <span className="text-sm sm:text-base">{t(d.tempC)}°</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

function Metric({ label, value, icon }) {
    return (
        <div className="flex items-center gap-2">
            <span className="text-base">{icon}</span>
            <div>
                <div className="opacity-90 leading-tight">{label}</div>
                <div className="font-semibold leading-tight">{value}</div>
            </div>
        </div>
    );
}

function Skeleton({ className = "" }) {
    return <div className={`rounded-2xl p-5 bg-slate-200 animate-pulse ${className}`}>Загрузка…</div>;
}
function ErrorBox({ msg, className = "" }) {
    return <div className={`rounded-2xl p-5 bg-rose-100 text-rose-700 ${className}`}>Ошибка: {msg}</div>;
}

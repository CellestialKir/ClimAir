// DistrictCards.jsx
import React from "react";
import { useEffect, useState } from "react";
import axios from "axios"

/* --- статусы --- */
const pm25Bands = [
    { max: 5, label: "Good", color: "text-emerald-600" },
    { max: 15, label: "Moderate", color: "text-yellow-600" },
    { max: 30, label: "Unhealthy", color: "text-red-600" },
    { max: 9999, label: "Very bad", color: "text-fuchsia-600" },
];

const co2Bands = [
    { max: 800, label: "Good", color: "text-emerald-600" },
    { max: 1000, label: "Moderate", color: "text-yellow-600" },
    { max: 1500, label: "Bad", color: "text-red-600" },
    { max: 9999, label: "Very bad", color: "text-fuchsia-600" },
];

function bandFor(v, bands) {
    return bands.find(b => v <= b.max) ?? bands[bands.length - 1];
}

/* --- круг-прогресс на conic-gradient --- */
function Ring({ value, max = 200, size = 64 }) {
    const pct = Math.max(0, Math.min(100, (value / max) * 100));
    const bg = `conic-gradient(var(--ringColor) ${pct}%, rgba(0,0,0,0.08) ${pct}% 100%)`;
    return (
        <div
            className="relative grid place-items-center rounded-full"
            style={{
                width: size,
                height: size,
                background: bg,
                ['--ringColor']: 'currentColor',
            }}
        >
            <div className="absolute inset-1 rounded-full bg-white/90 backdrop-blur" />
            <div className="relative text-base text-slate-800">{value}</div>
        </div>
    );
}

/* --- одна карточка района --- */
function DistrictCard({ name, pm25, co2 }) {
    const pmBand = bandFor(pm25, pm25Bands);
    const co2Band = bandFor(co2 * 1000, co2Bands);

    return (
        <div className="rounded-2xl px-5 py-4 bg-white/35 backdrop-blur-md
                    border border-white/40 shadow-xl shadow-black/10
                    relative overflow-hidden">
            {/* лёгкий внутренний свет */}
            <div className="pointer-events-none absolute inset-0 rounded-2xl
                      shadow-inner shadow-[inset_0_20px_60px_rgba(255,255,255,.25)]" />

            <div className="relative flex flex-wrap md:flex-nowrap items-center gap-4 md:gap-6">
                {/* название района */}
                <div className="min-w-0 md:w-[180px]">
                    <div className="text-slate-900 font-extrabold text-xl leading-tight truncate">
                        {name}
                    </div>
                </div>

                {/* PM2.5 */}
                <div className="flex items-center gap-3 flex-shrink-0">
                    <div className={`text-4xl ${pmBand.color}`}>
                        <Ring value={pm25} max={35} />
                    </div>
                    <div className="text-sm leading-tight whitespace-nowrap">
                        <div className="font-semibold text-slate-700">PM 2.5</div>
                        <div className={`${pmBand.color} font-semibold`}>{pmBand.label}</div>
                    </div>
                </div>

                {/* CO₂ (уходит вправо, не сжимается) */}
                <div className="ml-auto flex items-center gap-3 flex-shrink-0">
                    <div className={`text-4xl ${co2Band.color}`}>
                        <Ring value={co2 * 1000} max={2000} />
                    </div>
                    <div className="text-sm leading-tight whitespace-nowrap text-right">
                        <div className="font-semibold text-slate-700">CO₂</div>
                        <div className={`${co2Band.color} font-semibold`}>{co2Band.label}</div>
                    </div>
                </div>
            </div>
        </div>
    );
}

/* --- список --- */
export default function DistrictCards() {
    const [districts, setDistricts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await axios.get("/api/getStatsByRegion");
                const data = response.data.data;

                const mapped = data.map(d => ({
                    name: d.region,
                    pm25: Number(d.avg_pm25.toFixed(1)),
                    co2: Number(d.avg_co2.toFixed(2))
                }));

                setDistricts(mapped);
                setLoading(false);
            } catch (error) {
                console.error("Error with data", error);
                setLoading(false);
            }
        }

        fetchData();

    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }
    // const districts = [
    //     { name: "Medeu", pm25: 140, co2: 800 },
    //     { name: "Bostandyk", pm25: 95, co2: 720 },
    //     { name: "Auezov", pm25: 60, co2: 900 },
    //     { name: "Alatau", pm25: 35, co2: 780 },
    //     { name: "Turksib", pm25: 150, co2: 1100 },
    //     { name: "Zhetysu", pm25: 80, co2: 850 },
    //     { name: "Nauryzbai", pm25: 55, co2: 700 },
    //     { name: "Almalinsky", pm25: 120, co2: 920 },
    // ];

    return (
        <div className="container mx-auto px-4 mt-6">
            {/* 1 колонка на мобиле, 2 — с md и выше */}
            <div className="grid lg:grid-cols-2 md:grid-cols-1 sm:grid-cols-1 gap-4">
                {districts.map((d) => (
                    <DistrictCard key={d.name} {...d} />
                ))}
            </div>
        </div>
    );
}

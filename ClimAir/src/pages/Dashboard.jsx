// Dashboard.jsx
import Weather from "../components/Weather";
import DistrictCards from "../components/DistrictCards"

import Co2 from "../images/Co2.png";
import PM2 from "../images/PM2.png";
import PM10 from "../images/PM10.png";
import Noise from "../images/Noise.png";
import DistrictGraph from "../components/DistrictGraph";

/* Универсальная карточка показателя */
function StatCard({ iconSrc, titleTop = "Current", title, value, status = "Normal", unit = "мкг/м³" }) {
    return (
        <div className="rounded-2xl p-5 bg-gradient-to-b from-white/25 to-white/10
                    backdrop-blur-md border border-white/30 shadow-xl shadow-black/10">
            <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/60">
                    <img src={iconSrc} alt="" className="h-4xl w-4xl object-contain" />
                </div>
                <div className="leading-tight">
                    <div className="text-slate-700/80 text-sm">{titleTop}</div>
                    <div className="text-slate-700 font-semibold">{title}</div>
                </div>
            </div>

            <div className="mx-auto my-4 h-1.5 w-1.5 "></div>

            <div className="rounded-full px-4 py-2 bg-gradient-to-r from-emerald-400 to-green-500
                      text-white shadow-md flex items-center justify-center gap-2">
                <span className="text-xl font-extrabold">{value}</span>
                <span className="text-sm font-medium">{status}</span>
                <span className="text-xs opacity-90">{unit}</span>
            </div>
        </div>
    );
}





export default function Dashboard() {
    return (
        <div className="min-h-screen ml-66 mt-[80px]">
            {/* Карточка погоды */}
            <div className="container mx-auto px-4">
                <div className="flex justify-center mt-6">
                    <Weather city="Almaty" className="w-full max-w-7xl" />
                </div>
            </div>

            {/* Ряд маленьких карточек */}
            <div className="container mx-auto px-4 mt-6">
                <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
                    <StatCard iconSrc={Co2} title="PM 2.5 Level" value={12} />
                    <StatCard iconSrc={PM2} title="PM 2.5 Level" value={12} />
                    <StatCard iconSrc={PM10} title="PM 10 Level" value={15} />
                    <StatCard iconSrc={Noise} title="Noise Level" value={15} status="Normal" unit="dB" />
                </div>
            </div>

            {/* Большой стеклянный бокс под график */}
            <div className="container mx-auto px-4 mt-8">
                <div className="relative w-full max-w-6xl mx-auto">
                    <div className="relative h-[260px] rounded-3xl p-5
                          bg-gradient-to-b from-white/30 to-white/10
                          backdrop-blur-xl border border-white/30
                          shadow-xl shadow-black/10">
                        {/* мягкое внутреннее свечение у краёв */}
                        <div className="pointer-events-none absolute inset-0 rounded-3xl
                            shadow-inner shadow-[inset_0_20px_60px_rgba(255,255,255,.25)]" />
                        {/* тонкий кольцевой штрих для объёма */}
                        <div className="pointer-events-none absolute inset-0 rounded-3xl ring-1 ring-white/40" />

                        {/* кнопка в правом верхнем углу */}
                        {/* <button className="absolute top-3 right-3 rounded-full px-3 py-1
                               bg-emerald-500/90 text-black text-sm shadow
                               hover:bg-emerald-500">
                            Monthly ▾
                        </button> */}

                        {/* место для графика */}
                        <DistrictGraph region="Алатауский" />
                    </div>
                </div>
            </div>

            <div className="container mx-auto px-4">
                <div className="flex justify-center mt-6">
                    <DistrictCards />
                </div>
            </div>

        </div>
    );
}

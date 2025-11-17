import React, { useEffect, useState } from "react"
import axios from "axios"
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts"

export default function DistrictGraph({region}) {
    const [interval, setInterval] = useState("month");
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!region) return;

        async function fetchData() {
            setLoading(true);
            try {
                const response = await axios.get("/api/getGraphStats", {
                    params: { interval, region }
                });
                const chartData = (response.data.data || []).map((item, i) => ({ ...item, index: i + 1, co2: item.co2 * 1000}));
                setData(chartData);
            } catch (error) {
                console.error("Error with graphs", error);
                setData([]);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, [region, interval])

    return (
        <div className="w-full h-full">
            <div className="flex gap-2 mb-2">
                <select 
                    value={interval}
                    onChange={(e) => setInterval(e.target.value)}
                    className="px-3 py-1 rounded bg-white/20 text-black">
                    <option value="day">Day</option>
                    <option value="month">Month</option>
                    <option value="year">Year</option>
                </select>
            </div>

            {loading ? (
                <div>Loading...</div>
            ) : (
                <ResponsiveContainer width="100%" height={260}>
                    <LineChart data={data} margin={{ top: 20, right: 20, left: 0, bottom: 80 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="index" />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="pm25" stroke="#10b981" />
                        <Line type="monotone" dataKey="co2" stroke="#ef4444" />
                    </LineChart>
                </ResponsiveContainer>
            )}

        </div>
    )
}
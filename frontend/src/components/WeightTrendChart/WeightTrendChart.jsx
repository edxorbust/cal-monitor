import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// Días abreviados en español
  const days = ["D", "L", "Ma", "M", "J", "V", "S"];

const WeightTrendChart = () => {
  // Datos de ejemplo
  const data = [
    { date: "2025-07-29", weight: 185 },
    { date: "2025-07-30", weight: 182 },
    { date: "2025-07-31", weight: 179 },
    { date: "2025-08-01", weight: 178 },
    { date: "2025-08-02", weight: 180 },
    { date: "2025-08-03", weight: 175 },
    { date: "2025-08-04", weight: 173 },
  ];

  // Transformar dataset para que el campo day sea abreviado
  const formattedData = data.map((item) => {
    const date = new Date(item.date); // asegúrate de que tu data tenga un campo "date"
    return {
      ...item,
      day: days[date.getDay()],
    };
  });

  return (
    <ResponsiveContainer width="100%" height={125}>
      <LineChart data={formattedData} margin={{ top: 20, right: 25, left: 25, bottom: 10 }}>
        <XAxis dataKey="day" axisLine={false} />
        <YAxis hide={true} /> {/* ocultamos el eje Y */}
        <Tooltip
          formatter={(value) => [`${value} lbs`, ""]}
        />
        <Line
          type="monotone"
          dataKey="weight"
          stroke="#007bff"
          strokeWidth={2}
          dot={{ r: 5 }}
          activeDot={{ r: 8 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default WeightTrendChart;

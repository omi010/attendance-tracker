import React, { useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

const MonthlyReport = () => {
  const [month, setMonth] = useState('');
  const [data, setData] = useState([]);

  const fetchMonthlyData = async () => {
    if (!month) return alert("Select a month");

    try {
      const res = await axios.get(`http://localhost:8000/monthly-summary/${month}`);
      setData(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to fetch monthly data.");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Monthly Attendance Report</h2>

      <input
        type="month"
        value={month}
        onChange={(e) => setMonth(e.target.value)}
        className="border px-2 py-1"
      />
      <button
        onClick={fetchMonthlyData}
        className="ml-2 bg-blue-500 text-white px-4 py-1 rounded"
      >
        Load
      </button>

      <ResponsiveContainer width="100%" height={300} className="mt-6">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="student_id" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="present_days" fill="#4ade80" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default MonthlyReport;

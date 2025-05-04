import React, { useState } from 'react';
import axios from 'axios';

const DailySheet = () => {
  const [selectedDate, setSelectedDate] = useState('');
  const [sheet, setSheet] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchDailySheet = async () => {
    if (!selectedDate) {
      alert("Please select a date");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/daily-sheet/${selectedDate}`);
      setSheet(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to fetch daily sheet.");
    }
    setLoading(false);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Daily Attendance Sheet</h2>

      <div className="mb-4">
        <label className="block mb-1">Select Date:</label>
        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
          className="border px-2 py-1"
        />
        <button
          onClick={fetchDailySheet}
          className="ml-2 bg-green-500 text-white px-4 py-2 rounded"
        >
          View
        </button>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="table-auto w-full border">
          <thead>
            <tr>
              <th className="border px-4 py-2">Student ID</th>
              <th className="border px-4 py-2">Present</th>
              <th className="border px-4 py-2">Marked Time</th>
            </tr>
          </thead>
          <tbody>
            {sheet.map((s) => (
              <tr key={s.student_id}>
                <td className="border px-4 py-2">{s.student_id}</td>
                <td className="border px-4 py-2">{s.present ? "✅" : "❌"}</td>
                <td className="border px-4 py-2">
                  {s.timestamp ? new Date(s.timestamp._seconds * 1000).toLocaleString() : "N/A"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default DailySheet;

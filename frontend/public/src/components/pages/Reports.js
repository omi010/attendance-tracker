import React, { useState } from 'react';
import axios from 'axios';

const Reports = () => {
  const [month, setMonth] = useState('');
  const [status, setStatus] = useState('');

  const sendReports = async () => {
    try {
      setStatus('Sending...');
      const response = await axios.post(
        `http://localhost:8000/send-monthly-reports/${month}`
      );
      setStatus(response.data.message);
    } catch (err) {
      console.error(err);
      setStatus('Failed to send reports');
    }
  };

<button
  onClick={() => window.open(`http://localhost:8000/download-report/${month}`)}
  className="bg-green-600 text-white px-4 py-2 rounded ml-2"
>
  Download Excel
</button>

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Send Monthly Reports</h2>

      <input
        type="month"
        value={month}
        onChange={(e) => setMonth(e.target.value)}
        className="border p-2 mr-2"
      />
      <button
        onClick={sendReports}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Send Reports
      </button>

      <p className="mt-4 text-sm text-gray-600">{status}</p>
    </div>
  );
};

export default Reports;

const [className, setClassName] = useState('');

<input
  type="text"
  placeholder="Class (optional)"
  value={className}
  onChange={(e) => setClassName(e.target.value)}
  className="border p-2 mr-2"
/>

window.open(`http://localhost:8000/download-report/${month}?class_name=${className}`)
const downloadAbsentees = () => {
  window.open(`http://localhost:8000/download-absentees/${month}-01`);
};
<button
  onClick={downloadAbsentees}
  className="bg-red-600 text-white px-4 py-2 rounded ml-2"
>
  Absentees Only
</button>
const [absentees, setAbsentees] = useState([]);
const [previewDate, setPreviewDate] = useState('');

const fetchAbsentees = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/download-absentees-preview/${previewDate}`);
    setAbsentees(res.data);
  } catch (err) {
    console.error("Error fetching absentees", err);
  }
};
<input
  type="date"
  value={previewDate}
  onChange={(e) => setPreviewDate(e.target.value)}
  className="border p-2 mr-2"
/>

<button
  onClick={fetchAbsentees}
  className="bg-purple-600 text-white px-4 py-2 rounded"
>
  Preview Absentees
</button>
{absentees.length > 0 && (
  <table className="mt-4 w-full border">
    <thead>
      <tr className="bg-gray-200">
        <th className="p-2 border">Name</th>
        <th className="p-2 border">Email</th>
        <th className="p-2 border">Class</th>
      </tr>
    </thead>
    <tbody>
      {absentees.map((student, idx) => (
        <tr key={idx}>
          <td className="p-2 border">{student.name}</td>
          <td className="p-2 border">{student.email}</td>
          <td className="p-2 border">{student.class}</td>
        </tr>
      ))}
    </tbody>
  </table>
)}

const checkAbsenteeThreshold = async () => {
  const res = await axios.get(`http://localhost:8000/check-absentees-alert/${previewDate}?threshold=10`);
  alert(res.data.message);
};

<button
  onClick={checkAbsenteeThreshold}
  className="bg-yellow-600 text-white px-4 py-2 rounded mt-4"
>
  Check Absentee Alert
</button>
const emailAbsentees = async () => {
  const res = await axios.post(`http://localhost:8000/email-absentees/${previewDate}`);
  alert(`${res.data.count} absentee emails sent.`);
};

<button
  onClick={emailAbsentees}
  className="bg-red-600 text-white px-4 py-2 rounded mt-2"
>
  Email Parents of Absentees
</button>

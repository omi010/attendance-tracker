import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AttendanceTable = () => {
  const [students, setStudents] = useState([]);
  const [attendance, setAttendance] = useState({});
  const [date, setDate] = useState('');

  // 🚀 Load student list (Replace this with API call if needed)
  useEffect(() => {
    setStudents([
      { id: 'abc123', name: 'John Doe' },
      { id: 'def456', name: 'Jane Smith' },
      { id: 'ghi789', name: 'Ravi Kumar' },
    ]);
  }, []);

  // ✅ Toggle checkbox
  const handleCheckboxChange = (id) => {
    setAttendance((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  // 🚀 Submit attendance to backend
  const submitAttendance = async () => {
    if (!date) {
      alert('Please select a date');
      return;
    }

    const entries = Object.keys(attendance).map((id) => ({
      student_id: id,
      present: attendance[id],
    }));

    try {
      const response = await axios.post(
        `http://localhost:8000/mark-attendance/${date}`, // Change this to your backend URL
        entries
      );
      alert('✅ Attendance marked successfully!');
      console.log(response.data);
    } catch (error) {
      console.error('Error submitting attendance:', error);
      alert('❌ Failed to mark attendance');
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Mark Attendance</h2>

      <div className="mb-4">
        <label className="block mb-1 font-semibold">Select Date:</label>
        <input
          type="date"
          className="border rounded p-2 w-full"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      <table className="w-full border-collapse border mb-4">
        <thead>
          <tr>
            <th className="border px-4 py-2 text-left">Student Name</th>
            <th className="border px-4 py-2 text-center">Present</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.id}>
              <td className="border px-4 py-2">{student.name}</td>
              <td className="border px-4 py-2 text-center">
                <input
                  type="checkbox"
                  checked={attendance[student.id] || false}
                  onChange={() => handleCheckboxChange(student.id)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button
        onClick={submitAttendance}
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded shadow"
      >
        Submit Attendance
      </button>
    </div>
  );
};

export default AttendanceTable;

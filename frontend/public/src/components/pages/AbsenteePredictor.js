import React, { useState } from 'react';
import axios from 'axios';

const AbsenteePredictor = () => {
  const [date, setDate] = useState('');
  const [predictions, setPredictions] = useState([]);

  const predict = async () => {
    const res = await axios.get(`http://localhost:8000/predict-absentees/${date}`);
    setPredictions(res.data);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">AI Absentee Predictions</h2>

      <input
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        className="border px-2 py-1 mr-2"
      />
      <button onClick={predict} className="bg-purple-500 text-white px-4 py-1 rounded">
        Predict
      </button>

      <ul className="mt-4 list-disc pl-5">
        {predictions.map((s, i) => (
          <li key={i}>{s.student_id} is likely to be absent</li>
        ))}
      </ul>
    </div>
  );
};

export default AbsenteePredictor;

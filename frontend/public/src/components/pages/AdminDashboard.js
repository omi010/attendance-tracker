import React, { useState } from 'react';

const AdminDashboard = () => {
    const [reportType, setReportType] = useState('');
    const [date, setDate] = useState('');
    const [className, setClassName] = useState('');

    const handleGenerateReport = async () => {
        const response = await fetch(`/generate-report`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reportType, date, className })
        });
        if (response.ok) {
            alert('Report generated successfully');
        } else {
            alert('Failed to generate report');
        }
    };

    return (
        <div>
            <h1>Admin Dashboard</h1>
            <select onChange={(e) => setReportType(e.target.value)}>
                <option value="">Select Report Type</option>
                <option value="daily">Daily Report</option>
                <option value="class">Class Report</option>
                <option value="monthly">Monthly Report</option>
            </select>
            {reportType === 'daily' && (
                <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                />
            )}
            {reportType === 'class' && (
                <input
                    type="text"
                    placeholder="Enter class name"
                    value={className}
                    onChange={(e) => setClassName(e.target.value)}
                />
            )}
            <button onClick={handleGenerateReport}>Generate Report</button>
        </div>
    );
};

export default AdminDashboard;
import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const AdminDashboard = () => {
    const [reportType, setReportType] = useState('');
    const [date, setDate] = useState('');
    const [className, setClassName] = useState('');
    const [attendanceData, setAttendanceData] = useState([]);

    const fetchAttendanceData = async () => {
        const response = await fetch(`/attendance/${date}`); // Assume you have an endpoint to fetch attendance data for a specific date
        const data = await response.json();
        setAttendanceData(data);
    };

    useEffect(() => {
        if (date) fetchAttendanceData();
    }, [date]);

    const handleGenerateReport = async () => {
        const response = await fetch(`/generate-report`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reportType, date, className })
        });
        if (response.ok) {
            alert('Report generated successfully');
        } else {
            alert('Failed to generate report');
        }
    };

    const generateChartData = () => {
        const presentCount = attendanceData.filter(student => student.present).length;
        const absentCount = attendanceData.length - presentCount;

        return {
            labels: ['Present', 'Absent'],
            datasets: [
                {
                    data: [presentCount, absentCount],
                    backgroundColor: ['#4CAF50', '#FF5733'],
                    hoverOffset: 4,
                },
            ],
        };
    };

    return (
        <div>
            <h1>Admin Dashboard</h1>
            <select onChange={(e) => setReportType(e.target.value)}>
                <option value="">Select Report Type</option>
                <option value="daily">Daily Report</option>
                <option value="class">Class Report</option>
                <option value="monthly">Monthly Report</option>
            </select>
            {reportType === 'daily' && (
                <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                />
            )}
            {reportType === 'class' && (
                <input
                    type="text"
                    placeholder="Enter class name"
                    value={className}
                    onChange={(e) => setClassName(e.target.value)}
                />
            )}
            <button onClick={handleGenerateReport}>Generate Report</button>

            {attendanceData.length > 0 && (
                <div>
                    <h2>Attendance Chart for {date}</h2>
                    <Pie data={generateChartData()} />
                </div>
            )}
        </div>
    );
};

export default AdminDashboard;
import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const AdminDashboard = () => {
    const [reportType, setReportType] = useState('');
    const [date, setDate] = useState('');
    const [className, setClassName] = useState('');
    const [studentName, setStudentName] = useState('');
    const [dateFrom, setDateFrom] = useState('');
    const [dateTo, setDateTo] = useState('');
    const [attendanceData, setAttendanceData] = useState([]);

    const fetchAttendanceData = async () => {
        let url = `/attendance/${date}`;

        // Add filters to URL
        if (dateFrom && dateTo) {
            url += `?from=${dateFrom}&to=${dateTo}`;
        }
        if (className) {
            url += `&class=${className}`;
        }
        if (studentName) {
            url += `&student=${studentName}`;
        }

        const response = await fetch(url);
        const data = await response.json();
        setAttendanceData(data);
    };

    useEffect(() => {
        if (date || dateFrom || dateTo || className || studentName) fetchAttendanceData();
    }, [date, dateFrom, dateTo, className, studentName]);

    const handleGenerateReport = async () => {
        const response = await fetch(`/generate-report`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reportType, date, className })
        });
        if (response.ok) {
            alert('Report generated successfully');
        } else {
            alert('Failed to generate report');
        }
    };

    const generateChartData = () => {
        const presentCount = attendanceData.filter(student => student.present).length;
        const absentCount = attendanceData.length - presentCount;

        return {
            labels: ['Present', 'Absent'],
            datasets: [
                {
                    data: [presentCount, absentCount],
                    backgroundColor: ['#4CAF50', '#FF5733'],
                    hoverOffset: 4,
                },
            ],
        };
    };

    return (
        <div>
            <h1>Admin Dashboard</h1>
            <select onChange={(e) => setReportType(e.target.value)}>
                <option value="">Select Report Type</option>
                <option value="daily">Daily Report</option>
                <option value="class">Class Report</option>
                <option value="monthly">Monthly Report</option>
            </select>

            {reportType === 'daily' && (
                <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                />
            )}

            {reportType === 'class' && (
                <input
                    type="text"
                    placeholder="Enter class name"
                    value={className}
                    onChange={(e) => setClassName(e.target.value)}
                />
            )}

            {reportType === 'monthly' && (
                <>
                    <input
                        type="date"
                        placeholder="From Date"
                        value={dateFrom}
                        onChange={(e) => setDateFrom(e.target.value)}
                    />
                    <input
                        type="date"
                        placeholder="To Date"
                        value={dateTo}
                        onChange={(e) => setDateTo(e.target.value)}
                    />
                </>
            )}

            <button onClick={handleGenerateReport}>Generate Report</button>

            {attendanceData.length > 0 && (
                <div>
                    <h2>Attendance Chart for {date}</h2>
                    <Pie data={generateChartData()} />
                </div>
            )}
        </div>
    );
};

export default AdminDashboard;
const fetchAttendanceData = async () => {
    const token = localStorage.getItem("access_token");  // Retrieve JWT token from localStorage

    const response = await fetch(`/attendance/${date}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,  // Include token in the header
        }
    });

    const data = await response.json();
    setAttendanceData(data);
};

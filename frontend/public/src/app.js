import DailySheet from './pages/DailySheet';
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './pages/AdminDashboard';
import ProtectedRoute from './components/ProtectedRoute';

const App = () => {
    return (
        <Router>
            <Switch>
                <Route path="/login" component={LoginPage} />
                <ProtectedRoute path="/admin" component={AdminDashboard} />
                <Redirect from="/" to="/login" />
            </Switch>
        </Router>
    );
};

export default App;


<Route path="/daily-sheet" element={<DailySheet />} />

<Link to="/daily-sheet">📄 View Daily Sheet</Link>

import MonthlyReport from './pages/MonthlyReport';

<Route path="/monthly-report" element={<MonthlyReport />} />

import './i18n/i18n';

import AbsenteePredictor from './pages/AbsenteePredictor';

<Route path="/predict-absentees" element={<AbsenteePredictor />} />

import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { getRole } from './utils/tokenUtils';
import AdminDashboard from './components/AdminDashboard';
import TeacherDashboard from './components/TeacherDashboard';
import StudentDashboard from './components/StudentDashboard';
import Login from './components/Login';

const App = () => {
  const role = getRole();  // Get role from token

  return (
    <Router>
      <Switch>
        <Route path="/login" component={Login} />
        {role === "admin" && <Route path="/admin" component={AdminDashboard} />}
        {role === "teacher" && <Route path="/teacher" component={TeacherDashboard} />}
        {role === "student" && <Route path="/student" component={StudentDashboard} />}
        <Route exact path="/" render={() => <h1>Welcome to the Attendance Tracker</h1>} />
      </Switch>
    </Router>
  );
};

export default App;

// tokenUtils.js
export const getToken = () => {
    return localStorage.getItem("access_token");
};

export const getRefreshToken = () => {
    return localStorage.getItem("refresh_token");
};

export const isTokenExpired = (token) => {
    try {
        const decoded = JSON.parse(atob(token.split(".")[1])); // Decode JWT token
        const exp = decoded.exp * 1000; // Convert to milliseconds
        return exp < Date.now();
    } catch (error) {
        return true;
    }
};

export const refreshToken = async () => {
    const refreshToken = getRefreshToken();
    const response = await fetch('/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        return data.access_token;
    }
    return null;
};

export const decodeToken = (token) => {
    try {
        const decoded = JSON.parse(atob(token.split(".")[1])); // Decode JWT token
        return decoded;
    } catch (error) {
        return null;
    }
};

export const getRole = () => {
    const token = getToken();
    if (token) {
        const decoded = decodeToken(token);
        return decoded?.role || "student"; // Default role is 'student'
    }
    return "student";
};

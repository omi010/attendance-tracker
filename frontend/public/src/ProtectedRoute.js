import React, { useEffect, useState } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { getToken, isTokenExpired, refreshToken } from '../utils/tokenUtils';

const ProtectedRoute = ({ component: Component, ...rest }) => {
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const checkAuthentication = async () => {
            const token = getToken();

            if (!token || isTokenExpired(token)) {
                const newToken = await refreshToken();
                if (newToken) {
                    setIsAuthenticated(true);
                } else {
                    setIsAuthenticated(false);
                }
            } else {
                setIsAuthenticated(true);
            }
            setLoading(false);
        };

        checkAuthentication();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <Route
            {...rest}
            render={(props) =>
                isAuthenticated ? <Component {...props} /> : <Redirect to="/login" />
            }
        />
    );
};

export default ProtectedRoute;

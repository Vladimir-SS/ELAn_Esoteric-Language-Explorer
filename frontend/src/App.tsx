import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './scss/index.scss';
import Navbar from './components/Navbar';
import EsolangsList from './components/EsolangsList';
import EsolangDetails from './components/EsolangDetails';
import { useEffect, useState } from 'react';
import { ToastContainer } from 'react-toastify';

const App: React.FC = () => {
    const [theme, setTheme] = useState("dark");

    const updateTheme = () => {
        const colorMode = window.matchMedia("(prefers-color-scheme: dark)").matches
            ? "dark"
            : "light";
        setTheme(colorMode);
    };

    useEffect(() => {
        updateTheme();

        const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
        mediaQuery.addEventListener("change", updateTheme);

        document.documentElement.setAttribute("data-bs-theme", theme);

        return () => {
            mediaQuery.removeEventListener("change", updateTheme);
        };
    }, [theme]);

    return (
        <Router>
            <Navbar />
            <div className="content">
                <Routes>
                    <Route path="/" element={<EsolangsList />} />
                    <Route path="/esolangs/:name" element={<EsolangDetails />} />
                </Routes>
            </div>
            <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
            />
        </Router>
    );
};

export default App

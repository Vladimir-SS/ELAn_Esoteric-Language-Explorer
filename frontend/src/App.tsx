import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './scss/index.scss';
import Navbar from './components/Navbar';
import EsolangsList from './components/EsolangsList';
import EsolangDetails from './components/EsolangDetails';
import { useEffect, useState } from 'react';
import { ToastContainer } from 'react-toastify';
import PropertyList from './components/PropertyList';
import PropertyDetails from './components/PropertyDetails';

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
                    <Route path="/esolangs/category" element={<PropertyList propertyPath="category" propertyPluralName="Categories" />} />
                    <Route path="/esolangs/category/:name" element={<PropertyDetails propertyPath="category" />} />
                    <Route path="/esolangs/paradigm" element={<PropertyList propertyPath="paradigm" propertyPluralName="Paradigms" />} />
                    <Route path="/esolangs/paradigm/:name" element={<PropertyDetails propertyPath="paradigm" />} />
                    <Route path="/esolangs/dialect" element={<PropertyList propertyPath="dialect" propertyPluralName="Dialects" />} />
                    <Route path="/esolangs/dialect/:name" element={<PropertyDetails propertyPath="dialect" />} />
                    <Route path="/esolangs/dimension" element={<PropertyList propertyPath="dimension" propertyPluralName="Dimensions" />} />
                    <Route path="/esolangs/dimension/:name" element={<PropertyDetails propertyPath="dimension" />} />
                    <Route path="/esolangs/computational-class" element={<PropertyList propertyPath="computational-class" propertyPluralName="Computational Classes" />} />
                    <Route path="/esolangs/computational-class/:name" element={<PropertyDetails propertyPath="computational-class" />} />
                    <Route path="/esolangs/memory-system" element={<PropertyList propertyPath="memory-system" propertyPluralName="Memory Systems" />} />
                    <Route path="/esolangs/memory-system/:name" element={<PropertyDetails propertyPath="memory-system" />} />
                    <Route path="/esolangs/type-system" element={<PropertyList propertyPath="type-system" propertyPluralName="Type Systems" />} />
                    <Route path="/esolangs/type-system/:name" element={<PropertyDetails propertyPath="type-system" />} />

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

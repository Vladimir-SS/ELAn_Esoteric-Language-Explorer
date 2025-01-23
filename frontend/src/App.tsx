import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './scss/index.scss';
import Navbar from './components/Navbar';
import EsolangsList from './components/EsolangsList';
import EsolangDetails from './components/EsolangDetails';

const App: React.FC = () => {
    return (
        <Router>
            <Navbar />
            <div className="content">
                <Routes>
                    <Route path="/" element={<EsolangsList />} />
                    <Route path="/esolangs/:name" element={<EsolangDetails />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App

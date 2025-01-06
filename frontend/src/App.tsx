import { BrowserRouter as Router } from 'react-router-dom';
import './scss/index.scss';
import Navbar from './components/Navbar';

const App: React.FC = () => {
    return (
        <Router>
            <Navbar />
            <div className="content">
                {/* <Routes>
                    <Route path="/" element={} />
                </Routes> */}
            </div>
        </Router>
    );
};

export default App

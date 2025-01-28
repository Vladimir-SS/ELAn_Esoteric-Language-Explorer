import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
    return (
        <nav className="navbar">
            <div className="container-fluid">
                <ul className="navbar-nav">
                    <li className="nav-item">
                        <Link to="/" className="nav-link">Home</Link>
                    </li>
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;
import { useState } from 'react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
    return (
        <nav className="navbar">
            <ul className="navbar__list">
                <li className="navbar__item">
                    <Link to="/" className="navbar__link">Home</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
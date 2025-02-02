import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  return (
    <nav
      className="navbar navbar-expand-lg navbar-light"
      style={{ backgroundColor: "#282c30" }}
    >
      <div className="container-fluid">
        <ul className="navbar-nav">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              Esolangs
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/esolangs/category" className="nav-link">
              Categories
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/esolangs/paradigm" className="nav-link">
              Paradigms
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/compare" className="nav-link">
              Compare
            </Link>
          </li>
        </ul>
        <ul>
          <li className="nav-item">
            <a
              href="https://vladimir-ss.github.io/ELAn_Esoteric-Language-Explorer/"
              className="nav-link"
              target="_blank"
              rel="noopener noreferrer"
            >
              Documentation
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
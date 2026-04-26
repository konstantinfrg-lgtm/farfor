import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Header.css';

const Header: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <span className="logo-icon">🏺</span>
          <span className="logo-text">Фарфоровые молочники</span>
        </Link>

        <nav className="nav">
          <Link to="/public" className="nav-link">Публичные коллекции</Link>
          
          {isAuthenticated ? (
            <>
              <Link to="/my-collection" className="nav-link">Моя коллекция</Link>
              <Link to="/add-item" className="nav-link add-btn">Добавить предмет</Link>
              <div className="user-menu">
                <span className="username">{user?.username}</span>
                <button onClick={handleLogout} className="logout-btn">Выйти</button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Войти</Link>
              <Link to="/register" className="nav-link register-btn">Регистрация</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;

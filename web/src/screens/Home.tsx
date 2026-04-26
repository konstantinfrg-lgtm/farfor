import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { itemService } from '../services/api';
import ItemCard from '../components/ItemCard';
import './Home.css';

const Home: React.FC = () => {
  const [items, setItems] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadItems();
  }, [searchTerm]);

  const loadItems = async () => {
    setIsLoading(true);
    try {
      const data = await itemService.getAll(searchTerm, !isAuthenticated);
      setItems(data);
    } catch (error) {
      console.error('Ошибка загрузки предметов:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="home-page">
      <div className="home-container">
        <div className="home-header">
          <h1 className="page-title">
            {isAuthenticated ? 'Коллекция фарфоровых молочников' : 'Публичные коллекции'}
          </h1>
          <p className="page-subtitle">
            {isAuthenticated 
              ? 'Управляйте своей коллекцией и делитесь с другими' 
              : 'Просмотр публичных коллекций коллекционеров'}
          </p>
        </div>

        <div className="search-bar">
          <input
            type="text"
            placeholder="Поиск по названию, производителю, автору..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        {!isAuthenticated && (
          <div className="auth-cta">
            <p>Хотите вести свою коллекцию?</p>
            <button onClick={() => navigate('/register')} className="cta-btn">
              Зарегистрироваться
            </button>
          </div>
        )}

        {isLoading ? (
          <div className="loading">Загрузка...</div>
        ) : items.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🏺</div>
            <h3>Пока нет предметов</h3>
            <p>{searchTerm ? 'Попробуйте изменить поисковый запрос' : 'Будьте первым, кто добавит предмет!'}</p>
          </div>
        ) : (
          <div className="items-grid">
            {items.map((item) => (
              <ItemCard key={item.id} item={item} showOwner={!isAuthenticated} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;

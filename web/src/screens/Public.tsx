import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { publicService } from '../services/api';
import ItemCard from '../components/ItemCard';
import './Public.css';

const Public: React.FC = () => {
  const [items, setItems] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadItems();
  }, [searchTerm]);

  const loadItems = async () => {
    setIsLoading(true);
    try {
      const data = await publicService.getPublicItems(searchTerm);
      setItems(data);
    } catch (error) {
      console.error('Ошибка загрузки предметов:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="public-page">
      <div className="public-container">
        <div className="public-header">
          <h1 className="page-title">Публичные коллекции</h1>
          <p className="page-subtitle">Просмотр публичных предметов коллекционеров фарфора</p>
        </div>

        <div className="search-bar">
          <input
            type="text"
            placeholder="Поиск по публичным коллекциям..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="public-info">
          <p>🏺 Здесь представлены только предметы, которые коллекционеры сделали публичными</p>
        </div>

        {isLoading ? (
          <div className="loading">Загрузка...</div>
        ) : items.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🏺</div>
            <h3>Пока нет публичных предметов</h3>
            <p>{searchTerm ? 'Попробуйте изменить поисковый запрос' : 'Коллекционеры еще не добавили публичные предметы'}</p>
            {!searchTerm && (
              <button onClick={() => navigate('/register')} className="cta-btn">
                Начать свою коллекцию
              </button>
            )}
          </div>
        ) : (
          <div className="items-grid">
            {items.map((item) => (
              <ItemCard key={item.id} item={item} showOwner={true} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Public;

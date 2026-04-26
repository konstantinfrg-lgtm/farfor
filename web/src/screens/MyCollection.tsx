import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { itemService } from '../services/api';
import ItemCard from '../components/ItemCard';
import './MyCollection.css';

const MyCollection: React.FC = () => {
  const [items, setItems] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    loadItems();
  }, [searchTerm, isAuthenticated]);

  const loadItems = async () => {
    setIsLoading(true);
    try {
      const data = await itemService.getMyItems();
      const filtered = searchTerm
        ? data.filter(item =>
            item.form_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.decoration_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.manufacturer?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.author_form?.toLowerCase().includes(searchTerm.toLowerCase())
          )
        : data;
      setItems(filtered);
    } catch (error) {
      console.error('Ошибка загрузки коллекции:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: number, e: React.MouseEvent) => {
    e.preventDefault();
    if (confirm('Вы уверены, что хотите удалить этот предмет?')) {
      try {
        await itemService.delete(id);
        setItems(items.filter(item => item.id !== id));
      } catch (error) {
        console.error('Ошибка удаления:', error);
        alert('Не удалось удалить предмет');
      }
    }
  };

  const handleTogglePublic = async (id: number, currentStatus: boolean, e: React.MouseEvent) => {
    e.preventDefault();
    try {
      const updated = await itemService.togglePublic(id);
      setItems(items.map(item => 
        item.id === id ? { ...item, is_public: updated.is_public } : item
      ));
    } catch (error) {
      console.error('Ошибка изменения видимости:', error);
    }
  };

  if (!isAuthenticated) return null;

  return (
    <div className="collection-page">
      <div className="collection-container">
        <div className="collection-header">
          <h1 className="page-title">Моя коллекция</h1>
          <p className="page-subtitle">Управляйте своими фарфоровыми молочниками и сливочниками</p>
        </div>

        <div className="collection-actions">
          <div className="search-bar">
            <input
              type="text"
              placeholder="Поиск в моей коллекции..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
          <button onClick={() => navigate('/add-item')} className="add-btn">
            + Добавить предмет
          </button>
        </div>

        {isLoading ? (
          <div className="loading">Загрузка...</div>
        ) : items.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🏺</div>
            <h3>Коллекция пуста</h3>
            <p>Добавьте свой первый предмет!</p>
            <button onClick={() => navigate('/add-item')} className="cta-btn">
              Добавить предмет
            </button>
          </div>
        ) : (
          <div className="items-grid">
            {items.map((item) => (
              <div key={item.id} className="item-wrapper">
                <ItemCard item={item} />
                <div className="item-actions">
                  <button
                    onClick={(e) => handleTogglePublic(item.id, item.is_public, e)}
                    className={`action-btn ${item.is_public ? 'public' : 'private'}`}
                  >
                    {item.is_public ? '🌍 Публичный' : '🔒 Приватный'}
                  </button>
                  <button
                    onClick={(e) => navigate(`/edit-item/${item.id}`, { state: { item } })}
                    className="action-btn edit"
                  >
                    ✏️ Редактировать
                  </button>
                  <button
                    onClick={(e) => handleDelete(item.id, e)}
                    className="action-btn delete"
                  >
                    🗑️ Удалить
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MyCollection;

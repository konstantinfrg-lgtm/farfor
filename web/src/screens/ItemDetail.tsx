import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { itemService } from '../services/api';
import { Item } from '../types';
import './ItemDetail.css';

const ItemDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [item, setItem] = useState<Item | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPhotoIndex, setSelectedPhotoIndex] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    loadItem();
  }, [id]);

  const loadItem = async () => {
    setIsLoading(true);
    try {
      const data = await itemService.getById(Number(id));
      setItem(data);
    } catch (error) {
      console.error('Ошибка загрузки предмета:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="item-detail-page">
        <div className="loading">Загрузка...</div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="item-detail-page">
        <div className="not-found">
          <h2>Предмет не найден</h2>
          <button onClick={() => navigate('/')} className="back-btn">На главную</button>
        </div>
      </div>
    );
  }

  const photos = item.photos || [];
  const currentPhoto = photos[selectedPhotoIndex] || photos[0];
  const imageUrl = currentPhoto 
    ? `http://localhost:8000${currentPhoto.file_path}`
    : '/placeholder.png';

  return (
    <div className="item-detail-page">
      <div className="item-detail-container">
        <button onClick={() => navigate(-1)} className="back-button">
          ← Назад
        </button>

        <div className="item-detail-content">
          <div className="item-gallery">
            <div className="main-image-container">
              <img 
                src={imageUrl} 
                alt={item.form_name || item.decoration_name}
                className="main-image"
              />
            </div>
            
            {photos.length > 1 && (
              <div className="thumbnail-grid">
                {photos.map((photo, index) => (
                  <button
                    key={photo.id}
                    onClick={() => setSelectedPhotoIndex(index)}
                    className={`thumbnail ${index === selectedPhotoIndex ? 'active' : ''}`}
                  >
                    <img src={`http://localhost:8000${photo.file_path}`} alt={`Photo ${index + 1}`} />
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="item-details">
            <div className="item-header">
              <h1 className="detail-title">
                {item.form_name || item.decoration_name || 'Без названия'}
              </h1>
              
              {!item.is_public && (
                <span className="private-badge">Приватный предмет</span>
              )}
            </div>

            {(item.manufacturer || item.author_form) && (
              <p className="detail-subtitle">
                {item.manufacturer}{item.manufacturer && item.author_form ? ', ' : ''}{item.author_form}
              </p>
            )}

            <div className="detail-section">
              <h3 className="section-heading">Основная информация</h3>
              
              <div className="detail-grid">
                {item.manufacturer && (
                  <div className="detail-item">
                    <span className="detail-label">Производитель:</span>
                    <span className="detail-value">{item.manufacturer}</span>
                  </div>
                )}
                
                {item.author_form && (
                  <div className="detail-item">
                    <span className="detail-label">Автор формы:</span>
                    <span className="detail-value">{item.author_form}</span>
                  </div>
                )}
                
                {item.author_decoration && (
                  <div className="detail-item">
                    <span className="detail-label">Автор росписи:</span>
                    <span className="detail-value">{item.author_decoration}</span>
                  </div>
                )}
                
                {item.decoration_name && (
                  <div className="detail-item">
                    <span className="detail-label">Название росписи:</span>
                    <span className="detail-value">{item.decoration_name}</span>
                  </div>
                )}
                
                {item.year && (
                  <div className="detail-item">
                    <span className="detail-label">Год выпуска:</span>
                    <span className="detail-value">{item.year}</span>
                  </div>
                )}
                
                {item.period && (
                  <div className="detail-item">
                    <span className="detail-label">Период:</span>
                    <span className="detail-value">{item.period}</span>
                  </div>
                )}
                
                {item.material && (
                  <div className="detail-item">
                    <span className="detail-label">Материал:</span>
                    <span className="detail-value">{item.material}</span>
                  </div>
                )}
              </div>
            </div>

            <div className="detail-section">
              <h3 className="section-heading">Состояние и размеры</h3>
              
              <div className="detail-grid">
                {item.condition && (
                  <div className="detail-item">
                    <span className="detail-label">Состояние:</span>
                    <span className="detail-value">{item.condition}</span>
                  </div>
                )}
                
                {item.size && (
                  <div className="detail-item">
                    <span className="detail-label">Размер:</span>
                    <span className="detail-value">{item.size}</span>
                  </div>
                )}
              </div>
            </div>

            {item.location && (
              <div className="detail-section">
                <h3 className="section-heading">Местоположение</h3>
                <p className="detail-location">📍 {item.location}</p>
              </div>
            )}

            {item.comment && (
              <div className="detail-section">
                <h3 className="section-heading">Комментарий</h3>
                <p className="detail-comment">{item.comment}</p>
              </div>
            )}

            {item.owner_username && (
              <div className="owner-info">
                <span className="owner-label">Коллекционер:</span>
                <span className="owner-name">{item.owner_username}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ItemDetail;

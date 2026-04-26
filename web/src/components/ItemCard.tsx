import React from 'react';
import { Item } from '../types';
import { Link } from 'react-router-dom';
import './ItemCard.css';

interface ItemCardProps {
  item: Item;
  showOwner?: boolean;
}

const ItemCard: React.FC<ItemCardProps> = ({ item, showOwner = false }) => {
  const primaryPhoto = item.photos?.find(p => p.is_primary) || item.photos?.[0];
  const imageUrl = primaryPhoto 
    ? `http://localhost:8000${primaryPhoto.file_path}`
    : '/placeholder.png';

  return (
    <Link to={`/item/${item.id}`} className="item-card">
      <div className="item-image-container">
        <img 
          src={imageUrl} 
          alt={item.form_name || item.decoration_name}
          className="item-image"
          onError={(e) => {
            (e.target as HTMLImageElement).src = '/placeholder.png';
          }}
        />
        {!item.is_public && (
          <span className="private-badge">Приватный</span>
        )}
      </div>
      
      <div className="item-info">
        <h3 className="item-title">
          {item.form_name || item.decoration_name || 'Без названия'}
        </h3>
        
        {(item.manufacturer || item.author_form) && (
          <p className="item-subtitle">
            {item.manufacturer}{item.manufacturer && item.author_form ? ', ' : ''}{item.author_form}
          </p>
        )}
        
        <div className="item-meta">
          {item.year && <span className="item-year">{item.year}</span>}
          {item.period && <span className="item-period">{item.period}</span>}
        </div>
        
        {showOwner && item.owner_username && (
          <p className="item-owner">Коллекционер: {item.owner_username}</p>
        )}
        
        <div className="item-location">
          📍 {item.location || 'Не указано'}
        </div>
      </div>
    </Link>
  );
};

export default ItemCard;

import React, { useState, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { itemService } from '../services/api';
import { Item } from '../types';
import './AddItem.css';

const AddItem: React.FC = () => {
  const { state } = useLocation();
  const editItem = state?.item as Item | undefined;
  
  const [formData, setFormData] = useState({
    manufacturer: editItem?.manufacturer || '',
    author_form: editItem?.author_form || '',
    author_decoration: editItem?.author_decoration || '',
    form_name: editItem?.form_name || '',
    decoration_name: editItem?.decoration_name || '',
    year: editItem?.year || '',
    period: editItem?.period || '',
    material: editItem?.material || '',
    condition: editItem?.condition || '',
    size: editItem?.size || '',
    location: editItem?.location || '',
    comment: editItem?.comment || '',
    is_public: editItem?.is_public ?? true,
  });

  const [photos, setPhotos] = useState<File[]>([]);
  const [existingPhotos, setExistingPhotos] = useState<any[]>(editItem?.photos || []);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setFormData(prev => ({ ...prev, [name]: checked }));
  };

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newPhotos = Array.from(e.target.files);
      setPhotos(prev => [...prev, ...newPhotos]);
    }
  };

  const removePhoto = (index: number) => {
    setPhotos(prev => prev.filter((_, i) => i !== index));
  };

  const removeExistingPhoto = async (photoId: number) => {
    // В реальной реализации нужно добавить API для удаления фото
    setExistingPhotos(prev => prev.filter(p => p.id !== photoId));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const data = new FormData();
      
      Object.entries(formData).forEach(([key, value]) => {
        if (typeof value === 'boolean') {
          data.append(key, value.toString());
        } else {
          data.append(key, value);
        }
      });

      photos.forEach(photo => {
        data.append('photos', photo);
      });

      if (editItem) {
        await itemService.update(editItem.id, data);
      } else {
        await itemService.create(data);
      }

      navigate('/my-collection');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка сохранения предмета');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isAuthenticated) return null;

  return (
    <div className="add-item-page">
      <div className="add-item-container">
        <h1 className="page-title">{editItem ? 'Редактировать предмет' : 'Добавить предмет'}</h1>
        <p className="page-subtitle">Заполните информацию о фарфоровом молочнике или сливочнике</p>

        <form onSubmit={handleSubmit} className="add-item-form">
          {error && <div className="error-message">{error}</div>}

          <div className="form-section">
            <h2 className="section-title">Основная информация</h2>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="form_name">Название формы</label>
                <input
                  type="text"
                  id="form_name"
                  name="form_name"
                  value={formData.form_name}
                  onChange={handleInputChange}
                  placeholder="Например: Молочник классический"
                />
              </div>

              <div className="form-group">
                <label htmlFor="decoration_name">Название росписи</label>
                <input
                  type="text"
                  id="decoration_name"
                  name="decoration_name"
                  value={formData.decoration_name}
                  onChange={handleInputChange}
                  placeholder="Например: Гжель"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="manufacturer">Производитель</label>
                <input
                  type="text"
                  id="manufacturer"
                  name="manufacturer"
                  value={formData.manufacturer}
                  onChange={handleInputChange}
                  placeholder="Например: ЛФЗ, Гжель"
                />
              </div>

              <div className="form-group">
                <label htmlFor="author_form">Автор формы</label>
                <input
                  type="text"
                  id="author_form"
                  name="author_form"
                  value={formData.author_form}
                  onChange={handleInputChange}
                  placeholder="ФИО скульптора"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="author_decoration">Автор росписи</label>
                <input
                  type="text"
                  id="author_decoration"
                  name="author_decoration"
                  value={formData.author_decoration}
                  onChange={handleInputChange}
                  placeholder="ФИО художника"
                />
              </div>

              <div className="form-group">
                <label htmlFor="year">Год выпуска</label>
                <input
                  type="text"
                  id="year"
                  name="year"
                  value={formData.year}
                  onChange={handleInputChange}
                  placeholder="Например: 1985"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="period">Период</label>
                <input
                  type="text"
                  id="period"
                  name="period"
                  value={formData.period}
                  onChange={handleInputChange}
                  placeholder="Например: СССР, 1980-е"
                />
              </div>

              <div className="form-group">
                <label htmlFor="material">Материал</label>
                <input
                  type="text"
                  id="material"
                  name="material"
                  value={formData.material}
                  onChange={handleInputChange}
                  placeholder="Например: Фарфор, глазурь"
                />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h2 className="section-title">Состояние и размеры</h2>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="condition">Состояние</label>
                <select
                  id="condition"
                  name="condition"
                  value={formData.condition}
                  onChange={handleInputChange}
                >
                  <option value="">Выберите состояние</option>
                  <option value="Отличное">Отличное</option>
                  <option value="Хорошее">Хорошее</option>
                  <option value="Удовлетворительное">Удовлетворительное</option>
                  <option value="Требует реставрации">Требует реставрации</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="size">Размер</label>
                <input
                  type="text"
                  id="size"
                  name="size"
                  value={formData.size}
                  onChange={handleInputChange}
                  placeholder="Например: 12×8×10 см"
                />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h2 className="section-title">Дополнительно</h2>
            
            <div className="form-group full-width">
              <label htmlFor="location">Место нахождения или приобретения</label>
              <input
                type="text"
                id="location"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                placeholder="Например: Москва, антикварный магазин"
              />
            </div>

            <div className="form-group full-width">
              <label htmlFor="comment">Комментарий</label>
              <textarea
                id="comment"
                name="comment"
                value={formData.comment}
                onChange={handleInputChange}
                placeholder="Дополнительная информация о предмете"
                rows={4}
              />
            </div>

            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="is_public"
                  checked={formData.is_public}
                  onChange={handleCheckboxChange}
                />
                <span>Публичный предмет (виден другим пользователям)</span>
              </label>
            </div>
          </div>

          <div className="form-section">
            <h2 className="section-title">Фотографии</h2>
            
            <div className="photo-upload">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                multiple
                onChange={handlePhotoChange}
                className="file-input"
                id="photos"
              />
              <label htmlFor="photos" className="upload-btn">
                📷 Выбрать фотографии
              </label>
              <p className="upload-hint">Можно выбрать несколько файлов</p>
            </div>

            {photos.length > 0 && (
              <div className="photo-preview-grid">
                {photos.map((photo, index) => (
                  <div key={index} className="photo-preview">
                    <img src={URL.createObjectURL(photo)} alt={`Preview ${index}`} />
                    <button type="button" onClick={() => removePhoto(index)} className="remove-photo">×</button>
                  </div>
                ))}
              </div>
            )}

            {existingPhotos.length > 0 && (
              <div className="existing-photos">
                <p className="existing-photos-title">Текущие фотографии:</p>
                <div className="photo-preview-grid">
                  {existingPhotos.map((photo) => (
                    <div key={photo.id} className="photo-preview">
                      <img src={`http://localhost:8000${photo.file_path}`} alt="Existing" />
                      <button type="button" onClick={() => removeExistingPhoto(photo.id)} className="remove-photo">×</button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="form-actions">
            <button type="button" onClick={() => navigate('/my-collection')} className="cancel-btn">
              Отмена
            </button>
            <button type="submit" className="submit-btn" disabled={isLoading}>
              {isLoading ? 'Сохранение...' : (editItem ? 'Сохранить изменения' : 'Добавить предмет')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddItem;

import React, { useState } from 'react';
import { X, User, Save, Check } from 'lucide-react';
import { useLanguage } from '../i18n';

export default function FarmerProfileModal({ farmer, isOpen, onClose, onSave }) {
  const { t, normalizeCropKey } = useLanguage();

  if (!isOpen || !farmer) return null;

  const initialCropsStr = Array.isArray(farmer.crops) && farmer.crops.length > 0
    ? farmer.crops.join(', ')
    : (farmer.current_crop || 'Paddy');

  const [formData, setFormData] = useState({
    name: farmer.name || '',
    location: farmer.location || '',
    district: farmer.district || '',
    land_area: farmer.land_area || '',
    current_crop: farmer.current_crop || 'Paddy',
    crops_str: initialCropsStr,
    crop_variety: farmer.crop_variety || '',
    crop_stage: farmer.crop_stage || '',
    irrigation_type: farmer.irrigation_type || '',
    farming_type: farmer.farming_type || ''
  });

  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const parsedCrops = formData.crops_str
      ? formData.crops_str.split(',').map(s => s.trim()).filter(Boolean)
      : [formData.current_crop];

    const finalCrops = parsedCrops.length > 0 ? parsedCrops : [formData.current_crop];

    onSave({
      name: formData.name,
      location: formData.location,
      district: formData.district,
      land_area: formData.land_area,
      current_crop: formData.current_crop,
      crops: finalCrops,
      crop_variety: formData.crop_variety,
      crop_stage: formData.crop_stage,
      irrigation_type: formData.irrigation_type,
      farming_type: formData.farming_type
    });

    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      onClose();
    }, 800);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-row">
            <User size={20} color="#10b981" />
            <h3>{t('profileModalTitle')}</h3>
          </div>
          <button className="modal-close-btn" onClick={onClose} aria-label={t('close')}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="profile-form">
          <div className="form-row-2">
            <div className="form-group">
              <label>{t('fullName')}</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>{t('landAreaField')}</label>
              <input
                type="text"
                name="land_area"
                value={formData.land_area}
                onChange={handleChange}
                placeholder="2.0 Acres"
                required
              />
            </div>
          </div>

          <div className="form-row-2">
            <div className="form-group">
              <label>{t('locationField')}</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>{t('districtField')}</label>
              <input
                type="text"
                name="district"
                value={formData.district}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row-2">
            <div className="form-group">
              <label>{t('currentCropField')}</label>
              <select
                name="current_crop"
                value={formData.current_crop}
                onChange={handleChange}
              >
                <option value="Paddy">🌾 {t('crops.paddy')} (Paddy / Rice)</option>
                <option value="Sugarcane">🎋 {t('crops.sugarcane')} (Sugarcane)</option>
                <option value="Black Gram">🌱 {t('crops.black_gram')} (Black Gram / Urad)</option>
                <option value="Tomato">🍅 {t('crops.tomato')} (Tomato)</option>
                <option value="Chilli">🌶️ {t('crops.chilli')} (Chilli)</option>
                <option value="Groundnut">🥜 {t('crops.groundnut')} (Groundnut)</option>
              </select>
            </div>
            <div className="form-group">
              <label>{t('cropVarietyField')}</label>
              <input
                type="text"
                name="crop_variety"
                value={formData.crop_variety}
                onChange={handleChange}
                placeholder="e.g. BPT 5204 (Samba Mahsuri)"
              />
            </div>
          </div>

          <div className="form-group">
            <label>{t('cropStageField')}</label>
            <input
              type="text"
              name="crop_stage"
              value={formData.crop_stage}
              onChange={handleChange}
              placeholder="e.g. Tillering & Panicle Initiation (40-45 days)"
            />
          </div>

          <div className="form-row-2">
            <div className="form-group">
              <label>{t('irrigationTypeField')}</label>
              <input
                type="text"
                name="irrigation_type"
                value={formData.irrigation_type}
                onChange={handleChange}
                placeholder="Canal / Borewell / Drip"
              />
            </div>
            <div className="form-group">
              <label>{t('soilTypeField')}</label>
              <input
                type="text"
                name="farming_type"
                value={formData.farming_type}
                onChange={handleChange}
                placeholder="Alluvial / Clay Loam"
              />
            </div>
          </div>

          <div className="modal-actions-row">
            <button type="button" className="btn-cancel" onClick={onClose}>
              {t('close')}
            </button>
            <button type="submit" className="btn-save">
              {savedSuccess ? (
                <>
                  <Check size={16} />
                  <span>{t('profileSavedSuccess')}</span>
                </>
              ) : (
                <>
                  <Save size={16} />
                  <span>{t('saveProfile')}</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

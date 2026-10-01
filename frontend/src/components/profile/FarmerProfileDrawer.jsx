import React, { useState, useEffect, useMemo, useRef } from 'react';
import { useLanguage } from '../../i18n';
import {
  X,
  User,
  MapPin,
  Sprout,
  Calendar,
  Layers,
  Droplets,
  Check,
  AlertTriangle,
  Save,
  Loader2,
  ChevronDown,
  FolderLock,
  CreditCard,
  FileText,
  Landmark,
  ShieldCheck,
  Eye,
  Upload,
  Download,
  Printer,
  FileCheck
} from 'lucide-react';

/* =====================================================================
   CUSTOM REUSABLE DRAWER FORM COMPONENTS (NO BROWSER-DEFAULT LOOK)
   ===================================================================== */

function FormSection({ icon: Icon, title, children }) {
  return (
    <div className="drawer-form-section">
      <div className="drawer-section-header">
        {Icon && <Icon size={15} className="section-header-icon" />}
        <span className="drawer-section-title">{title}</span>
      </div>
      <div className="drawer-section-body">{children}</div>
    </div>
  );
}

function FormField({ label, error, children, required = false }) {
  return (
    <div className="custom-form-field">
      <div className="field-label-row">
        <label className="custom-field-label">
          {label} {required && <span className="required-star">*</span>}
        </label>
      </div>
      {children}
      {error && (
        <div className="custom-validation-msg">
          <AlertTriangle size={12} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}

function TextInput({ value, onChange, placeholder, hasError, ...props }) {
  return (
    <div className={`custom-input-wrapper ${hasError ? 'has-error' : ''}`}>
      <input
        type="text"
        className="custom-text-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        {...props}
      />
    </div>
  );
}

function NumberInput({ value, onChange, placeholder, unit, hasError, min = '0.1', step = '0.1', max = '1000' }) {
  return (
    <div className={`custom-number-wrapper ${hasError ? 'has-error' : ''}`}>
      <input
        type="number"
        className="custom-number-input"
        value={value}
        min={min}
        step={step}
        max={max}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
      {unit && <span className="custom-input-unit-badge">{unit}</span>}
    </div>
  );
}

function SelectField({ value, onChange, options, hasError }) {
  return (
    <div className={`custom-select-wrapper ${hasError ? 'has-error' : ''}`}>
      <select
        className="custom-select-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {options.map((opt) => (
          <option key={opt.id} value={opt.id}>
            {opt.label}
          </option>
        ))}
      </select>
      <ChevronDown size={16} className="custom-select-chevron" />
    </div>
  );
}

function DateInput({ value, onChange, maxDate, hasError }) {
  return (
    <div className={`custom-date-wrapper ${hasError ? 'has-error' : ''}`}>
      <input
        type="date"
        className="custom-date-input"
        value={value}
        max={maxDate}
        onChange={(e) => onChange(e.target.value)}
      />
      <Calendar size={16} className="custom-date-icon" />
    </div>
  );
}

function ChoiceCard({ isSelected, onClick, icon, title, subtitle, badge }) {
  return (
    <div
      className={`custom-choice-card ${isSelected ? 'selected' : ''}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
    >
      <div className="choice-card-left">
        {icon && <span className="choice-card-icon">{icon}</span>}
        <div className="choice-card-text">
          <span className="choice-card-title">{title}</span>
          {subtitle && <span className="choice-card-sub">{subtitle}</span>}
        </div>
      </div>
      <div className="choice-card-right">
        {badge && <span className="choice-card-badge">{badge}</span>}
        <div className={`choice-radio-circle ${isSelected ? 'checked' : ''}`}>
          {isSelected && <Check size={12} strokeWidth={3} />}
        </div>
      </div>
    </div>
  );
}

/* =====================================================================
   MAIN FARM PROFILE DRAWER
   ===================================================================== */

export default function FarmerProfileDrawer({
  farmer,
  isOpen,
  onClose,
  onSave
}) {
  const { t, language } = useLanguage();

  const parseLandArea = (val) => {
    if (!val) return '2.0';
    const match = String(val).match(/[\d.]+/);
    return match ? match[0] : '2.0';
  };

  const getInitialSowingDate = (dateVal) => {
    if (dateVal && dateVal.length >= 10) return dateVal.substring(0, 10);
    const d = new Date();
    d.setDate(d.getDate() - 40);
    return d.toISOString().split('T')[0];
  };

  const initialFormState = useMemo(() => {
    if (!farmer) return null;
    return {
      name: farmer.name || '',
      location: farmer.location || '',
      district: farmer.district || '',
      land_area: parseLandArea(farmer.land_area),
      current_crop: farmer.current_crop || 'Paddy',
      crop_variety: farmer.crop_variety || 'BPT-5204 (Samba Mahsuri)',
      irrigation_type: farmer.irrigation_type || 'Canal & Furrow',
      soil_type: farmer.soil_type || 'Clay Loam',
      sowing_date: getInitialSowingDate(farmer.sowing_date),
      passport_photo_url: farmer.passport_photo_url || '/assets/farmer_photo.jpg',
      aadhaar_number: farmer.aadhaar_number || 'XXXX-XXXX-4829',
      pan_number: farmer.pan_number || 'ABCDE1234F',
      bank_name: farmer.bank_name || 'State Bank of India (SBI)',
      bank_account_number: farmer.bank_account_number || 'XXXXXX5621',
      bank_ifsc: farmer.bank_ifsc || 'SBIN0001234',
      dbt_linked: farmer.dbt_linked ?? true,
      pattadar_passbook_number: farmer.pattadar_passbook_number || 'AP-KRI-2024-88412 (Khata: 412, Survey: 84/2A)',
      documents: farmer.documents || [
        {
          id: 'doc-001',
          type: 'passport_photo',
          name: 'Farmer_Passport_Photo.jpg',
          title: t('passportPhoto') || 'Passport Size Photograph',
          status: 'Verified',
          format: 'JPG',
          size: '240 KB',
          upload_date: '2026-08-15',
          file_url: '/assets/farmer_photo.jpg'
        },
        {
          id: 'doc-002',
          type: 'aadhaar_card',
          name: 'Aadhaar_Card_VenkatRao.pdf',
          title: t('aadhaarCard') || 'Aadhaar Card (UIDAI)',
          number: 'XXXX-XXXX-4829',
          status: 'e-KYC Verified',
          format: 'PDF',
          size: '1.2 MB',
          upload_date: '2026-08-15'
        },
        {
          id: 'doc-003',
          type: 'pan_card',
          name: 'PAN_Card_ABCDE1234F.pdf',
          title: t('panCard') || 'PAN Card (Income Tax Dept)',
          number: 'ABCDE1234F',
          status: 'Verified',
          format: 'PDF',
          size: '850 KB',
          upload_date: '2026-08-16'
        },
        {
          id: 'doc-004',
          type: 'bank_passbook',
          name: 'SBI_Passbook_AadhaarLinked.pdf',
          title: t('bankAccountPassbook') || 'Bank Passbook (DBT Linked)',
          bank_name: 'State Bank of India',
          account_number: 'XXXXXX5621',
          ifsc: 'SBIN0001234',
          status: 'DBT Active',
          format: 'PDF',
          size: '1.8 MB',
          upload_date: '2026-08-15'
        },
        {
          id: 'doc-005',
          type: 'pattadar_passbook',
          name: 'RoR_1B_Pattadar_Passbook.pdf',
          title: t('pattadarPassbook') || 'Pattadar Passbook / 1B Record',
          passbook_number: 'AP-KRI-2024-88412',
          survey_numbers: '84/2A, 84/2B (2.0 Acres)',
          status: 'Revenue Dept Certified',
          format: 'PDF',
          size: '2.4 MB',
          upload_date: '2026-08-15'
        }
      ]
    };
  }, [farmer, t]);

  const [formData, setFormData] = useState(initialFormState || {});
  const [errors, setErrors] = useState({});
  const [isSaving, setIsSaving] = useState(false);
  const [showDiscardPrompt, setShowDiscardPrompt] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [previewDoc, setPreviewDoc] = useState(null);
  const [uploadTargetId, setUploadTargetId] = useState(null);
  const fileInputRef = useRef(null);

  const handleTriggerReplace = (docId) => {
    setUploadTargetId(docId);
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileSelected = (e) => {
    const file = e.target.files?.[0];
    if (!file || !uploadTargetId) return;
    const isImage = file.type.startsWith('image/');
    const fileUrl = isImage ? URL.createObjectURL(file) : undefined;
    const fileSizeStr = file.size > 1024 * 1024
      ? `${(file.size / (1024 * 1024)).toFixed(1)} MB`
      : `${Math.round(file.size / 1024)} KB`;

    setFormData((prev) => {
      const updatedDocs = (prev.documents || []).map((d) => {
        if (d.id === uploadTargetId) {
          return {
            ...d,
            name: file.name,
            size: fileSizeStr,
            format: file.name.split('.').pop()?.toUpperCase() || (isImage ? 'JPG' : 'PDF'),
            upload_date: new Date().toISOString().split('T')[0],
            file_url: fileUrl || d.file_url,
            status: 'Verified'
          };
        }
        return d;
      });
      return {
        ...prev,
        documents: updatedDocs,
        ...(uploadTargetId === 'doc-001' && fileUrl ? { passport_photo_url: fileUrl } : {})
      };
    });
    e.target.value = '';
  };

  useEffect(() => {
    if (initialFormState) {
      setFormData(initialFormState);
      setErrors({});
      setShowDiscardPrompt(false);
    }
  }, [initialFormState, isOpen]);

  // Dynamically calculate crop age (days) from sowing date
  const calculatedCropAge = useMemo(() => {
    if (!formData.sowing_date) return 40;
    try {
      const sowing = new Date(formData.sowing_date);
      const now = new Date();
      const diffTime = now.getTime() - sowing.getTime();
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      return Math.max(1, diffDays);
    } catch {
      return 40;
    }
  }, [formData.sowing_date]);

  // Derive agricultural stage according to ICAR & ANGRAU taxonomy
  const derivedCropStage = useMemo(() => {
    const crop = (formData.current_crop || 'paddy').toLowerCase();
    const age = calculatedCropAge;

    if (crop.includes('paddy') || crop.includes('rice')) {
      if (age <= 25) return 'Seedling & Nursery Stage';
      if (age <= 50) return 'Active Tillering Stage';
      if (age <= 75) return 'Panicle Initiation Stage';
      if (age <= 100) return 'Flowering & Heading Stage';
      return 'Maturity & Grain Filling';
    }
    if (crop.includes('sugarcane')) {
      if (age <= 45) return 'Germination Stage';
      if (age <= 120) return 'Tillering & Formative Stage';
      if (age <= 250) return 'Grand Growth Stage';
      return 'Maturity & Ripening Stage';
    }
    if (crop.includes('black') || crop.includes('gram') || crop.includes('urad')) {
      if (age <= 20) return 'Vegetative & Branching Stage';
      if (age <= 45) return 'Flowering & Pod Formation';
      return 'Pod Filling & Maturity';
    }
    if (crop.includes('tomato')) {
      if (age <= 30) return 'Vegetative & Early Growth';
      if (age <= 60) return 'Flowering & Early Fruit Set';
      return 'Fruit Development & Harvest';
    }
    if (crop.includes('chilli')) {
      if (age <= 35) return 'Vegetative & Branching';
      if (age <= 70) return 'Flowering & Fruit Setting';
      return 'Fruit Maturation & Picking';
    }
    if (crop.includes('groundnut')) {
      if (age <= 30) return 'Vegetative Stage';
      if (age <= 55) return 'Flowering & Pegging';
      if (age <= 90) return 'Pod Development';
      return 'Maturity & Harvest';
    }
    return 'Active Vegetative Stage';
  }, [formData.current_crop, calculatedCropAge]);

  const hasUnsavedChanges = useMemo(() => {
    if (!initialFormState) return false;
    return Object.keys(initialFormState).some(
      (key) => initialFormState[key] !== formData[key]
    );
  }, [initialFormState, formData]);

  if (!isOpen) return null;

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: null }));
    }
  };

  const handleAttemptClose = () => {
    if (hasUnsavedChanges) {
      setShowDiscardPrompt(true);
    } else {
      onClose();
    }
  };

  const handleDiscardConfirm = () => {
    setShowDiscardPrompt(false);
    setFormData(initialFormState || {});
    onClose();
  };

  const validateForm = () => {
    const errs = {};
    if (!formData.name?.trim()) errs.name = t('errNameRequired');
    if (!formData.location?.trim()) errs.location = t('errLocationRequired');
    if (!formData.district?.trim()) errs.district = t('errDistrictRequired');
    if (!formData.land_area || isNaN(formData.land_area) || Number(formData.land_area) <= 0) {
      errs.land_area = t('errAreaRequired');
    }
    if (!formData.current_crop) errs.current_crop = t('errCropRequired');
    if (!formData.sowing_date) errs.sowing_date = t('errDateRequired');

    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm() || isSaving) return;

    setIsSaving(true);
    try {
      const formattedArea = `${formData.land_area} ${t('acres') || 'Acres'}`;
      const payload = {
        name: formData.name.trim(),
        location: formData.location.trim(),
        district: formData.district.trim(),
        land_area: formattedArea,
        current_crop: formData.current_crop,
        crops: [formData.current_crop],
        crop_variety: formData.crop_variety.trim(),
        crop_stage: `${derivedCropStage} (${calculatedCropAge} ${t('daysUnit') || 'days'})`,
        sowing_date: formData.sowing_date,
        irrigation_type: formData.irrigation_type,
        soil_type: formData.soil_type,
        passport_photo_url: formData.passport_photo_url,
        aadhaar_number: formData.aadhaar_number,
        pan_number: formData.pan_number,
        bank_name: formData.bank_name,
        bank_account_number: formData.bank_account_number,
        bank_ifsc: formData.bank_ifsc,
        dbt_linked: formData.dbt_linked,
        pattadar_passbook_number: formData.pattadar_passbook_number,
        documents: formData.documents
      };

      await onSave(payload);
      setShowToast(true);
      setTimeout(() => {
        setShowToast(false);
        onClose();
      }, 700);
    } catch (err) {
      console.error('Failed to update profile:', err);
    } finally {
      setIsSaving(false);
    }
  };

  // Crops Taxonomy
  const primaryCrops = [
    { id: 'Paddy', label: t('crops.paddy') || 'Paddy', icon: '🌾', tag: 'Primary' },
    { id: 'Sugarcane', label: t('crops.sugarcane') || 'Sugarcane', icon: '🌱', tag: 'Primary' },
    { id: 'Black Gram', label: t('crops.black_gram') || 'Black Gram', icon: '🫘', tag: 'Primary' }
  ];

  const secondaryCrops = [
    { id: 'Tomato', label: t('crops.tomato') || 'Tomato', icon: '🍅', tag: 'Secondary' },
    { id: 'Chilli', label: t('crops.chilli') || 'Chilli', icon: '🌶', tag: 'Secondary' },
    { id: 'Groundnut', label: t('crops.groundnut') || 'Groundnut', icon: '🥜', tag: 'Secondary' }
  ];

  // Irrigation Options
  const irrigationOptions = [
    { id: 'Canal & Furrow', label: t('irrigationCanal'), icon: '💧', desc: 'Gravity-fed canal network' },
    { id: 'Borewell', label: t('irrigationBorewell'), icon: '🚰', desc: 'Groundwater pump irrigation' },
    { id: 'Rainfed', label: t('irrigationRainfed'), icon: '🌧', desc: 'Monsoon rainfall dependent' },
    { id: 'Drip', label: t('irrigationDrip'), icon: '💦', desc: 'Micro-irrigation system' }
  ];

  // Soil Type Options
  const soilOptions = [
    { id: 'Clay Loam', label: t('soilClayLoam') },
    { id: 'Sandy Loam', label: t('soilSandyLoam') },
    { id: 'Black Cotton Soil', label: t('soilBlackCotton') },
    { id: 'Red Sandy Loam', label: t('soilRedLoam') },
    { id: 'Alluvial Soil', label: t('soilAlluvial') }
  ];

  return (
    <div className="drawer-backdrop" onClick={handleAttemptClose}>
      <aside className="profile-drawer" onClick={(e) => e.stopPropagation()}>
        {/* Sticky Header */}
        <div className="drawer-header">
          <div>
            <div className="drawer-header-title">
              <span className="drawer-avatar-icon">
                <User size={18} />
              </span>
              <h3>{t('farmProfileTitle')}</h3>
            </div>
            <p className="drawer-header-subtitle">{t('updateFarmInfo')}</p>
          </div>
          <button
            className="drawer-close-btn"
            onClick={handleAttemptClose}
            aria-label="Close"
          >
            <X size={20} />
          </button>
        </div>

        {/* Profile Summary Card */}
        <div className="drawer-profile-summary-box">
          <div className="summary-col">
            <span className="summary-farmer-name">👤 {formData.name || 'Venkat Rao'}</span>
            <span className="summary-meta-sub">
              📍 {formData.district || 'Krishna'}, {formData.location ? formData.location.split(',')[1] || 'AP' : 'AP'}
            </span>
          </div>
          <div className="summary-crop-tag">
            <span className="tag-crop-name">
              {primaryCrops.find(c => c.id === formData.current_crop)?.icon || secondaryCrops.find(c => c.id === formData.current_crop)?.icon || '🌾'} {formData.current_crop}
            </span>
            <span className="tag-crop-area">{formData.land_area} {t('acres') || 'Acres'}</span>
          </div>
        </div>

        {/* Scrollable Form Content */}
        <form onSubmit={handleFormSubmit} className="drawer-scroll-body" id="farm-profile-form">
          {/* SECTION 1: PERSONAL INFORMATION */}
          <FormSection icon={User} title={t('personalInfo')}>
            <FormField label={t('fullName')} error={errors.name} required>
              <TextInput
                value={formData.name}
                onChange={(v) => handleInputChange('name', v)}
                placeholder="Venkat Rao"
                hasError={Boolean(errors.name)}
              />
            </FormField>

            <div className="form-row-2">
              <FormField label={t('farmLocationField')} error={errors.location} required>
                <TextInput
                  value={formData.location}
                  onChange={(v) => handleInputChange('location', v)}
                  placeholder="Vijayawada, Andhra Pradesh"
                  hasError={Boolean(errors.location)}
                />
              </FormField>

              <FormField label={t('district')} error={errors.district} required>
                <TextInput
                  value={formData.district}
                  onChange={(v) => handleInputChange('district', v)}
                  placeholder="Krishna"
                  hasError={Boolean(errors.district)}
                />
              </FormField>
            </div>
          </FormSection>

          {/* SECTION 2: YOUR FARM */}
          <FormSection icon={Sprout} title={t('yourFarmSection')}>
            <FormField label={t('landArea')} error={errors.land_area} required>
              <NumberInput
                value={formData.land_area}
                onChange={(v) => handleInputChange('land_area', v)}
                placeholder="2.0"
                unit={t('acres')}
                hasError={Boolean(errors.land_area)}
              />
            </FormField>

            {/* Smart Crop Selector (Choice Cards) */}
            <FormField label={t('currentCrop')} error={errors.current_crop} required>
              <div className="crop-selector-container">
                <span className="crop-group-label">{t('primaryCrops')}</span>
                <div className="crop-choice-cards-grid">
                  {primaryCrops.map((c) => {
                    const isSelected = formData.current_crop === c.id;
                    return (
                      <div
                        key={c.id}
                        className={`crop-select-pill ${isSelected ? 'selected' : ''}`}
                        onClick={() => handleInputChange('current_crop', c.id)}
                        role="button"
                        tabIndex={0}
                      >
                        <span className="crop-pill-icon">{c.icon}</span>
                        <span className="crop-pill-label">{c.label}</span>
                        {isSelected && <Check size={13} className="crop-pill-check" />}
                      </div>
                    );
                  })}
                </div>

                <span className="crop-group-label" style={{ marginTop: '8px' }}>
                  {t('secondaryCrops')}
                </span>
                <div className="crop-choice-cards-grid">
                  {secondaryCrops.map((c) => {
                    const isSelected = formData.current_crop === c.id;
                    return (
                      <div
                        key={c.id}
                        className={`crop-select-pill ${isSelected ? 'selected' : ''}`}
                        onClick={() => handleInputChange('current_crop', c.id)}
                        role="button"
                        tabIndex={0}
                      >
                        <span className="crop-pill-icon">{c.icon}</span>
                        <span className="crop-pill-label">{c.label}</span>
                        {isSelected && <Check size={13} className="crop-pill-check" />}
                      </div>
                    );
                  })}
                </div>
              </div>
            </FormField>

            <FormField label={t('cropVariety')}>
              <TextInput
                value={formData.crop_variety}
                onChange={(v) => handleInputChange('crop_variety', v)}
                placeholder="BPT-5204 (Samba Mahsuri)"
              />
            </FormField>
          </FormSection>

          {/* SECTION 3: FARM CONDITIONS */}
          <FormSection icon={Droplets} title={t('farmConditions')}>
            <FormField label={t('irrigationType')}>
              <div className="irrigation-choice-grid">
                {irrigationOptions.map((irr) => {
                  const isSelected = formData.irrigation_type?.toLowerCase().includes(irr.id.toLowerCase());
                  return (
                    <ChoiceCard
                      key={irr.id}
                      isSelected={isSelected}
                      onClick={() => handleInputChange('irrigation_type', irr.id)}
                      icon={irr.icon}
                      title={irr.label}
                      subtitle={irr.desc}
                    />
                  );
                })}
              </div>
            </FormField>

            <FormField label={t('soilType')}>
              <SelectField
                value={formData.soil_type}
                onChange={(v) => handleInputChange('soil_type', v)}
                options={soilOptions}
              />
            </FormField>
          </FormSection>

          {/* SECTION 4: CROP INFORMATION */}
          <FormSection icon={Calendar} title={t('cropInfoSection')}>
            <FormField label={t('sowingDateField')} error={errors.sowing_date} required>
              <DateInput
                value={formData.sowing_date}
                onChange={(v) => handleInputChange('sowing_date', v)}
                maxDate={new Date().toISOString().split('T')[0]}
                hasError={Boolean(errors.sowing_date)}
              />
            </FormField>

            {/* Smart Calculated Crop Age & Derived Stage */}
            <div className="calculated-metrics-card">
              <div className="metric-row">
                <div className="metric-item">
                  <span className="metric-label">{t('cropAgeField')}</span>
                  <span className="metric-value-pill">
                    ⏳ <strong>{calculatedCropAge}</strong> {t('daysUnit') || 'days'}
                  </span>
                </div>
                <div className="metric-divider" />
                <div className="metric-item">
                  <span className="metric-label">{t('currentCropStageField')}</span>
                  <span className="stage-value-pill">
                    🌱 {derivedCropStage}
                  </span>
                </div>
              </div>
              <p className="metric-auto-note">
                ⓘ {t('metricAutoNote')}
              </p>
            </div>
          </FormSection>

          {/* SECTION 5: FARMER DOCUMENTS & DIGITAL FILE ACCESS LOCKER */}
          <FormSection icon={FolderLock} title={t('farmerDocumentsSection')}>
            <div className="farmer-docs-subtitle-box">
              <span className="docs-badge-vault">
                <ShieldCheck size={14} color="#059669" />
                <span>{t('farmerDocsSubtitle')}</span>
              </span>
            </div>

            <input
              type="file"
              ref={fileInputRef}
              style={{ display: 'none' }}
              onChange={handleFileSelected}
              accept="image/*,application/pdf"
            />

            <div className="farmer-docs-list">
              {(formData.documents || []).map((doc) => {
                let badgeText = t('ekycVerifiedStatus');
                if (doc.type === 'passport_photo') badgeText = 'Verified Photo';
                else if (doc.type === 'aadhaar_card') badgeText = t('ekycVerifiedStatus');
                else if (doc.type === 'pan_card') badgeText = t('taxExemptStatus');
                else if (doc.type === 'bank_passbook') badgeText = t('dbtActiveStatus');
                else if (doc.type === 'pattadar_passbook') badgeText = t('revenueCertifiedStatus');

                return (
                  <div key={doc.id} className="doc-item-card">
                    <div className="doc-item-top">
                      <div className="doc-item-icon-box">
                        {doc.type === 'passport_photo' ? (
                          <img
                            src={formData.passport_photo_url || '/assets/farmer_photo.jpg'}
                            alt="Passport"
                            className="doc-avatar-thumb"
                          />
                        ) : doc.type === 'aadhaar_card' ? (
                          <CreditCard size={20} color="#059669" />
                        ) : doc.type === 'pan_card' ? (
                          <FileText size={20} color="#0284c7" />
                        ) : doc.type === 'bank_passbook' ? (
                          <Landmark size={20} color="#d97706" />
                        ) : (
                          <FileCheck size={20} color="#7c3aed" />
                        )}
                      </div>
                      <div className="doc-item-info">
                        <div className="doc-title-row">
                          <span className="doc-name">{doc.title || doc.name}</span>
                          <span className="doc-verified-pill">
                            <ShieldCheck size={11} />
                            <span>{badgeText}</span>
                          </span>
                        </div>
                        <div className="doc-meta-row">
                          {doc.number && <span className="doc-number-pill">🔢 {doc.number}</span>}
                          {doc.account_number && (
                            <span className="doc-number-pill">
                              🏦 {doc.bank_name} • A/C: {doc.account_number} • IFSC: {doc.ifsc}
                            </span>
                          )}
                          {doc.passbook_number && (
                            <span className="doc-number-pill">
                              📜 {doc.passbook_number} • {doc.survey_numbers}
                            </span>
                          )}
                        </div>
                        <div className="doc-file-info-row">
                          <span className="file-name-text">📄 {doc.name}</span>
                          <span className="file-size-text">({doc.size || '1.0 MB'} • {doc.format || 'PDF'})</span>
                        </div>
                      </div>
                    </div>

                    <div className="doc-actions-row">
                      <button
                        type="button"
                        className="btn-view-doc"
                        onClick={() => setPreviewDoc(doc)}
                      >
                        <Eye size={13} />
                        <span>{doc.type === 'passport_photo' ? t('viewPhoto') : t('viewDocument')}</span>
                      </button>
                      <button
                        type="button"
                        className="btn-replace-doc"
                        onClick={() => handleTriggerReplace(doc.id)}
                      >
                        <Upload size={13} />
                        <span>{t('replaceFile')}</span>
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </FormSection>
        </form>

        {/* Sticky Action Footer */}
        <div className="drawer-sticky-footer">
          <button
            type="button"
            className="drawer-btn-cancel"
            onClick={handleAttemptClose}
            disabled={isSaving}
          >
            {t('cancel')}
          </button>
          <button
            type="submit"
            form="farm-profile-form"
            className="drawer-btn-save"
            disabled={isSaving}
          >
            {isSaving ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                <span>{t('saving')}</span>
              </>
            ) : (
              <>
                <Save size={16} />
                <span>{t('saveChanges')}</span>
              </>
            )}
          </button>
        </div>

        {/* Document Preview Full Modal */}
        {previewDoc && (
          <div className="doc-preview-modal-overlay" onClick={() => setPreviewDoc(null)}>
            <div className="doc-preview-modal-card" onClick={(e) => e.stopPropagation()}>
              <div className="doc-preview-header">
                <div className="doc-preview-header-left">
                  <ShieldCheck size={20} color="#059669" />
                  <div>
                    <h3 className="doc-preview-title">{previewDoc.title || previewDoc.name}</h3>
                    <p className="doc-preview-subtitle">
                      {previewDoc.name} • {previewDoc.size} • {t('ekycVerifiedStatus')}
                    </p>
                  </div>
                </div>
                <button
                  type="button"
                  className="doc-preview-close"
                  onClick={() => setPreviewDoc(null)}
                  aria-label="Close"
                >
                  <X size={18} />
                </button>
              </div>

              <div className="doc-preview-body">
                {previewDoc.type === 'passport_photo' ? (
                  <div className="photo-preview-sheet">
                    <img
                      src={formData.passport_photo_url || '/assets/farmer_photo.jpg'}
                      alt="Venkat Rao"
                      className="photo-preview-img"
                    />
                    <div className="photo-spec-box">
                      <h4>👤 {formData.name || 'Venkat Rao'}</h4>
                      <p><strong>{t('location')}:</strong> {formData.location}, {formData.district}</p>
                      <p><strong>{t('docFileSize')}:</strong> {previewDoc.size} • 1024 x 1024 px</p>
                      <p><strong>{t('docUploadedDate')}:</strong> {previewDoc.upload_date}</p>
                      <span className="photo-verified-tag">✅ {t('ekycVerifiedStatus')}</span>
                    </div>
                  </div>
                ) : previewDoc.type === 'aadhaar_card' ? (
                  <div className="card-mockup-sheet aadhaar-mockup">
                    <div className="card-mockup-top-band">
                      <span className="emblem-text">भारत सरकार / GOVERNMENT OF INDIA</span>
                    </div>
                    <div className="card-mockup-inner">
                      <div className="card-mockup-avatar-col">
                        <img
                          src={formData.passport_photo_url || '/assets/farmer_photo.jpg'}
                          alt="Avatar"
                          className="card-mockup-avatar"
                        />
                      </div>
                      <div className="card-mockup-data-col">
                        <div className="mockup-name">{formData.name || 'Venkat Rao'}</div>
                        <div className="mockup-sub">వెంకట్ రావు</div>
                        <div className="mockup-field"><strong>DOB / పుట్టిన తేది:</strong> 15/06/1976</div>
                        <div className="mockup-field"><strong>Gender / లింగం:</strong> Male / పురుషుడు</div>
                        <div className="mockup-number">{formData.aadhaar_number || 'XXXX XXXX 4829'}</div>
                      </div>
                    </div>
                    <div className="card-mockup-bottom-band">
                      <span>మేరా ఆధార్, మేరీ పహచాన్ • UIDAI Verified</span>
                    </div>
                  </div>
                ) : previewDoc.type === 'pan_card' ? (
                  <div className="card-mockup-sheet pan-mockup">
                    <div className="pan-top-row">
                      <span>आयकर विभाग / INCOME TAX DEPARTMENT</span>
                      <span className="pan-govt-sub">GOVT. OF INDIA</span>
                    </div>
                    <div className="card-mockup-inner">
                      <div className="card-mockup-avatar-col">
                        <img
                          src={formData.passport_photo_url || '/assets/farmer_photo.jpg'}
                          alt="Avatar"
                          className="card-mockup-avatar"
                        />
                      </div>
                      <div className="card-mockup-data-col">
                        <div className="mockup-field"><strong>Permanent Account Number Card</strong></div>
                        <div className="pan-big-number">{formData.pan_number || 'ABCDE1234F'}</div>
                        <div className="mockup-field"><strong>Name:</strong> {formData.name || 'VENKAT RAO'}</div>
                        <div className="mockup-field"><strong>Father's Name:</strong> RAMA RAO</div>
                        <div className="mockup-field"><strong>Status:</strong> {t('taxExemptStatus')}</div>
                      </div>
                    </div>
                  </div>
                ) : previewDoc.type === 'bank_passbook' ? (
                  <div className="card-mockup-sheet bank-mockup">
                    <div className="bank-header-bar">
                      <span className="bank-logo-text">🏛️ {formData.bank_name || 'STATE BANK OF INDIA'}</span>
                      <span className="bank-badge-active">DBT ENABLED</span>
                    </div>
                    <div className="bank-details-grid">
                      <div className="bank-detail-item">
                        <span className="b-label">Account Holder:</span>
                        <span className="b-val">{formData.name || 'VENKAT RAO'}</span>
                      </div>
                      <div className="bank-detail-item">
                        <span className="b-label">Account Number:</span>
                        <span className="b-val">{formData.bank_account_number || 'XXXXXX5621'}</span>
                      </div>
                      <div className="bank-detail-item">
                        <span className="b-label">IFSC Code:</span>
                        <span className="b-val">{formData.bank_ifsc || 'SBIN0001234'}</span>
                      </div>
                      <div className="bank-detail-item">
                        <span className="b-label">Branch:</span>
                        <span className="b-val">Vijayawada Main Agricultural Branch</span>
                      </div>
                      <div className="bank-detail-item">
                        <span className="b-label">Aadhaar Seeding:</span>
                        <span className="b-val text-green">✅ Linked for PM-KISAN & PMFBY Subsidies</span>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="card-mockup-sheet ror-mockup">
                    <div className="ror-header-bar">
                      <span>GOVERNMENT OF ANDHRA PRADESH • REVENUE DEPARTMENT</span>
                      <span className="ror-sub">Webland Certified 1B Record & Pattadar Passbook</span>
                    </div>
                    <div className="bank-details-grid">
                      <div className="bank-detail-item">
                        <span className="b-label">Pattadar Name:</span>
                        <span className="b-val">{formData.name || 'Venkat Rao'}</span>
                      </div>
                      <div className="bank-detail-item">
                        <span className="b-label">Passbook No:</span>
                        <span className="b-val">{formData.pattadar_passbook_number || 'AP-KRI-2024-88412'}</span>
                      </div>
                      <div className="bank-detail-item">
                        <span className="b-label">Khata / Survey Extent:</span>
                        <span className="b-val">Khata: 412 • Survey: 84/2A, 84/2B ({formData.land_area} {t('acres')})</span>
                      </div>
                      <div className="bank-detail-item">
                        <span className="b-label">Location:</span>
                        <span className="b-val">{formData.location}, {formData.district}</span>
                      </div>
                      <div className="bank-detail-item">
                        <span className="b-label">Digital Verification:</span>
                        <span className="b-val text-green">✅ Authenticated with State Webland Registry</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="doc-preview-footer">
                <button
                  type="button"
                  className="btn-preview-download"
                  onClick={() => window.print()}
                >
                  <Download size={14} />
                  <span>{t('downloadPrint')}</span>
                </button>
                <button
                  type="button"
                  className="btn-preview-close"
                  onClick={() => setPreviewDoc(null)}
                >
                  {t('closePreview')}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Discard Confirmation Prompt */}
        {showDiscardPrompt && (
          <div className="discard-prompt-overlay" onClick={() => setShowDiscardPrompt(false)}>
            <div className="discard-prompt-box" onClick={(e) => e.stopPropagation()}>
              <div className="prompt-header">
                <AlertTriangle size={20} color="var(--amber-500)" />
                <h4>{t('discardChangesTitle')}</h4>
              </div>
              <p className="prompt-message">{t('discardChangesMsg')}</p>
              <div className="prompt-actions-row">
                <button
                  type="button"
                  className="btn-keep-editing"
                  onClick={() => setShowDiscardPrompt(false)}
                >
                  {t('keepEditing')}
                </button>
                <button
                  type="button"
                  className="btn-discard"
                  onClick={handleDiscardConfirm}
                >
                  {t('discard')}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Success Toast */}
        {showToast && (
          <div className="drawer-success-toast">
            <Check size={18} />
            <span>{t('farmProfileUpdated')}</span>
          </div>
        )}
      </aside>
    </div>
  );
}

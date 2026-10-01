import React, { createContext, useContext, useState, useEffect } from 'react';
import en from './en';
import te from './te';
import hi from './hi';

export const SUPPORTED_LANGUAGES = [
  { code: 'en', label: 'English', nativeLabel: 'English' },
  { code: 'te', label: 'Telugu', nativeLabel: 'తెలుగు' },
  { code: 'hi', label: 'Hindi', nativeLabel: 'हिन्दी' }
];

const dictionaries = { en, te, hi };

export const CROP_METADATA = {
  paddy: {
    icon: '🌾',
    en: 'Paddy',
    te: 'వరి',
    hi: 'धान',
    chip: {
      en: '🌾 Weekly Paddy Farm Plan',
      te: '🌾 వారపు వరి పంట ప్రణాళిక',
      hi: '🌾 साप्ताहिक धान कृषि योजना'
    }
  },
  sugarcane: {
    icon: '🎋',
    en: 'Sugarcane',
    te: 'చెరకు',
    hi: 'गन्ना',
    chip: {
      en: '🎋 Weekly Sugarcane Farm Plan',
      te: '🎋 వారపు చెరకు పంట ప్రణాళిక',
      hi: '🎋 साप्ताहिक गन्ना कृषि योजना'
    }
  },
  black_gram: {
    icon: '🌱',
    en: 'Black Gram',
    te: 'మినుములు',
    hi: 'उड़द',
    chip: {
      en: '🌱 Weekly Black Gram Farm Plan',
      te: '🌱 వారపు మినుము పంట ప్రణాళిక',
      hi: '🌱 साप्ताहिक उड़द कृषि योजना'
    }
  },
  tomato: {
    icon: '🍅',
    en: 'Tomato',
    te: 'టమాటా',
    hi: 'टमाटर',
    chip: {
      en: '🍅 Weekly Tomato Farm Plan',
      te: '🍅 వారపు టమాటా పంట ప్రణాళిక',
      hi: '🍅 साप्ताहिक टमाटर कृषि योजना'
    }
  },
  chilli: {
    icon: '🌶️',
    en: 'Chilli',
    te: 'మిరప',
    hi: 'मिर्च',
    chip: {
      en: '🌶️ Weekly Chilli Farm Plan',
      te: '🌶️ వారపు మిరప పంట ప్రణాళిక',
      hi: '🌶️ साप्ताहिक मिर्च कृषि योजना'
    }
  },
  groundnut: {
    icon: '🥜',
    en: 'Groundnut',
    te: 'వేరుశనగ',
    hi: 'मूंगफली',
    chip: {
      en: '🥜 Weekly Groundnut Farm Plan',
      te: '🥜 వారపు వేరుశనగ పంట ప్రణాళిక',
      hi: '🥜 साप्ताहिक मूंगफली कृषि योजना'
    }
  }
};

const LanguageContext = createContext();

export function normalizeCropKey(cropName) {
  if (!cropName) return 'paddy';
  const c = cropName.toString().trim().toLowerCase();
  if (c.includes('rice') || c.includes('paddy') || c.includes('వరి') || c.includes('వడ్లు') || c.includes('धान')) return 'paddy';
  if (c.includes('sugarcane') || c.includes('చెరకు') || c.includes('गन्ना') || c.includes('sugar')) return 'sugarcane';
  if (c.includes('black') || c.includes('urad') || c.includes('మినుము') || c.includes('మినుములు') || c.includes('उड़द')) return 'black_gram';
  if (c.includes('tomato') || c.includes('టమాటా') || c.includes('టమాట') || c.includes('टमाटर')) return 'tomato';
  if (c.includes('chilli') || c.includes('chili') || c.includes('మిరప') || c.includes('మిర్చి') || c.includes('मिर्च')) return 'chilli';
  if (c.includes('groundnut') || c.includes('peanut') || c.includes('వేరుశనగ') || c.includes('मूंगफली')) return 'groundnut';
  return 'paddy';
}

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    try {
      const saved = localStorage.getItem('rythu_agent_language');
      return saved && dictionaries[saved] ? saved : 'en';
    } catch {
      return 'en';
    }
  });

  const setLanguage = (langCode) => {
    if (dictionaries[langCode]) {
      setLanguageState(langCode);
      try {
        localStorage.setItem('rythu_agent_language', langCode);
      } catch (e) {
        console.warn('Could not save language to localStorage', e);
      }
    }
  };

  const t = (key, params = {}) => {
    const dict = dictionaries[language] || dictionaries.en;
    let val = key.split('.').reduce((acc, part) => acc && acc[part], dict);
    if (!val) {
      val = key.split('.').reduce((acc, part) => acc && acc[part], dictionaries.en) || key;
    }
    if (typeof val === 'string' && params) {
      Object.entries(params).forEach(([k, v]) => {
        val = val.replace(new RegExp(`{${k}}`, 'g'), v);
      });
    }
    return val;
  };

  const getFarmPlanChip = (cropName, isMultiCrop = false) => {
    if (isMultiCrop) {
      return t('multiCropPlan');
    }
    const key = normalizeCropKey(cropName);
    const meta = CROP_METADATA[key] || CROP_METADATA.paddy;
    return meta.chip[language] || meta.chip.en;
  };

  const getServicesChip = () => {
    return t('relevantServices');
  };

  return (
    <LanguageContext.Provider value={{
      language,
      setLanguage,
      t,
      getFarmPlanChip,
      getServicesChip,
      normalizeCropKey,
      supportedLanguages: SUPPORTED_LANGUAGES
    }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}

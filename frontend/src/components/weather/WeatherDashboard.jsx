import React, { useState, useEffect } from 'react';
import { useLanguage } from '../../i18n';
import { getWeather } from '../../api/client';
import {
  CloudSun,
  Droplets,
  Wind,
  Compass,
  AlertTriangle,
  CheckCircle2,
  Calendar,
  Sparkles
} from 'lucide-react';

export default function WeatherDashboard({ farmer, onTriggerAgentPrompt }) {
  const { t } = useLanguage();
  const [weatherData, setWeatherData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const location = farmer?.district || 'Vijayawada';
  const cropDisplay = t(`crops.${farmer?.current_crop?.toLowerCase()}`) || farmer?.current_crop || 'Paddy';

  useEffect(() => {
    async function fetchWeather() {
      setIsLoading(true);
      try {
        const data = await getWeather(location, false);
        setWeatherData(data);
      } catch (err) {
        console.error('Weather fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    }
    fetchWeather();
  }, [location]);

  const temp = weatherData?.temperature_c ? `${Math.round(weatherData.temperature_c)}°C` : '31°C';
  const rainProb = weatherData?.rainfall_probability_pct !== undefined ? `${weatherData.rainfall_probability_pct}%` : '37%';
  const humidity = weatherData?.humidity_pct !== undefined ? `${weatherData.humidity_pct}%` : '54%';
  const windSpeed = weatherData?.wind_speed_kmh || '9.7 km/h';

  // 7-day forecast mock/default if daily forecast array is not populated
  const forecastDays = weatherData?.forecast_days || [
    { day: 'Today', temp_max: 33, temp_min: 24, rain_prob: 35, condition: 'Partly Cloudy', spray: 'Optimal (4:30 PM - 6:30 PM)' },
    { day: 'Tomorrow', temp_max: 32, temp_min: 25, rain_prob: 45, condition: 'Scattered Showers', spray: 'Morning Only (7:00 AM - 9:30 AM)' },
    { day: 'Day 3', temp_max: 30, temp_min: 23, rain_prob: 65, condition: 'Moderate Rain', spray: 'Unfavorable (Rain Expected)' },
    { day: 'Day 4', temp_max: 31, temp_min: 24, rain_prob: 25, condition: 'Partly Sunny', spray: 'Favorable Spray Window' },
    { day: 'Day 5', temp_max: 33, temp_min: 25, rain_prob: 15, condition: 'Clear Sky', spray: 'Optimal All Day' },
    { day: 'Day 6', temp_max: 34, temp_min: 26, rain_prob: 10, condition: 'Sunny', spray: 'Optimal All Day' },
    { day: 'Day 7', temp_max: 34, temp_min: 26, rain_prob: 20, condition: 'Clear Sky', spray: 'Optimal All Day' }
  ];

  return (
    <div className="view-content-wrapper">
      <div className="view-header-block">
        <h1 className="view-headline">
          🌦 {t('navWeather')} — {location}, Andhra Pradesh
        </h1>
        <p className="view-subheadline">
          {t('weatherHeadlineDesc')}
        </p>
      </div>

      {/* Top Weather Metrics */}
      <div className="kpi-cards-grid">
        <div className="kpi-card">
          <span className="kpi-label">{t('currentTemperature')}</span>
          <div className="kpi-val-primary">{temp}</div>
          <div className="kpi-val-sub">{t('satelliteFeed')}</div>
        </div>

        <div className="kpi-card">
          <span className="kpi-label">{t('rainProbability3Day')}</span>
          <div className="kpi-val-primary">{rainProb}</div>
          <div className="kpi-val-sub">{t('relativeHumidity')}: {humidity}</div>
        </div>

        <div className="kpi-card">
          <span className="kpi-label">{t('windSpeedDirection')}</span>
          <div className="kpi-val-primary">{windSpeed}</div>
          <div className="kpi-val-sub">{t('breezeCalm')}</div>
        </div>

        <div className="kpi-card">
          <span className="kpi-label">{t('sprayAdvisory')}</span>
          <div className="kpi-val-primary" style={{ fontSize: '18px', color: 'var(--emerald-800)' }}>
            {t('favorable')}
          </div>
          <div className="kpi-val-sub">{t('eveningWindow')}</div>
        </div>
      </div>

      {/* Agricultural Implications Banner */}
      <div style={{
        background: 'linear-gradient(135deg, #ffffff 0%, var(--emerald-50) 100%)',
        border: '1.5px solid var(--border-emerald)',
        borderRadius: 'var(--radius-lg)',
        padding: '22px 26px',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <h3 style={{ fontSize: '16px', fontWeight: 800, color: 'var(--emerald-950)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Sparkles size={18} color="var(--emerald-800)" />
          {t('agriInterpretationTitle')} — {cropDisplay} (40 {t('daysUnit')})
        </h3>
        <p style={{ margin: '8px 0 0 0', fontSize: '13.5px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          {t('agriInterpretationBody')}
        </p>
      </div>

      {/* 7-Day Forecast Table */}
      <div className="table-card-container">
        <h3 style={{ fontSize: '16px', fontWeight: 800, color: 'var(--text-main)', marginBottom: '14px' }}>
          {t('forecast7Day')}
        </h3>
        <table className="custom-data-table">
          <thead>
            <tr>
              <th>{t('date')}</th>
              <th>{t('weather')}</th>
              <th>{t('rainProbability3Day')}</th>
              <th>{t('sprayAdvisory')}</th>
            </tr>
          </thead>
          <tbody>
            {forecastDays.map((fd, i) => (
              <tr key={i}>
                <td><strong>{fd.day}</strong></td>
                <td>{fd.temp_max}°C / {fd.temp_min}°C</td>
                <td style={{ fontWeight: 700, color: fd.rain_prob > 50 ? 'var(--blue-600)' : 'var(--text-main)' }}>
                  {fd.rain_prob}%
                </td>
                <td>{fd.condition}</td>
                <td>
                  <span style={{
                    fontSize: '12px',
                    fontWeight: 600,
                    padding: '3px 8px',
                    borderRadius: 'var(--radius-full)',
                    background: fd.rain_prob > 50 ? 'var(--amber-100)' : 'var(--emerald-100)',
                    color: fd.rain_prob > 50 ? 'var(--amber-500)' : 'var(--emerald-800)'
                  }}>
                    {fd.spray}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

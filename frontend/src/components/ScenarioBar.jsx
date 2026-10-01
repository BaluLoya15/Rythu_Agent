import React from 'react';
import { PlayCircle, Award, Landmark, AlertCircle, Calendar } from 'lucide-react';

export default function ScenarioBar({ onSelectScenario, isLoading }) {
  const scenarios = [
    {
      id: 'sc-1',
      title: 'Scenario 1 (Primary): 2 Acres Tomato Market & Farm Plan',
      query: 'I have 2 acres of tomato near Vijayawada. The market price is changing and I want to know what I should do this week.',
      icon: <Award size={14} color="#10b981" />,
      primary: true
    },
    {
      id: 'sc-2',
      title: 'Scenario 2: Government Schemes & Welfare Subsidies',
      query: 'I want to know what agricultural government services may be relevant to me.',
      icon: <Landmark size={14} color="#f59e0b" />,
      primary: false
    },
    {
      id: 'sc-3',
      title: 'Scenario 3: Chilli Leaf Yellowing Diagnosis',
      query: 'My chilli plants have yellow leaves. What should I check?',
      icon: <AlertCircle size={14} color="#ef4444" />,
      primary: false
    },
    {
      id: 'sc-4',
      title: 'Scenario 4: Groundnut 40-Day Pegging Guide',
      query: 'My groundnut crop is 40 days old. What should I do now?',
      icon: <Calendar size={14} color="#60a5fa" />,
      primary: false
    }
  ];

  return (
    <div className="scenarios-bar">
      <div className="scenarios-label">
        <PlayCircle size={14} />
        <span>Judge / Demo Scenarios:</span>
      </div>
      {scenarios.map((sc) => (
        <button
          key={sc.id}
          className={`scenario-pill ${sc.primary ? 'primary' : ''}`}
          onClick={() => !isLoading && onSelectScenario(sc.query)}
          disabled={isLoading}
          title={sc.query}
        >
          {sc.icon}
          <span>{sc.title}</span>
        </button>
      ))}
    </div>
  );
}

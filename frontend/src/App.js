import React, { useState, useEffect } from "react";
import "./App.css";
import Animal from "./components/Animal";
import AddAnimalButton from "./components/AddAnimalButton";

function App() {
  const [animals, setAnimals] = useState([]);
  const [showWelcome, setShowWelcome] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Smooth page load animation
    setIsLoading(false);
  }, []);

  const addAnimal = () => {
    if (showWelcome) {
      setShowWelcome(false);
    }
    const newId = Math.max(...animals.map(a => a.id), 0) + 1;
    const newAnimal = {
      id: newId,
      name: `Subject ${newId}`,
      animal: {
        species: "",
        age: "",
        diet: "",
        healthConditions: ""
      },
      video: null,
      analysis: null,
      loading: false,
      error: null
    };
    setAnimals([...animals, newAnimal]);
  };

  const handleGetStarted = () => {
    setShowWelcome(false);
    if (animals.length === 0) {
      const newAnimal = {
        id: 1,
        name: `Subject 1`,
        animal: {
          species: "",
          age: "",
          diet: "",
          healthConditions: ""
        },
        video: null,
        analysis: null,
        loading: false,
        error: null
      };
      setAnimals([newAnimal]);
    }
  };

  const removeAnimal = (id) => {
    const newAnimals = animals.filter(a => a.id !== id);
    setAnimals(newAnimals);
    if (newAnimals.length === 0) {
      setShowWelcome(true);
    }
  };

  const updateAnimal = (id, updates) => {
    setAnimals(animals.map(a => 
      a.id === id ? { ...a, ...updates } : a
    ));
  };

  return (
    <div className={`App ${isLoading ? 'loading' : ''}`}>
      <header className="App-header">
        <div className="header-content">
          <div className="logo-container">
            <div className="logo-icon">
              <img src="/PigVisionLogo.png" alt="PigVision Logo" className="logo-image" />
            </div>
            <div className="logo-text">
              <h1 className="logo-title">FaunaVision</h1>
              <p className="logo-subtitle">AI-Powered Animal Health Analytics</p>
            </div>
          </div>
        </div>
      </header>

      <main className="App-main">
        {showWelcome ? (
          <div className="welcome-page">
            <div className="welcome-content">
              <div className="welcome-icon">
                <img src="/PigVisionLogo.png" alt="PigVision Logo" className="welcome-logo-image" />
              </div>
              <h2 className="welcome-title">Welcome to FaunaVision</h2>
              <p className="welcome-description">
                Advanced AI-powered platform for monitoring animal health through behavioral analysis.
                Upload videos to detect distress behaviors and receive comprehensive health insights.
              </p>
              <div className="features-list">
                <div className="feature-item">
                  <span className="feature-icon">✓</span>
                  <span>Real-time behavior detection</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">✓</span>
                  <span>AI-powered health assessment</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">✓</span>
                  <span>Detailed analytics & recommendations</span>
                </div>
              </div>
              <button className="get-started-button" onClick={handleGetStarted}>
                <span>Get Started</span>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </div>
          </div>
        ) : (
          <div className="main-content">
            <div className={`animals-container ${animals.length === 1 ? 'single-animal' : ''}`}>
              {animals.map((animal, index) => (
                <div 
                  key={animal.id} 
                  className="animal-wrapper"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <Animal
                    animal={animal}
                    onUpdate={(updates) => updateAnimal(animal.id, updates)}
                    onRemove={() => removeAnimal(animal.id)}
                    canRemove={animals.length > 1}
                  />
                </div>
              ))}
            </div>

            <AddAnimalButton onAdd={addAnimal} />
          </div>
        )}
      </main>

      <footer className="App-footer">
        <div className="footer-content">
          <p>© 2024 FaunaVision. Advanced AI-powered animal health monitoring.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;

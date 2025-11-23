import React, { useState, useEffect } from "react";
import "./App.css";
import Animal from "./components/Animal";
import AddAnimalButton from "./components/AddAnimalButton";

function App() {
  const [animals, setAnimals] = useState([]);
  const [showWelcome, setShowWelcome] = useState(true);
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(0);

  useEffect(() => {
    setIsLoading(false);
  }, []);

  const addAnimal = () => {
    if (showWelcome) {
      setShowWelcome(false);
    }
    const newId = Math.max(...animals.map(a => a.id), 0) + 1;
    const newAnimal = {
      id: newId,
      name: `Animal ${newId}`,
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
        name: `Animal 1`,
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

  const nextPage = () => {
    if (currentPage < 2) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  const goToPage = (page) => {
    setCurrentPage(page);
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
            <div className="welcome-container">
              {/* Page Indicators */}
              <div className="page-indicators">
                {[0, 1, 2].map((index) => (
                  <button
                    key={index}
                    className={`indicator ${currentPage === index ? 'active' : ''}`}
                    onClick={() => goToPage(index)}
                    aria-label={`Go to page ${index + 1}`}
                  />
                ))}
              </div>

              {/* Page Content with Fade Transitions */}
              <div className="pages-container">
                {/* Page 1: Get Started */}
                <div className={`welcome-page-content ${currentPage === 0 ? 'active' : ''}`}>
                  <div className="get-started-widget">
                    <div className="widget-header">
                      <div className="widget-icon">
                        <img src="/PigVisionLogo.png" alt="PigVision Logo" className="widget-logo-image" />
                      </div>
                      <h2 className="widget-title">Welcome to FaunaVision</h2>
                    </div>
                    <div className="widget-body">
                      <p className="widget-description">
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
                </div>

                {/* Page 2: Video */}
                <div className={`welcome-page-content ${currentPage === 1 ? 'active' : ''}`}>
                  <div className="video-page">
                    <h2 className="page-title">See It In Action</h2>
                    <p className="page-subtitle">Watch how FaunaVision analyzes pig behavior</p>
                    <div className="video-container">
                      <img 
                        src="/example-pig-video.gif" 
                        alt="Example pig behavior analysis" 
                        className="example-video"
                      />
                    </div>
                    <p className="video-description">
                      Our AI analyzes video footage to detect behaviors like tail biting, ear biting, 
                      aggression, eating, sleeping, and rooting patterns.
                    </p>
                  </div>
                </div>

                {/* Page 3: Workflow */}
                <div className={`welcome-page-content ${currentPage === 2 ? 'active' : ''}`}>
                  <div className="workflow-widget">
                    <div className="widget-header">
                      <h2 className="widget-title">How It Works</h2>
                      <p className="widget-subtitle">Simple three-step process</p>
                    </div>
                    <div className="widget-body">
                      <div className="workflow-steps">
                        <div className="workflow-step">
                          <div className="step-number">1</div>
                          <div className="step-content">
                            <h3 className="step-title">Upload Video</h3>
                            <p className="step-description">
                              Upload a video of the animal you want to analyze. 
                              Supports MP4, AVI, MOV, and MKV formats.
                            </p>
                          </div>
                        </div>
                        <div className="workflow-step">
                          <div className="step-number">2</div>
                          <div className="step-content">
                            <h3 className="step-title">AI Analysis</h3>
                            <p className="step-description">
                              Our dual AI system (YOLO + Gemini) analyzes the video 
                              to detect behaviors and calculate time distributions.
                            </p>
                          </div>
                        </div>
                        <div className="workflow-step">
                          <div className="step-number">3</div>
                          <div className="step-content">
                            <h3 className="step-title">Get Insights</h3>
                            <p className="step-description">
                              Receive detailed health assessment, behavior percentages, 
                              and actionable recommendations.
                            </p>
                          </div>
                        </div>
                      </div>
                      <button className="get-started-button" onClick={handleGetStarted}>
                        <span>Start Analyzing</span>
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Navigation Buttons */}
              <div className="page-navigation">
                <button 
                  className="nav-button prev-button" 
                  onClick={prevPage}
                  disabled={currentPage === 0}
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Previous</span>
                </button>
                <button 
                  className="nav-button next-button" 
                  onClick={nextPage}
                  disabled={currentPage === 2}
                >
                  <span>Next</span>
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
              </div>
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

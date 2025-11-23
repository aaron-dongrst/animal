import React, { useState } from "react";
import "./App.css";
import Animal from "./components/Animal";
import AddAnimalButton from "./components/AddAnimalButton";

function App() {
  const [animals, setAnimals] = useState([]);
  const [showWelcome, setShowWelcome] = useState(true);

  const addAnimal = () => {
    if (showWelcome) {
      setShowWelcome(false);
    }
    const newId = Math.max(...animals.map(a => a.id), 0) + 1;
    const newAnimal = {
      id: newId,
      name: `Pig ${newId}`,
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
        name: `Pig 1`,
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
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <img src="/FaunaVisionLogo.png" alt="FaunaVision Logo" className="header-logo" />
          <h1>PigVision</h1>
        </div>
      </header>

      <main className="App-main">
        {showWelcome ? (
          <div className="welcome-page">
            <div className="welcome-content">
              <h2 className="welcome-title">Welcome to PigVision</h2>
              <p className="welcome-description">
                Monitor pig health through AI-powered behavior analysis.
                Upload videos of pigs to detect distress behaviors (tail biting, ear biting, aggression) and get detailed health insights and recommendations.
              </p>
              <button className="get-started-button" onClick={handleGetStarted}>
                Get Started
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className={`animals-container ${animals.length === 1 ? 'single-animal' : ''}`}>
              {animals.map((animal) => (
                <Animal
                  key={animal.id}
                  animal={animal}
                  onUpdate={(updates) => updateAnimal(animal.id, updates)}
                  onRemove={() => removeAnimal(animal.id)}
                  canRemove={animals.length > 1}
                />
              ))}
            </div>

            <AddAnimalButton onAdd={addAnimal} />
          </>
        )}
      </main>

      <footer className="App-footer">
        <p>PigVision - Monitoring pig health through AI-powered behavior analysis</p>
      </footer>
    </div>
  );
}

export default App;

import React, { useState } from "react";
import "./App.css";
import Animal from "./components/Animal";
import AddAnimalButton from "./components/AddAnimalButton";

function App() {
  const [animals, setAnimals] = useState([
    {
      id: 1,
      name: "Animal 1",
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
    }
  ]);

  const addAnimal = () => {
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

  const removeAnimal = (id) => {
    if (animals.length > 1) {
      setAnimals(animals.filter(a => a.id !== id));
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
          <h1>FaunaVision</h1>
        </div>
      </header>

      <main className="App-main">
        <div className="animals-container">
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
      </main>

      <footer className="App-footer">
        <p>FaunaVision - Monitoring animal health through AI-powered behavior analysis</p>
      </footer>
    </div>
  );
}

export default App;

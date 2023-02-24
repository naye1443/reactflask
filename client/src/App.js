import {useEffect, useState} from "react";
import './App.css';
import Home from "./components/Pages/Home";
function App() {

  const [data, setdata] = useState({  // sets inital states of data
    Practice: "none"
  });

  useEffect(() => {
    fetch("/api").then((res) => res.json().then((data) => {
      setdata({ // Sets data
        Practice: data.Practice
      });
    })
    );
  },[]);

  return (
    <div className="App">
      <header className="App-header">
        <p>My Token = {window.token}</p>
        <p>{data.Practice}</p>
        <Home/>
      </header>
    </div>
  );
}

export default App;

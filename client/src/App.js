import React, { Component } from 'react';
import logo from './assets/images/logo.png';

class App extends Component {
  render() {
    return (
      <div className="app" style={styles.app}>
        <header className="header" style={styles.header}>
          <img src={logo} className="logo" alt="logo" style={styles.logo} />
          <h1 className="title" style={styles.title}>Epic Masterproject</h1>
        </header>
        <p className="intro" style={styles.intro}>
          We're doing awesome stuff.
        </p>
      </div>
    );
  }
}

const styles = {
  app: {
    textAlign: "center",
  },
  logo: {
    height: "80px",
  },
  header: {
    backgroundColor: "#222",
    height: "150px",
    padding: "20px",
    color: "white",
  },
  title: {
    fontSize: "1.5em",
  },
  intro: {
    fontSize: "large",
  },
}

export default App;

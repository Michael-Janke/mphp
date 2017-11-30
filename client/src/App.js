import React, { Component } from "react";
import Header from "./components/Header";
import Content from "./components/Content";
import injectTapEventPlugin from "react-tap-event-plugin";

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

class App extends Component {
  render() {
    return (
      <div className="app">
        <Header />
        <Content />
      </div>
    );
  }
}

export default App;

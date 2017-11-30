import React from "react";
import ReactDOM from "react-dom";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import { ThemeProvider } from "styled-components";

import EpicApp from "./App";
import registerServiceWorker from "./registerServiceWorker";
import "./index.css";
import * as colors from "./config/colors"; // from Step #1

const App = () => (
  <ThemeProvider theme={colors}>
    <MuiThemeProvider>
      <EpicApp />
    </MuiThemeProvider>
  </ThemeProvider>
);

ReactDOM.render(<App />, document.getElementById("root"));
registerServiceWorker();

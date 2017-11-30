import React from "react";
import ReactDOM from "react-dom";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import { ThemeProvider } from "styled-components";
import { injectGlobal } from "styled-components";

import EpicApp from "./App";
import registerServiceWorker from "./registerServiceWorker";
import Roboto from "./assets/fonts/Roboto/Roboto-Regular.ttf";
import * as colors from "./config/colors";
import * as fontSizes from "./config/fontSizes";
import * as spacings from "./config/spacings";

const App = () => (
  <ThemeProvider theme={{ ...colors, ...fontSizes, ...spacings }}>
    <MuiThemeProvider>
      <EpicApp />
    </MuiThemeProvider>
  </ThemeProvider>
);

injectGlobal`
  @font-face {
    font-family: "Roboto";
    font-style: normal;
    font-weight: 400;
    src: url(${Roboto});
  }

  body {
    margin: 0;
    padding: 0;
    font-family: "Roboto";
  }
`;

ReactDOM.render(<App />, document.getElementById("root"));
registerServiceWorker();

import React from "react";
import ReactDOM from "react-dom";
import registerServiceWorker from "./registerServiceWorker";
import EpicApp from "./App";

// Theme
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import { ThemeProvider, injectGlobal } from "styled-components";
import Roboto from "./assets/fonts/Roboto/Roboto-Regular.ttf";
import * as colors from "./config/colors";
import * as fontSizes from "./config/fontSizes";
import * as spacings from "./config/spacings";

// Redux
import { Provider } from "react-redux";
import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk"; // needed for async actions
import * as reducers from "./reducers";

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
import injectTapEventPlugin from "react-tap-event-plugin";

let store = createStore(combineReducers(reducers), applyMiddleware(thunk));

const App = () => (
  <ThemeProvider theme={{ ...colors, ...fontSizes, ...spacings }}>
    <MuiThemeProvider>
      <Provider store={store}>
        <EpicApp />
      </Provider>
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
injectTapEventPlugin();

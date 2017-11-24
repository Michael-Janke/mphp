import React from 'react';
import ReactDOM from 'react-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import EpicApp from './App';
import registerServiceWorker from './registerServiceWorker';
import './index.css';

const App = () => (
  <MuiThemeProvider>
    <EpicApp />
  </MuiThemeProvider>
);

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();

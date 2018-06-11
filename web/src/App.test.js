import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';



it('renders without crashing', () => {
  const div = document.createElement('div');
  // Empty fetch implement
  global.fetch = jest.fn().mockImplementation(() => new Promise(() => { }));
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);
});

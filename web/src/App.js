import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      client:'REACT',
      server: '',
    }

    this.fetch_who();
  }

  fetch_who() {
    fetch('/api/who').then(response => {
      if (response.ok) {
        return response.json();
      } else {
        console.log("Oh dear, our request to /api/ failed!")
        throw response;
      }
    }).then(json =>
      this.setState({
        server: json.who
      })
    );
  }

  render() {
    const { client, server } = this.state;
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to {client} + {server}</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
      </div>
    );
  }
}

export default App;

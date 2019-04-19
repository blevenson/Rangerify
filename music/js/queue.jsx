import React from 'react';

class Queue extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      songs: [],
    };

    this.handleAddButton = this.handleAddButton.bind(this);
    this.handleUpVoteButton = this.handleUpVoteButton.bind(this);
    this.handleDownVoteButton = this.handleDownVoteButton.bind(this);
    this.handleSongChange = this.handleSongChange.bind(this);

  }

  componentDidMount() {
    //this.interval = setInterval(() => this.getSongs(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }


  getSongs() {

    fetch('/api/v1/players', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })
    .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      }).then((data) => {
        this.setState(prevState => ({
          players: data.players,
        }));
      })
      .catch();

      // Update answered players
      var ansPlayers = [];
      this.state.players.forEach(function(player) {
        if(player.ans1 !== "" && player.ans2 !== "") {
          ansPlayers.push(player)
        }
      });

      this.setState(prevState => ({
          answeredPlayers: ansPlayers,
        }));

      // Check if all players have answered
      if(this.state.answeredPlayers.length === this.state.players.length && this.state.answeredPlayers.length > 0) {
        // All players have answered, next stage
        this.setState(prevState => ({
          stage: 2,
        }));
      }

      // Update voted players
      fetch('/api/v1/votedPlayers', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      }).then((data) => {
        this.setState(prevState => ({
          votedPlayers: data.voters,
        }));
      })
      .catch();

      // Check if all players have voted
      if(this.state.votedPlayers.length === this.state.players.length && this.state.votedPlayers.length > 0) {
        // All players have voted, next stage
        this.setState(prevState => ({
          stage: 3,
        }));
      }

      // Update winners
      fetch('/api/v1/winners', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      }).then((data) => {
        this.setState(prevState => ({
          winners: data.winners,
        }));
      })
      .catch();

  }

  handleAddButton(event) {
    event.preventDefault();

    this.setState({
      songs: [{"name": this.state.add_song}]
    });

    fetch('/api/v1/resetanswer', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/assignquestions', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    this.setState(prevState => ({
          stage: 1,
          answeredPlayers: [],
        }));

  }

  handleUpVoteButton() {
    fetch('/api/v1/resetanswer', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/resetquestions', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/resetvotes', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    this.setState(prevState => ({
          stage: 0,
          answeredPlayers: [],
        }));

    // Increment scores
    fetch('/api/v1/incrementScores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({"winners": this.state.winners}),
    })

  }

  handleDownVoteButton() {
    fetch('/api/v1/resetplayers', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/resetquestions', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })

    fetch('/api/v1/resetvotes', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })
  }

  handleSongChange(event) {
    this.setState({add_song: event.target.value});
    if(event.which == 13) {
      handleAddButton(event);
    }
  }


  render() {
    let output = ""

    output = (<div>
    <form className="songForm" id="song-form" onSubmit={this.handleAddButton}>
        <label>
          <input type="text" placeholder="Song" onChange={this.handleSongChange} />
        </label>
      </form>
    <button onClick={this.handleAddButton}>Add Song</button>

    <p>Current Queue...</p>

        <ul>
            {
            this.state.songs.map((song, index) =>
              <li key={index}><p>{song.name}</p> <button onClick={this.handleUpVoteButton}>Good</button><button onClick={this.handleDownVoteButton}>Bad</button> </li>)
              }
          </ul>
          </div>);
    return (
      <div className="queue">
        {output}
      </div>
    );
  }
}

Queue.propTypes = {
};

export default Queue;

import React from 'react';

class Queue extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      songs: [],
      add_song: "",
      liked_songs: [],
      disliked_songs: [],
      my_songs: [],
    };

    this.handleAddButton = this.handleAddButton.bind(this);
    this.handleUpVoteButton = this.handleUpVoteButton.bind(this);
    this.handleDownVoteButton = this.handleDownVoteButton.bind(this);
    this.handleSongChange = this.handleSongChange.bind(this);
    this.handleDeleteButton = this.handleDeleteButton.bind(this);

  }

  componentDidMount() {
    this.interval = setInterval(() => this.getSongs(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }


  getSongs() {

    fetch('/api/v1/queue', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })
    .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      }).then((data) => {
        this.setState(prevState => ({
          songs: data.queue,
        }));
      })
      .catch();
  }

  handleAddButton(event) {
    event.preventDefault();

    let new_song = this.state.add_song

    this.setState({add_song: ""});

    /*
    this.setState({
      songs: [{"name": this.state.add_song}]
    });
    */

    // Add song
    fetch('/api/v1/addsong', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({"song_title": new_song}),
    })
    .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if(data.hasOwnProperty('error')) {
          alert(data.error);
        } else {
          // Successfully added song
          this.state.my_songs.push(new_song)
        }
      })

  }

  handleUpVoteButton(e) {
    this.state.liked_songs.push(e.target.value);

    // Check if should switch vote to up vote
    let index = this.state.disliked_songs.indexOf(e.target.value);
    if (index > -1) {
      this.state.disliked_songs.splice(index, 1);
    }

    // Up vote song
    fetch('/api/v1/updatepriority', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({"song_title": e.target.value, "weight": 1}),
    })

  }

  handleDownVoteButton(e) {
    this.state.disliked_songs.push(e.target.value);

    // Check if should switch vote to down vote
    let index = this.state.liked_songs.indexOf(e.target.value);
    if (index > -1) {
      this.state.liked_songs.splice(index, 1);
    }

    // Down vote song
    fetch('/api/v1/updatepriority', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({"song_title": e.target.value, "weight": -1}),
    })
  }

  handleSongChange(event) {
    this.setState({add_song: event.target.value});
    if(event.which == 13) {
      handleAddButton(event);
    }
  }

  handleDeleteButton(e) {

    let song = e.target.value;

    // Check if should delete up vote
    let index = this.state.liked_songs.indexOf(song);
    if (index > -1) {
      this.state.liked_songs.splice(index, 1);
    }

    // Check if should delete down vote
    index = this.state.disliked_songs.indexOf(song);
    if (index > -1) {
      this.state.disliked_songs.splice(index, 1);
    }

    // Remove from my_songs
    this.state.my_songs.splice(this.state.my_songs.indexOf(song), 1);

    // Delete from server
    fetch('/api/v1/deletesong', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({"song_title": song}),
    })

  }

  getDeleteButton(title) {
    // Check if I added this song -> I can delete it
    if(this.state.my_songs.indexOf(title) >= 0)
      return (<button value={title} onClick={this.handleDeleteButton}>Put Down</button>);
    return ("");
  }


  render() {
    let output = ""
    output = (<div>
    <form className="songForm" id="song-form" onSubmit={this.handleAddButton}>
        <label>
          <input type="text" value={this.state.add_song} placeholder="Song" onChange={this.handleSongChange} />
        </label>
      </form>
    <button onClick={this.handleAddButton}>Add Song</button>

    <p>Current Queue...</p>

        <ul>
            {
            this.state.songs.map((song, index) =>
              <li key={index}>
                <p>{song[1]}: {song[0]}</p> 
                <button disabled={this.state.liked_songs.indexOf(song[1]) >= 0} value={song[1]} onClick={this.handleUpVoteButton}>Good Boy</button>
                <button disabled={this.state.disliked_songs.indexOf(song[1]) >= 0} value={song[1]} onClick={this.handleDownVoteButton}>Bad Dog</button> 

                {this.getDeleteButton(song[1])}
              </li>)
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

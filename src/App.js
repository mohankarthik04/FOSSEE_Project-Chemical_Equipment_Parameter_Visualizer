import React from "react";
import Upload from "./Upload";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <div>
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container">
          <a className="navbar-brand" href="#">⚙ Chemical Equipment Parameter Visualizer</a>
        </div>
      </nav>

      {/* Upload Section */}
      <Upload />
    </div>
  );
}

export default App;

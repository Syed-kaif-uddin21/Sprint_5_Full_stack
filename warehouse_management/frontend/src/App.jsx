import { useState } from "react";
import Login from "./components/login.jsx";

function App() {
  const [token, setToken] = useState( "");


  const handleLogin = (newToken) => {
    setToken(newToken);
  };

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }
return ( <div>
    hello
  </div>
);

}

export default App

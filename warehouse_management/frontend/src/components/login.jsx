
import { useState } from "react";

function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    if (!username || !password || (isRegister && !role)) {
      setError("All fields are required");
      return;
    }

    if (isRegister) {
      fetch("http://127.0.0.1:8001/register_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: username,
          password: password,
          role: role
        })
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.detail) {
            setError(data.detail);
          } else {
            setMsg("Registration successful! You can now log in.");
            setIsRegister(false);
            setUsername("");
            setPassword("");
            setRole("user");
          }
        })

    } else {
      fetch("http://127.0.0.1:8001/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: username,
          password: password
        })
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.detail) {
            setError(data.detail);
          } else {
            const token = data.token?.access_token || data.token;
            onLogin(token);
            setUsername("");
            setPassword("");
          }
        })
    }
  }

  return (
    <>
      <div className="add-form">
        <h2>{isRegister ? "Register User" : "Warehouse Login"}</h2>

        <form onSubmit={handleSubmit}>
          <div>
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div>
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          {isRegister && (
            <div>
              <label>Role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          )}

          <button type="submit" className="btn-primary">
            {isRegister ? "Sign Up" : "Log In"}
          </button>

          {error && <p className="error">{error}</p>}
          {msg && <p className="success">{msg}</p>}
        </form>

        <button
          type="button"
          onClick={() => {
            setIsRegister(!isRegister);
            setError("");
            setMsg("");
          }}
        >
          {isRegister
            ? "Already have an account? Login"
            : "Need an account? Register"}
        </button>
      </div>
    </>
  );
}

export default Login;

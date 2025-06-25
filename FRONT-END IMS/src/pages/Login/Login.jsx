import React from "react";
import "./Login.css";

const Login = () => {
  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-form">
          <div className="orange-box"></div>
          <h2>Login</h2>
          <p className="subtext">See your growth and get support</p>
          <label>Email*</label>
          <input type="email" placeholder="Enter your email" />
          <label>Password*</label>
          <input type="password" placeholder="minimum 8 characters" />

          <div className="remember-forgot">
            <label>
              <input type="checkbox" /> Remember me
            </label>
            <a href="#">Forgot password?</a>
          </div>

          <button className="login-btn">Login</button>

          <p className="register-text">
            Not registered yet? <a href="/Register">Create a new account</a>
          </p>
        </div>

        <div className="login-image">
          
        </div>
      </div>
    </div>
  );
};

export default Login;

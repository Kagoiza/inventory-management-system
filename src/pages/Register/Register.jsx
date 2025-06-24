import React from "react";
import "./Register.css";

const Register = () => {
  return (
    <div className="register-container">
      <div className="register-box">
        <div className="register-form">
          <div className="orange-box"></div>
          <h2>Create Account</h2>
          <p className="subtext">Join us and start managing your inventory</p>

          <label>Full Name*</label>
          <input type="text" placeholder="Enter your full name" />

          <label>Email*</label>
          <input type="email" placeholder="Enter your email" />

          <label>Password*</label>
          <input type="password" placeholder="Minimum 8 characters" />

          <label>Confirm Password*</label>
          <input type="password" placeholder="Repeat your password" />

          <button className="register-btn">Register</button>

          <p className="login-link">
            Already have an account? <a href="/login">Login here</a>
          </p>
        </div>

        <div className="register-image">
  
        </div>
      </div>
    </div>
  );
};

export default Register;

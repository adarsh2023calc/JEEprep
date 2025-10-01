import React, { useState } from "react";
import "./LoginModal.css";

const LoginModal = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({ email: "", password: "" });

  if (!isOpen) return null; // hide when not open

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Login Data:", formData);
    onClose(); // close modal after submit
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-btn" onClick={onClose}>✖</button>
        
        <h2>Welcome Back 👋</h2>
        <p>Please log in to continue</p>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>Email</label>
            <input 
              type="email"
              name="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required 
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input 
              type="password"
              name="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              required 
            />
          </div>

          <button type="submit" className="login-btn">Log In</button>
        </form>

        <p className="signup-text">
          Don’t have an account? <a href="">Sign Up</a>
        </p>
      </div>
    </div>
  );
};

export default LoginModal;

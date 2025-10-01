import React, { useState } from "react";
import "./Navbar.css"; // import CSS file

import Signup from "./Signup";
import LoginModal from "./Login";

export default function Navbar() {
   const [isLoginOpen, setIsLoginOpen] = useState(false);
   const [isSignupOpen,setIsSignupOpen] = useState(false);
  return (
    <nav className="navbar">
      {/* Logo */}
      <div className="logo">JeePrep</div>

      {/* Nav Links */}
      <ul className="nav-links">
        <li>Home</li>
        <li>About Us</li>
        <li>Contact Us</li>
      </ul>

      {/* Auth Links */}
      
      <ul className="auth-links">
        <li className="signup" onClick={() => setIsSignupOpen(true)}>
          Sign Up
        </li>
        <li className="login" onClick={() => setIsLoginOpen(true)}>
          Log In
        </li>
      </ul>

      {/* Popup login modal */}
      <LoginModal isOpen={isLoginOpen} onClose={() => setIsLoginOpen(false)} />

      {/* Popup signup modal */}
      <Signup isOpen={isSignupOpen} onClose={() => setIsSignupOpen(false)} />
    </nav>
  );
}

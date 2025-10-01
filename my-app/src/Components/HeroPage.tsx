import { useState } from "react";
import LoginModal from "./Login";
import Signup from "./Signup";

import "./HeroPage.css"

export default function Hero() {
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isSignupOpen, setIsSignupOpen] = useState(false);

  return (
    <section className="hero">
      <div className="hero-content">
        <h1>Welcome to Our Platform</h1>
        <p>Join us today and unlock the best experience.</p>
        <div className="hero-buttons">
          <button className="signup-btn" onClick={() => setIsSignupOpen(true)}>
            Get Started
          </button>
          <button className="login-btn" onClick={() => setIsLoginOpen(true)}>
            Log In
          </button>
        </div>
      </div>

      {/* Popup modals */}
      <LoginModal isOpen={isLoginOpen} onClose={() => setIsLoginOpen(false)} />
      <Signup isOpen={isSignupOpen} onClose={() => setIsSignupOpen(false)} />
    </section>
  );
}

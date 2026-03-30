import React from 'react';
import './MainPage.css';

const MainPage: React.FC = () => {
  const handleStartQuiz = (): void => {
    console.log('Quiz started!');
  };

  const handleLearnMore = (): void => {
    console.log('Learn more clicked!');
  };

  return (
    <div className="main-page">
      <header className="header">
        <h1>⭐ Pickleball Quiz</h1>
        <p>Test your pickleball knowledge!</p>
      </header>
      
      <main className="content">
        <div className="welcome-section">
          <h2>Welcome to the Pickleball Quiz</h2>
          <p>Get ready to test your knowledge about paddle specifications, gameplay, and more!</p>
          
          <div className="button-group">
            <button className="btn btn-primary" onClick={handleStartQuiz}>
              Start Quiz
            </button>
            <button className="btn btn-secondary" onClick={handleLearnMore}>
              Learn More
            </button>
          </div>
        </div>

        <div className="features">
          <div className="feature-card">
            <h3>🎯 Challenge Yourself</h3>
            <p>Test your knowledge with our comprehensive quiz questions</p>
          </div>
          <div className="feature-card">
            <h3>📊 Track Progress</h3>
            <p>Monitor your scores and see how you improve over time</p>
          </div>
          <div className="feature-card">
            <h3>🏆 Compete</h3>
            <p>Compare your scores with other pickleball enthusiasts</p>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>&copy; 2026 Pickleball Quiz. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default MainPage;

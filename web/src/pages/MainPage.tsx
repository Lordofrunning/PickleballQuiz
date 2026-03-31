import React, { useState, useEffect } from 'react';
import './MainPage.css';

const MainPage: React.FC = () => {
  const [currentImageIndex, setCurrentImageIndex] = useState<number>(0);

  // Placeholder images - replace with actual paddle images
  const carouselImages = [
    '/Images/Paddles/selPaddle.png',
    '/Images/Paddles/trans1.png',
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prev) => (prev + 1) % carouselImages.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [carouselImages.length]);

  const handleStartQuiz = (): void => {
    console.log('Quiz started!');
  };

  return (
    <div className="main-page">
      <header className="header">
        <h1>Find the best paddle for your playstyle!</h1>
      </header>
      
      <main className="content">
        <div className="hero-card">
          <div className="card-header">
            <h2>Find Your Paddle</h2>
          </div>
          
          <div className="carousel">
            <img 
              src={carouselImages[currentImageIndex]} 
              alt={`Paddle ${currentImageIndex + 1}`}
              className="carousel-image"
            />
          </div>
          
          <button className="btn btn-primary btn-full" onClick={handleStartQuiz}>
            Start Quiz
          </button>
        </div>
      </main>

      <footer className="footer">
        <div className="footer-content">
          <p>Paddle information provided by <a href="https://thepickleballstudio.notion.site/5bdf3ee752c940eba864a81bc3281164?v=a5170d43e5ab4573b18f48c363cce7ec" target="_blank" rel="noopener noreferrer">PickleBall Studio</a></p>
          <div className="social-links">
            <a href="#" className="social-icon" title="YouTube">
              <img src="" alt="YouTube" />
            </a>
            <a href="#" className="social-icon" title="Instagram">
              <img src="" alt="Instagram" />
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default MainPage;

import React from 'react';
import { motion } from 'framer-motion';
import { personalInfo } from '../data';
import { Github, Linkedin, Mail, Download } from 'lucide-react';

const Hero = () => {
  const downloadResume = async () => {
    try {
      const response = await fetch('/Resume.pdf');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Yogasunder_S_Resume.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading resume:', error);
    }
  };

  return (
    <section id="home" className="hero" style={{ paddingTop: '80px' }}>
      <div className="container">
        <div className="hero-content">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="hero-text"
          >
            <span className="hero-greeting">Hello, I'm</span>
            <h1 className="hero-name">{personalInfo.name}</h1>
            <h2 className="hero-title">{personalInfo.title}</h2>
            <p className="hero-description">{personalInfo.summary}</p>
            
            <div className="hero-buttons">
              <a href="#contact" className="btn btn-primary">
                Get In Touch
              </a>
              <a href="#projects" className="btn btn-outline">
                View Projects
              </a>
              <button 
                onClick={downloadResume} 
                className="btn btn-outline"
                style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}
              >
                <Download size={18} />
                <span>Download Resume</span>
              </button>
            </div>

            <div className="hero-social">
              <a 
                href={personalInfo.github} 
                target="_blank" 
                rel="noopener noreferrer"
                className="social-link"
                title="GitHub"
              >
                <Github size={20} />
              </a>
              <a 
                href={personalInfo.linkedin} 
                target="_blank" 
                rel="noopener noreferrer"
                className="social-link"
                title="LinkedIn"
              >
                <Linkedin size={20} />
              </a>
              <a 
                href={`mailto:${personalInfo.email}`} 
                className="social-link"
                title="Email"
              >
                <Mail size={20} />
              </a>
              
              <button 
                onClick={downloadResume}
                className="social-link"
                title="Download Resume"
                style={{ 
                  background: 'none', 
                  border: 'none', 
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  padding: '0 8px',
                  font: 'inherit',
                  color: 'inherit'
                }}
              >
                <Download size={20} />
                <span>Resume</span>
              </button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="hero-image"
          >
            <div className="image-placeholder">
              <div className="image-frame">
                <div className="image-content">
                  <img 
                    src="/images/Yoga.png"
                    alt={personalInfo.name}
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                      objectPosition: '80% 10%',
                      borderRadius: 'inherit',
                    }}
                  />
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

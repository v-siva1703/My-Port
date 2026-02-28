import React from 'react';
import { motion } from 'framer-motion';
import { Heart } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
            className="footer-text"
          >
            <h3 className="footer-logo">Siva</h3>
            <p>Full Stack Developer & AI/ML Enthusiast</p>
            <p>Building innovative solutions with cutting-edge technologies</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            viewport={{ once: true }}
            className="footer-links"
          >
            <div className="link-group">
              <h4>Quick Links</h4>
              <a href="#home">Home</a>
              <a href="#about">About</a>
              <a href="#projects">Projects</a>
              <a href="#contact">Contact</a>
            </div>
            
            <div className="link-group">
              <h4>Services</h4>
              <a href="#">Web Development</a>
              <a href="#">AI/ML Solutions</a>
              <a href="#">Data Visualization</a>
              <a href="#">UI/UX Design</a>
            </div>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          viewport={{ once: true }}
          className="footer-bottom"
        >
          <p>
            © {currentYear} Siva. All rights reserved. | Made with <Heart size={16} /> using React
          </p>
          <div className="footer-legal">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
          </div>
        </motion.div>
      </div>
    </footer>
  );
};

export default Footer;
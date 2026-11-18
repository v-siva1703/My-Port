import React from 'react';
import { motion } from 'framer-motion';
import { Heart } from 'lucide-react';
import { personalInfo } from '../data';

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
            <h3 className="footer-logo">{personalInfo.name}</h3>
            <p>{personalInfo.title}</p>
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
              <a href="/#home">Home</a>
              <a href="/#about">About</a>
              <a href="/#experience">Experience</a>
              <a href="/#projects">Projects</a>
              <a href="/#skills">Skills</a>
              <a href="/#contact">Contact</a>
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
            © {currentYear} {personalInfo.name}. All rights reserved. | Built with <Heart size={16} /> using React
          </p>
          <div className="footer-legal">
            <a href="/privacy-policy">Privacy Policy</a>
            <a href="/terms-of-service">Terms of Service</a>
          </div>
        </motion.div>
      </div>
    </footer>
  );
};

export default Footer;

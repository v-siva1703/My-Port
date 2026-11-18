import React from 'react';
import { motion } from 'framer-motion';
import { personalInfo, projects } from '../data';
import { User, MapPin, Mail, Phone, Award } from 'lucide-react';

const About = () => {
  return (
    <section id="about" className="about">
      <div className="container">
        <h2 className="section-title">About Me</h2>
        
        <div className="about-content">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="about-card"
          >
            <div className="about-info">
              <div className="info-item">
                <User size={20} />
                <div>
                  <h4>Name</h4>
                  <p>{personalInfo.name}</p>
                </div>
              </div>
              
              <div className="info-item">
                <MapPin size={20} />
                <div>
                  <h4>Location</h4>
                  <p>{personalInfo.location}</p>
                </div>
              </div>
              
              <div className="info-item">
                <Mail size={20} />
                <div>
                  <h4>Email</h4>
                  <p>{personalInfo.email}</p>
                </div>
              </div>

              <div className="info-item">
                <Phone size={20} />
                <div>
                  <h4>Mobile</h4>
                  <p>{personalInfo.phone}</p>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
            className="about-text"
          >
            <h3>Professional Summary</h3>
            <p>{personalInfo.summary}</p>
            
            <div className="about-highlights">
              <div className="highlight">
                <span className="highlight-number">{projects.length}+</span>
                <span className="highlight-text">Projects Built</span>
              </div>
              <div className="highlight">
                <span className="highlight-number">8.83</span>
                <span className="highlight-text">Engineering CGPA</span>
              </div>
              <div className="highlight">
                <span className="highlight-number">100%</span>
                <span className="highlight-text">Techno-Functional Delivery</span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default About;

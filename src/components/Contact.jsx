import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { personalInfo, languages } from '../data';
import { Mail, Phone, MapPin, Globe, Send } from 'lucide-react';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here
    console.log('Form submitted:', formData);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <section id="contact" className="contact">
      <div className="container">
        <h2 className="section-title">Get In Touch</h2>
        
        <div className="contact-content">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="contact-info"
          >
            <div className="info-card">
              <h3>Contact Information</h3>
              
              <div className="info-items">
                <div className="info-item">
                  <Mail size={20} />
                  <div>
                    <h4>Email</h4>
                    <p>{personalInfo.email}</p>
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
                  <Globe size={20} />
                  <div>
                    <h4>Languages</h4>
                    <p>{languages.join(', ')}</p>
                  </div>
                </div>

                 <div className="info-item">
                  <Phone size={20} />
                  <div>
                    <h4>Mobile Number</h4>
                    <p>+91 7094224519</p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
            className="contact-form"
          >
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <input
                  type="text"
                  name="name"
                  placeholder="Your Name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <input
                  type="email"
                  name="email"
                  placeholder="Your Email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <input
                  type="text"
                  name="subject"
                  placeholder="Subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <textarea
                  name="message"
                  placeholder="Your Message"
                  rows="5"
                  value={formData.message}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <button type="submit" className="btn">
                <Send size={18} />
                <span>Send Message</span>
              </button>
            </form>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
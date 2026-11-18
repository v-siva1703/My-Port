import React, { useState } from 'react';
import { personalInfo } from '../data';
import { Mail, MapPin, Phone, Briefcase, Send } from 'lucide-react';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Send email using Gmail with proper content
  const sendEmailViaGmail = (name, email, message) => {
    const subject = `Portfolio Contact from ${name}`;
    const body = `Name: ${name}\nEmail: ${email}\nDate: ${new Date().toLocaleString()}\n\nMessage:\n${message}\n\n---\nSent from Yogasunder's Portfolio Website`;
    const gmailLink = `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(personalInfo.email)}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.open(gmailLink, '_blank');
  };

  // Send WhatsApp message with complete details
  const sendWhatsAppMessage = (name, email, message) => {
    const phoneNumber = personalInfo.rawPhone || "8524867725";
    const whatsappMessage = `📬 *New Contact Form Submission*\n\n👤 *Name:* ${name}\n📧 *Email:* ${email}\n🕐 *Time:* ${new Date().toLocaleString()}\n\n📝 *Message:*\n${message}\n\n---\nFrom: Yogasunder's Portfolio Website`;
    const whatsappLink = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(whatsappMessage)}`;
    window.open(whatsappLink, '_blank');
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const { name, email, message } = formData;
    
    // Validate form
    if (!name || !email || !message) {
      setSubmitStatus({ type: 'error', message: '⚠️ Please fill in all fields' });
      setTimeout(() => setSubmitStatus(null), 3000);
      return;
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setSubmitStatus({ type: 'error', message: '⚠️ Please enter a valid email address' });
      setTimeout(() => setSubmitStatus(null), 3000);
      return;
    }

    setIsSubmitting(true);
    setSubmitStatus({ type: 'info', message: '⏳ Opening Gmail & WhatsApp...' });

    try {
      sendEmailViaGmail(name, email, message);
      sendWhatsAppMessage(name, email, message);
      
      setSubmitStatus({ 
        type: 'success', 
        message: '✅ Message sent! Check Gmail and WhatsApp.' 
      });
      
      setTimeout(() => {
        setFormData({ name: '', email: '', message: '' });
      }, 1000);
      
      setTimeout(() => setSubmitStatus(null), 5000);
    } catch (error) {
      setSubmitStatus({ 
        type: 'error', 
        message: '❌ Error sending message. Please try again.' 
      });
      setTimeout(() => setSubmitStatus(null), 3000);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section id="contact" className="contact">
      <div className="container">
        <h2 className="section-title">Get In Touch</h2>
        
        <div className="contact-content">
          {/* Contact Info */}
          <div className="info-card card">
            <h3>Contact Information</h3>
            <div className="info-items">
              <div className="info-item">
                <span className="info-icon">
                  <Mail size={20} />
                </span>
                <div>
                  <h4>Email</h4>
                  <p>{personalInfo.email}</p>
                </div>
              </div>
              <div className="info-item">
                <span className="info-icon">
                  <MapPin size={20} />
                </span>
                <div>
                  <h4>Location</h4>
                  <p>{personalInfo.location}</p>
                </div>
              </div>
              <div className="info-item">
                <span className="info-icon">
                  <Phone size={20} />
                </span>
                <div>
                  <h4>Mobile / WhatsApp</h4>
                  <p>{personalInfo.phone}</p>
                </div>
              </div>
              <div className="info-item">
                <span className="info-icon">
                  <Briefcase size={20} />
                </span>
                <div>
                  <h4>Availability</h4>
                  <p>Open to opportunities</p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div className="contact-form card">
            <h3>Send a Message</h3>
            <p style={{ color: 'var(--gray-light)', marginBottom: '25px', fontSize: '0.95rem' }}>
              Fill in the details below and I'll get back to you promptly.
            </p>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder=" "
                  required
                />
                <label htmlFor="name">Your Name</label>
              </div>
              
              <div className="form-group">
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder=" "
                  required
                />
                <label htmlFor="email">Your Email</label>
              </div>
              
              <div className="form-group">
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder=" "
                  rows="5"
                  required
                />
                <label htmlFor="message">Your Message</label>
              </div>

              {submitStatus && (
                <div className={`submit-status ${submitStatus.type}`}>
                  {submitStatus.message}
                </div>
              )}

              <button type="submit" className="btn" disabled={isSubmitting} style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                <Send size={18} />
                <span>{isSubmitting ? 'Sending...' : 'Send Message'}</span>
              </button>
              
              <div className="contact-note">
                <p>📌 Message will be sent via <strong>Gmail & WhatsApp</strong></p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;

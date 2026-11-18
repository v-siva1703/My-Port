import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Menu, X, Download } from 'lucide-react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const navItems = ['Home', 'About', 'Education', 'Experience', 'Projects', 'Skills', 'Achievements', 'Contact'];

  return (
    <nav className="navbar">
      <div className="container">
        <div className="nav-container">
          <motion.div 
            className="logo"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <span className="logo-text">Yogasunder S</span>
          </motion.div>

          <div className="nav-desktop">
            {navItems.map((item, index) => (
              <motion.a
                key={item}
                href={`/#${item.toLowerCase()}`}
                className="nav-link"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.05 }}
              >
                {item}
              </motion.a>
            ))}
            <motion.a
              href="/Resume.pdf"
              download="Yogasunder_S_Resume.pdf"
              className="nav-link resume-nav-link"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: navItems.length * 0.05 }}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 14px',
                borderRadius: '20px',
                background: 'rgba(99, 102, 241, 0.15)',
                border: '1px solid rgba(99, 102, 241, 0.4)',
                color: '#818cf8',
                marginLeft: '8px'
              }}
            >
              <Download size={14} />
              <span>Resume</span>
            </motion.a>
          </div>

          {/* Mobile menu toggle */}
          <button className="nav-toggle" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>

          {isOpen && (
            <motion.div 
              className="nav-mobile"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {navItems.map((item) => (
                <a
                  key={item}
                  href={`/#${item.toLowerCase()}`}
                  className="nav-link"
                  onClick={() => setIsOpen(false)}
                >
                  {item}
                </a>
              ))}
              <a
                href="/Resume.pdf"
                download="Yogasunder_S_Resume.pdf"
                className="nav-link"
                onClick={() => setIsOpen(false)}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '8px',
                  color: '#818cf8',
                  fontWeight: 600
                }}
              >
                <Download size={16} />
                <span>Download Resume</span>
              </a>
            </motion.div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

import React from 'react';
import { motion } from 'framer-motion';
import { skills } from '../data';
import { Code, Layout, Database, Briefcase, Sparkles } from 'lucide-react';

const Skills = () => {
  const skillCategories = [
    { 
      icon: <Code size={24} />, 
      title: "Programming Languages", 
      items: skills.programming 
    },
    { 
      icon: <Layout size={24} />, 
      title: "Frontend Development", 
      items: skills.frontend 
    },
    { 
      icon: <Database size={24} />, 
      title: "Backend Development", 
      items: skills.backend 
    },
    { 
      icon: <Briefcase size={24} />, 
      title: "ERP & Functional Consulting", 
      items: skills.erp 
    },
    { 
      icon: <Sparkles size={24} />, 
      title: "AI Tools & Automation", 
      items: skills.ai 
    }
  ];

  return (
    <section id="skills" className="skills">
      <div className="container">
        <h2 className="section-title">Skills & Technologies</h2>
        
        <div className="skills-grid">
          {skillCategories.map((category, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="skill-category"
            >
              <div className="category-header">
                <div className="category-icon">
                  {category.icon}
                </div>
                <h3>{category.title}</h3>
              </div>
              
              <div className="category-skills">
                {category.items.map((skill, idx) => (
                  <div key={idx} className="skill-item">
                    <span className="skill-name">{skill}</span>
                    <div className="skill-bar">
                      <motion.div
                        className="skill-level"
                        initial={{ width: 0 }}
                        whileInView={{ width: `${85 + ((idx * 7) % 15)}%` }}
                        transition={{ duration: 0.8, delay: 0.1 + idx * 0.05 }}
                        viewport={{ once: true }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Skills;

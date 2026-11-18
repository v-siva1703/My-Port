import React from 'react';
import { motion } from 'framer-motion';
import { achievements } from '../data';
import { Trophy, Award, BadgeCheck } from 'lucide-react';

const Achievements = () => {
  return (
    <section id="achievements" className="achievements">
      <div className="container">
        <h2 className="section-title">Achievements & Certifications</h2>
        
        <div className="achievements-grid">
          {achievements.map((item, index) => {
            const title = typeof item === 'object' ? item.title : item.split(' - ')[0];
            const description = typeof item === 'object' ? item.description : item.split(' - ').slice(1).join(' - ') || item;

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="achievement-card"
              >
                <div className="achievement-icon">
                  {index === 0 ? <Trophy size={28} /> : 
                   index === 1 ? <Award size={28} /> : 
                   <BadgeCheck size={28} />}
                </div>
                
                <div className="achievement-content">
                  <h3>{title}</h3>
                  <p>{description}</p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Achievements;

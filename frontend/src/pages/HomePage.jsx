import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  MessageSquare,
  HelpCircle,
  Megaphone,
  GraduationCap,
  Bot,
  Sparkles,
  ArrowRight,
  Shield,
  Clock,
  BookOpen,
} from 'lucide-react';

export default function HomePage() {
  const { isLoggedIn } = useAuth();

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <Sparkles size={16} />
            AI-Powered Student Support
          </div>
          <h1>
            Your Intelligent
            <br />
            <span className="gradient-text">University Assistant</span>
          </h1>
          <p className="hero-description">
            Get instant answers about admissions, examinations, fees, scholarships,
            campus facilities, and more — powered by advanced AI and a comprehensive
            university knowledge base.
          </p>
          <div className="hero-actions">
            <Link to="/chat" className="btn btn-primary btn-lg">
              <MessageSquare size={20} />
              Start Chatting
              <ArrowRight size={18} />
            </Link>
            {!isLoggedIn && (
              <Link to="/register" className="btn btn-outline btn-lg">
                Create Account
              </Link>
            )}
          </div>
        </div>
        <div className="hero-visual">
          <div className="hero-bot-card">
            <div className="bot-avatar-lg">
              <Bot size={48} />
            </div>
            <div className="bot-demo-messages">
              <div className="demo-msg user-demo">What are the hostel fees?</div>
              <div className="demo-msg bot-demo">
                The hostel accommodation charges are ₹45,000 per semester for
                shared rooms and ₹60,000 for single occupancy...
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2>Everything you need, one chat away</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <Bot size={28} />
            </div>
            <h3>AI Chat Assistant</h3>
            <p>
              Ask questions in natural language and get accurate, contextual answers
              from our knowledge base.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <HelpCircle size={28} />
            </div>
            <h3>FAQ Knowledge Base</h3>
            <p>
              Browse categorized FAQs covering admissions, exams, fees, scholarships,
              and campus life.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <Megaphone size={28} />
            </div>
            <h3>Announcements</h3>
            <p>
              Stay updated with the latest university notices, deadlines, and
              important information.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <Shield size={28} />
            </div>
            <h3>Verified Answers</h3>
            <p>
              Responses are grounded in official university documents and curated
              knowledge entries.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <Clock size={28} />
            </div>
            <h3>Available 24/7</h3>
            <p>
              Get help anytime — no waiting for office hours. Instant responses
              around the clock.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <BookOpen size={28} />
            </div>
            <h3>Source Transparency</h3>
            <p>
              Every answer shows its sources so you can verify the information
              from official documents.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <GraduationCap size={40} />
        <h2>Ready to get started?</h2>
        <p>Join thousands of students who use UniBot for quick, reliable answers.</p>
        <Link to="/chat" className="btn btn-primary btn-lg">
          <MessageSquare size={20} />
          Ask Your First Question
        </Link>
      </section>
    </div>
  );
}

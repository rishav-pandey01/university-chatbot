import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  MessageSquare,
  HelpCircle,
  Megaphone,
  LayoutDashboard,
  LogOut,
  LogIn,
  UserPlus,
  GraduationCap,
  Menu,
  X,
} from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const { user, isAdmin, isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
    setMobileOpen(false);
  };

  const navLinks = [
    { to: '/chat', label: 'Chat', icon: <MessageSquare size={18} /> },
    { to: '/faqs', label: 'FAQs', icon: <HelpCircle size={18} /> },
    { to: '/announcements', label: 'Notices', icon: <Megaphone size={18} /> },
  ];

  if (isAdmin) {
    navLinks.push({
      to: '/admin',
      label: 'Dashboard',
      icon: <LayoutDashboard size={18} />,
    });
  }

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <NavLink to="/" className="navbar-brand" onClick={() => setMobileOpen(false)}>
          <GraduationCap size={28} strokeWidth={2.2} />
          <span>UniBot</span>
        </NavLink>

        <button
          className="mobile-toggle"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle navigation"
        >
          {mobileOpen ? <X size={24} /> : <Menu size={24} />}
        </button>

        <div className={`navbar-links ${mobileOpen ? 'open' : ''}`}>
          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              onClick={() => setMobileOpen(false)}
            >
              {link.icon}
              <span>{link.label}</span>
            </NavLink>
          ))}

          <div className="nav-divider" />

          {isLoggedIn ? (
            <div className="nav-user-section">
              <span className="nav-user-name">
                {user.name}
                {isAdmin && <span className="admin-badge">Admin</span>}
              </span>
              <button className="nav-link logout-btn" onClick={handleLogout}>
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </div>
          ) : (
            <div className="nav-auth-section">
              <NavLink
                to="/login"
                className="nav-link"
                onClick={() => setMobileOpen(false)}
              >
                <LogIn size={18} />
                <span>Login</span>
              </NavLink>
              <NavLink
                to="/register"
                className="nav-link btn-register"
                onClick={() => setMobileOpen(false)}
              >
                <UserPlus size={18} />
                <span>Register</span>
              </NavLink>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}

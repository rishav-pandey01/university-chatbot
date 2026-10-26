import { useState, useEffect } from 'react';
import { announcementAPI } from '../api';
import { Megaphone, AlertTriangle, Calendar, Tag, Loader2 } from 'lucide-react';

export default function AnnouncementsPage() {
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnnouncements();
  }, []);

  const loadAnnouncements = async () => {
    try {
      const res = await announcementAPI.getActive();
      setAnnouncements(res.data);
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-center page-loading">
        <Loader2 size={32} className="spin" />
        <p>Loading announcements...</p>
      </div>
    );
  }

  return (
    <div className="announcements-page">
      <div className="page-header">
        <Megaphone size={32} className="page-icon" />
        <div>
          <h1>Announcements & Notices</h1>
          <p>Stay updated with the latest university information</p>
        </div>
      </div>

      {announcements.length === 0 ? (
        <div className="empty-state">
          <Megaphone size={48} />
          <h3>No announcements</h3>
          <p>There are no active announcements right now.</p>
        </div>
      ) : (
        <div className="announcements-list">
          {announcements.map((ann) => (
            <article
              key={ann.id}
              className={`announcement-card ${ann.priority === 'urgent' ? 'urgent' : ''}`}
            >
              {ann.priority === 'urgent' && (
                <div className="urgent-badge">
                  <AlertTriangle size={14} />
                  Urgent
                </div>
              )}
              <h2>{ann.title}</h2>
              <div className="announcement-meta">
                <span className="meta-item">
                  <Tag size={14} />
                  {ann.category}
                </span>
                <span className="meta-item">
                  <Calendar size={14} />
                  {new Date(ann.created_at).toLocaleDateString('en-IN', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                  })}
                </span>
              </div>
              <p className="announcement-content">{ann.content}</p>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

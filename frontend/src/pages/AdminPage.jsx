import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  analyticsAPI,
  faqAPI,
  announcementAPI,
  documentAPI,
  feedbackAPI,
} from '../api';
import {
  LayoutDashboard,
  Users,
  MessageSquare,
  HelpCircle,
  FileText,
  ThumbsUp,
  ThumbsDown,
  AlertTriangle,
  TrendingUp,
  Plus,
  Trash2,
  Edit3,
  Save,
  X,
  Upload,
  Megaphone,
  Loader2,
  Check,
  BarChart3,
  Search,
} from 'lucide-react';

export default function AdminPage() {
  const { isAdmin } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState(null);
  const [unanswered, setUnanswered] = useState([]);
  const [faqs, setFaqs] = useState([]);
  const [announcements, setAnnouncements] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [allFeedback, setAllFeedback] = useState([]);
  const [loading, setLoading] = useState(true);

  // FAQ form state
  const [faqForm, setFaqForm] = useState({ category: '', question: '', answer: '', keywords: '' });
  const [editingFaqId, setEditingFaqId] = useState(null);
  const [showFaqForm, setShowFaqForm] = useState(false);

  // Announcement form state
  const [annForm, setAnnForm] = useState({ title: '', content: '', category: 'General', priority: 'normal' });
  const [showAnnForm, setShowAnnForm] = useState(false);

  // Document upload state
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadTitle, setUploadTitle] = useState('');
  const [uploadCategory, setUploadCategory] = useState('General');
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (!isAdmin) {
      navigate('/chat');
      return;
    }
    loadAll();
  }, [isAdmin]);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [statsRes, unansRes, faqsRes, annsRes, docsRes, fbRes] = await Promise.all([
        analyticsAPI.getDashboard(),
        analyticsAPI.getUnanswered(),
        faqAPI.getAll({}),
        announcementAPI.getAll(),
        documentAPI.getAll(),
        feedbackAPI.getAll(),
      ]);
      setStats(statsRes.data);
      setUnanswered(unansRes.data);
      setFaqs(faqsRes.data);
      setAnnouncements(annsRes.data);
      setDocuments(docsRes.data);
      setAllFeedback(fbRes.data);
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  };

  // ── FAQ CRUD ──
  const handleSaveFaq = async () => {
    try {
      if (editingFaqId) {
        await faqAPI.update(editingFaqId, faqForm);
      } else {
        await faqAPI.create(faqForm);
      }
      setShowFaqForm(false);
      setEditingFaqId(null);
      setFaqForm({ category: '', question: '', answer: '', keywords: '' });
      const res = await faqAPI.getAll({});
      setFaqs(res.data);
    } catch {
      /* ignore */
    }
  };

  const startEditFaq = (faq) => {
    setFaqForm({
      category: faq.category,
      question: faq.question,
      answer: faq.answer,
      keywords: faq.keywords || '',
    });
    setEditingFaqId(faq.id);
    setShowFaqForm(true);
  };

  const handleDeleteFaq = async (id) => {
    try {
      await faqAPI.delete(id);
      setFaqs((prev) => prev.filter((f) => f.id !== id));
    } catch {
      /* ignore */
    }
  };

  // ── Announcement CRUD ──
  const handleSaveAnn = async () => {
    try {
      await announcementAPI.create(annForm);
      setShowAnnForm(false);
      setAnnForm({ title: '', content: '', category: 'General', priority: 'normal' });
      const res = await announcementAPI.getAll();
      setAnnouncements(res.data);
    } catch {
      /* ignore */
    }
  };

  const handleDeleteAnn = async (id) => {
    try {
      await announcementAPI.delete(id);
      setAnnouncements((prev) => prev.filter((a) => a.id !== id));
    } catch {
      /* ignore */
    }
  };

  // ── Document Upload ──
  const handleUpload = async () => {
    if (!uploadFile || !uploadTitle) return;
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', uploadFile);
      formData.append('title', uploadTitle);
      formData.append('category', uploadCategory);
      await documentAPI.upload(formData);
      setUploadFile(null);
      setUploadTitle('');
      setUploadCategory('General');
      const res = await documentAPI.getAll();
      setDocuments(res.data);
    } catch {
      /* ignore */
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDoc = async (id) => {
    try {
      await documentAPI.delete(id);
      setDocuments((prev) => prev.filter((d) => d.id !== id));
    } catch {
      /* ignore */
    }
  };

  // ── Resolve Query ──
  const handleResolve = async (id) => {
    try {
      await analyticsAPI.resolveQuery(id, { resolved: true });
      setUnanswered((prev) => prev.filter((q) => q.id !== id));
    } catch {
      /* ignore */
    }
  };

  if (loading) {
    return (
      <div className="loading-center page-loading">
        <Loader2 size={32} className="spin" />
        <p>Loading dashboard...</p>
      </div>
    );
  }

  const tabs = [
    { key: 'overview', label: 'Overview', icon: <BarChart3 size={18} /> },
    { key: 'faqs', label: 'FAQs', icon: <HelpCircle size={18} /> },
    { key: 'announcements', label: 'Notices', icon: <Megaphone size={18} /> },
    { key: 'documents', label: 'Documents', icon: <FileText size={18} /> },
    { key: 'unanswered', label: 'Unanswered', icon: <AlertTriangle size={18} /> },
    { key: 'feedback', label: 'Feedback', icon: <ThumbsUp size={18} /> },
  ];

  return (
    <div className="admin-page">
      <div className="page-header">
        <LayoutDashboard size={32} className="page-icon" />
        <div>
          <h1>Admin Dashboard</h1>
          <p>Manage the university chatbot knowledge base and analytics</p>
        </div>
      </div>

      <div className="admin-tabs">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            className={`admin-tab ${activeTab === tab.key ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.key)}
          >
            {tab.icon}
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* ── Overview Tab ── */}
      {activeTab === 'overview' && stats && (
        <div className="admin-section">
          <div className="stats-grid">
            <div className="stat-card">
              <Users size={24} />
              <div>
                <span className="stat-value">{stats.total_users}</span>
                <span className="stat-label">Total Users</span>
              </div>
            </div>
            <div className="stat-card">
              <MessageSquare size={24} />
              <div>
                <span className="stat-value">{stats.total_conversations}</span>
                <span className="stat-label">Conversations</span>
              </div>
            </div>
            <div className="stat-card">
              <Search size={24} />
              <div>
                <span className="stat-value">{stats.total_queries}</span>
                <span className="stat-label">Total Queries</span>
              </div>
            </div>
            <div className="stat-card">
              <HelpCircle size={24} />
              <div>
                <span className="stat-value">{stats.total_faqs}</span>
                <span className="stat-label">FAQs</span>
              </div>
            </div>
            <div className="stat-card">
              <FileText size={24} />
              <div>
                <span className="stat-value">{stats.total_documents}</span>
                <span className="stat-label">Documents</span>
              </div>
            </div>
            <div className="stat-card">
              <TrendingUp size={24} />
              <div>
                <span className="stat-value">{stats.satisfaction_rate}%</span>
                <span className="stat-label">Satisfaction</span>
              </div>
            </div>
          </div>

          <div className="stats-row">
            <div className="stat-detail-card">
              <h3>Feedback Summary</h3>
              <div className="feedback-summary">
                <div className="fb-item positive">
                  <ThumbsUp size={20} />
                  <span>{stats.feedback_helpful_count} Helpful</span>
                </div>
                <div className="fb-item negative">
                  <ThumbsDown size={20} />
                  <span>{stats.feedback_unhelpful_count} Unhelpful</span>
                </div>
              </div>
              <div className="fallback-info">
                <AlertTriangle size={16} />
                Fallback Rate: <strong>{stats.fallback_rate}%</strong>
              </div>
            </div>

            <div className="stat-detail-card">
              <h3>Query Categories</h3>
              <div className="category-bars">
                {stats.category_distribution.map((cat) => (
                  <div key={cat.category} className="cat-bar-row">
                    <span className="cat-name">{cat.category}</span>
                    <div className="cat-bar-track">
                      <div
                        className="cat-bar-fill"
                        style={{
                          width: `${Math.min((cat.count / Math.max(...stats.category_distribution.map((c) => c.count), 1)) * 100, 100)}%`,
                        }}
                      />
                    </div>
                    <span className="cat-count">{cat.count}</span>
                  </div>
                ))}
                {stats.category_distribution.length === 0 && (
                  <p className="empty-text">No query data yet</p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── FAQs Management Tab ── */}
      {activeTab === 'faqs' && (
        <div className="admin-section">
          <div className="section-header">
            <h3>Manage FAQs ({faqs.length})</h3>
            <button
              className="btn btn-primary btn-sm"
              onClick={() => {
                setShowFaqForm(true);
                setEditingFaqId(null);
                setFaqForm({ category: '', question: '', answer: '', keywords: '' });
              }}
            >
              <Plus size={16} />
              Add FAQ
            </button>
          </div>

          {showFaqForm && (
            <div className="admin-form-card">
              <h4>{editingFaqId ? 'Edit FAQ' : 'New FAQ'}</h4>
              <div className="form-grid">
                <div className="form-group">
                  <label>Category</label>
                  <input
                    type="text"
                    value={faqForm.category}
                    onChange={(e) => setFaqForm({ ...faqForm, category: e.target.value })}
                    placeholder="e.g. Admissions"
                  />
                </div>
                <div className="form-group">
                  <label>Keywords (comma-separated)</label>
                  <input
                    type="text"
                    value={faqForm.keywords}
                    onChange={(e) => setFaqForm({ ...faqForm, keywords: e.target.value })}
                    placeholder="e.g. eligibility, criteria"
                  />
                </div>
                <div className="form-group full">
                  <label>Question</label>
                  <input
                    type="text"
                    value={faqForm.question}
                    onChange={(e) => setFaqForm({ ...faqForm, question: e.target.value })}
                    placeholder="Enter the question"
                  />
                </div>
                <div className="form-group full">
                  <label>Answer</label>
                  <textarea
                    value={faqForm.answer}
                    onChange={(e) => setFaqForm({ ...faqForm, answer: e.target.value })}
                    placeholder="Enter the answer"
                    rows={4}
                  />
                </div>
              </div>
              <div className="form-actions">
                <button className="btn btn-primary btn-sm" onClick={handleSaveFaq}>
                  <Save size={16} />
                  {editingFaqId ? 'Update' : 'Create'}
                </button>
                <button
                  className="btn btn-ghost btn-sm"
                  onClick={() => {
                    setShowFaqForm(false);
                    setEditingFaqId(null);
                  }}
                >
                  <X size={16} />
                  Cancel
                </button>
              </div>
            </div>
          )}

          <div className="admin-table-container">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Question</th>
                  <th>Answer</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {faqs.map((faq) => (
                  <tr key={faq.id}>
                    <td><span className="table-tag">{faq.category}</span></td>
                    <td className="truncate-cell">{faq.question}</td>
                    <td className="truncate-cell">{faq.answer}</td>
                    <td>
                      <div className="table-actions">
                        <button className="icon-btn" onClick={() => startEditFaq(faq)} title="Edit">
                          <Edit3 size={14} />
                        </button>
                        <button className="icon-btn danger" onClick={() => handleDeleteFaq(faq.id)} title="Delete">
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ── Announcements Management Tab ── */}
      {activeTab === 'announcements' && (
        <div className="admin-section">
          <div className="section-header">
            <h3>Manage Announcements ({announcements.length})</h3>
            <button className="btn btn-primary btn-sm" onClick={() => setShowAnnForm(true)}>
              <Plus size={16} />
              New Announcement
            </button>
          </div>

          {showAnnForm && (
            <div className="admin-form-card">
              <h4>New Announcement</h4>
              <div className="form-grid">
                <div className="form-group full">
                  <label>Title</label>
                  <input
                    type="text"
                    value={annForm.title}
                    onChange={(e) => setAnnForm({ ...annForm, title: e.target.value })}
                    placeholder="Announcement title"
                  />
                </div>
                <div className="form-group">
                  <label>Category</label>
                  <input
                    type="text"
                    value={annForm.category}
                    onChange={(e) => setAnnForm({ ...annForm, category: e.target.value })}
                    placeholder="e.g. Academic"
                  />
                </div>
                <div className="form-group">
                  <label>Priority</label>
                  <select
                    value={annForm.priority}
                    onChange={(e) => setAnnForm({ ...annForm, priority: e.target.value })}
                  >
                    <option value="normal">Normal</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>
                <div className="form-group full">
                  <label>Content</label>
                  <textarea
                    value={annForm.content}
                    onChange={(e) => setAnnForm({ ...annForm, content: e.target.value })}
                    placeholder="Announcement details..."
                    rows={4}
                  />
                </div>
              </div>
              <div className="form-actions">
                <button className="btn btn-primary btn-sm" onClick={handleSaveAnn}>
                  <Save size={16} />
                  Publish
                </button>
                <button className="btn btn-ghost btn-sm" onClick={() => setShowAnnForm(false)}>
                  <X size={16} />
                  Cancel
                </button>
              </div>
            </div>
          )}

          <div className="admin-cards-list">
            {announcements.map((ann) => (
              <div key={ann.id} className={`admin-list-card ${ann.priority === 'urgent' ? 'urgent' : ''}`}>
                <div className="admin-list-card-body">
                  <h4>{ann.title}</h4>
                  <p>{ann.content}</p>
                  <div className="admin-list-meta">
                    <span className="table-tag">{ann.category}</span>
                    <span className={`priority-tag ${ann.priority}`}>{ann.priority}</span>
                    <span>{new Date(ann.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <button className="icon-btn danger" onClick={() => handleDeleteAnn(ann.id)} title="Delete">
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Documents Management Tab ── */}
      {activeTab === 'documents' && (
        <div className="admin-section">
          <div className="section-header">
            <h3>Knowledge Base Documents ({documents.length})</h3>
          </div>

          <div className="admin-form-card">
            <h4>Upload Document</h4>
            <div className="form-grid">
              <div className="form-group">
                <label>Title</label>
                <input
                  type="text"
                  value={uploadTitle}
                  onChange={(e) => setUploadTitle(e.target.value)}
                  placeholder="Document title"
                />
              </div>
              <div className="form-group">
                <label>Category</label>
                <input
                  type="text"
                  value={uploadCategory}
                  onChange={(e) => setUploadCategory(e.target.value)}
                  placeholder="e.g. Academic Policies"
                />
              </div>
              <div className="form-group full">
                <label>File (PDF, TXT, MD)</label>
                <input
                  type="file"
                  accept=".pdf,.txt,.md"
                  onChange={(e) => setUploadFile(e.target.files[0])}
                />
              </div>
            </div>
            <div className="form-actions">
              <button
                className="btn btn-primary btn-sm"
                onClick={handleUpload}
                disabled={!uploadFile || !uploadTitle || uploading}
              >
                {uploading ? <Loader2 size={16} className="spin" /> : <Upload size={16} />}
                {uploading ? 'Uploading...' : 'Upload'}
              </button>
            </div>
          </div>

          <div className="admin-table-container">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>File</th>
                  <th>Category</th>
                  <th>Size</th>
                  <th>Chunks</th>
                  <th>Uploaded</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.id}>
                    <td>{doc.title}</td>
                    <td className="truncate-cell">{doc.filename}</td>
                    <td><span className="table-tag">{doc.category}</span></td>
                    <td>{doc.file_size_kb} KB</td>
                    <td>{doc.chunk_count}</td>
                    <td>{new Date(doc.uploaded_at).toLocaleDateString()}</td>
                    <td>
                      <button className="icon-btn danger" onClick={() => handleDeleteDoc(doc.id)} title="Delete">
                        <Trash2 size={14} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ── Unanswered Queries Tab ── */}
      {activeTab === 'unanswered' && (
        <div className="admin-section">
          <div className="section-header">
            <h3>Unanswered / Fallback Queries ({unanswered.length})</h3>
          </div>

          {unanswered.length === 0 ? (
            <div className="empty-state">
              <Check size={48} />
              <h3>All caught up!</h3>
              <p>No unanswered queries at this time.</p>
            </div>
          ) : (
            <div className="admin-cards-list">
              {unanswered.map((q) => (
                <div key={q.id} className="admin-list-card">
                  <div className="admin-list-card-body">
                    <p className="query-text">&ldquo;{q.query_text}&rdquo;</p>
                    <div className="admin-list-meta">
                      <span className="table-tag">{q.detected_category || 'Uncategorized'}</span>
                      {q.similarity_score != null && (
                        <span>Match: {(q.similarity_score * 100).toFixed(0)}%</span>
                      )}
                      <span>{new Date(q.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                  <button className="btn btn-outline btn-sm" onClick={() => handleResolve(q.id)}>
                    <Check size={14} />
                    Resolve
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ── Feedback Tab ── */}
      {activeTab === 'feedback' && (
        <div className="admin-section">
          <div className="section-header">
            <h3>Recent Feedback ({allFeedback.length})</h3>
          </div>

          {allFeedback.length === 0 ? (
            <div className="empty-state">
              <ThumbsUp size={48} />
              <h3>No feedback yet</h3>
              <p>Feedback from users will appear here.</p>
            </div>
          ) : (
            <div className="admin-table-container">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Rating</th>
                    <th>Comment</th>
                    <th>Message ID</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {allFeedback.map((fb) => (
                    <tr key={fb.id}>
                      <td>
                        <span className={`rating-badge ${fb.rating}`}>
                          {fb.rating === 'helpful' ? <ThumbsUp size={14} /> : <ThumbsDown size={14} />}
                          {fb.rating}
                        </span>
                      </td>
                      <td>{fb.comment || '—'}</td>
                      <td>#{fb.message_id}</td>
                      <td>{new Date(fb.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

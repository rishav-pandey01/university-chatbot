import { useState, useEffect } from 'react';
import { faqAPI } from '../api';
import { HelpCircle, Search, ChevronDown, ChevronUp, Tag, Loader2 } from 'lucide-react';

export default function FAQPage() {
  const [faqs, setFaqs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [search, setSearch] = useState('');
  const [expanded, setExpanded] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCategories();
    loadFaqs();
  }, []);

  const loadCategories = async () => {
    try {
      const res = await faqAPI.getCategories();
      setCategories(['All', ...res.data]);
    } catch {
      /* ignore */
    }
  };

  const loadFaqs = async (category, searchTerm) => {
    setLoading(true);
    try {
      const params = {};
      if (category && category !== 'All') params.category = category;
      if (searchTerm) params.search = searchTerm;
      const res = await faqAPI.getAll(params);
      setFaqs(res.data);
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryChange = (cat) => {
    setSelectedCategory(cat);
    setExpanded(null);
    loadFaqs(cat, search);
  };

  const handleSearch = (e) => {
    const term = e.target.value;
    setSearch(term);
    setExpanded(null);
    loadFaqs(selectedCategory, term);
  };

  const toggleExpand = (id) => {
    setExpanded(expanded === id ? null : id);
  };

  // Group FAQs by category
  const grouped = faqs.reduce((acc, faq) => {
    if (!acc[faq.category]) acc[faq.category] = [];
    acc[faq.category].push(faq);
    return acc;
  }, {});

  return (
    <div className="faq-page">
      <div className="page-header">
        <HelpCircle size={32} className="page-icon" />
        <div>
          <h1>Frequently Asked Questions</h1>
          <p>Find answers to common queries about university life</p>
        </div>
      </div>

      <div className="faq-controls">
        <div className="search-bar">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search questions..."
            value={search}
            onChange={handleSearch}
          />
        </div>
        <div className="category-pills">
          {categories.map((cat) => (
            <button
              key={cat}
              className={`pill ${selectedCategory === cat ? 'active' : ''}`}
              onClick={() => handleCategoryChange(cat)}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="loading-center">
          <Loader2 size={32} className="spin" />
          <p>Loading FAQs...</p>
        </div>
      ) : faqs.length === 0 ? (
        <div className="empty-state">
          <HelpCircle size={48} />
          <h3>No FAQs found</h3>
          <p>Try a different search term or category.</p>
        </div>
      ) : (
        <div className="faq-list">
          {Object.entries(grouped).map(([category, items]) => (
            <div key={category} className="faq-category-group">
              <h2 className="category-heading">
                <Tag size={18} />
                {category}
                <span className="count">{items.length}</span>
              </h2>
              {items.map((faq) => (
                <div
                  key={faq.id}
                  className={`faq-item ${expanded === faq.id ? 'expanded' : ''}`}
                >
                  <button className="faq-question" onClick={() => toggleExpand(faq.id)}>
                    <span>{faq.question}</span>
                    {expanded === faq.id ? (
                      <ChevronUp size={20} />
                    ) : (
                      <ChevronDown size={20} />
                    )}
                  </button>
                  {expanded === faq.id && (
                    <div className="faq-answer">
                      <p>{faq.answer}</p>
                      {faq.keywords && (
                        <div className="faq-keywords">
                          {faq.keywords.split(',').map((kw, i) => (
                            <span key={i} className="keyword-tag">
                              {kw.trim()}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

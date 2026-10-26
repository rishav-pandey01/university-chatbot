import { useState, useEffect, useRef } from 'react';
import { chatAPI, feedbackAPI } from '../api';
import { useAuth } from '../context/AuthContext';
import {
  Send,
  Bot,
  UserCircle,
  Sparkles,
  MessageSquarePlus,
  History,
  Trash2,
  ThumbsUp,
  ThumbsDown,
  ChevronDown,
  BookOpen,
  Loader2,
  AlertTriangle,
  X,
} from 'lucide-react';

export default function ChatPage() {
  const { user, isLoggedIn } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [suggested, setSuggested] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    chatAPI.getSuggested().then((res) => setSuggested(res.data)).catch(() => {});
  }, []);

  useEffect(() => {
    if (isLoggedIn) {
      loadConversations();
    }
  }, [isLoggedIn]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      const res = await chatAPI.getConversations();
      setConversations(res.data);
    } catch {
      /* ignore */
    }
  };

  const loadConversation = async (id) => {
    setLoadingHistory(true);
    try {
      const res = await chatAPI.getConversation(id);
      const msgs = res.data.messages.map((m) => ({
        id: m.id,
        sender: m.sender,
        content: m.content,
        sources: m.sources_json ? JSON.parse(m.sources_json) : [],
        timestamp: m.timestamp,
      }));
      setMessages(msgs);
      setConversationId(id);
      setSidebarOpen(false);
    } catch {
      /* ignore */
    } finally {
      setLoadingHistory(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setConversationId(null);
    setInput('');
    setSidebarOpen(false);
    inputRef.current?.focus();
  };

  const handleDeleteConversation = async (id, e) => {
    e.stopPropagation();
    try {
      await chatAPI.deleteConversation(id);
      setConversations((prev) => prev.filter((c) => c.id !== id));
      if (conversationId === id) startNewChat();
    } catch {
      /* ignore */
    }
  };

  const sendMessage = async (text) => {
    const msg = text || input.trim();
    if (!msg || sending) return;

    const userMessage = { sender: 'user', content: msg, id: Date.now() };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setSending(true);

    try {
      const res = await chatAPI.sendMessage({
        message: msg,
        conversation_id: conversationId,
      });
      const data = res.data;
      setConversationId(data.conversation_id);

      const botMessage = {
        id: data.message_id,
        sender: 'bot',
        content: data.content,
        sources: data.sources || [],
        fallback: data.fallback_triggered,
        followups: data.suggested_followups || [],
        timestamp: data.timestamp,
      };
      setMessages((prev) => [...prev, botMessage]);

      if (isLoggedIn) loadConversations();
    } catch (err) {
      console.error('Chat error:', err);
      const detailMsg =
        err.response?.data?.detail ||
        (err.message === 'Network Error'
          ? 'Network Error: Unable to reach the backend on port 8000. Please ensure the backend server is running.'
          : 'Sorry, something went wrong. Please check your backend terminal for details.');
      const errMsg = {
        sender: 'bot',
        content: detailMsg,
        id: Date.now() + 1,
        error: true,
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleFeedback = async (messageId, rating) => {
    try {
      await feedbackAPI.submit({ message_id: messageId, rating });
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? { ...m, feedbackGiven: rating } : m))
      );
    } catch {
      /* ignore */
    }
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="chat-page">
      {/* Sidebar - Conversation History */}
      {isLoggedIn && (
        <aside className={`chat-sidebar ${sidebarOpen ? 'open' : ''}`}>
          <div className="sidebar-header">
            <h3>
              <History size={18} />
              Chat History
            </h3>
            <button className="sidebar-close" onClick={() => setSidebarOpen(false)}>
              <X size={20} />
            </button>
          </div>
          <button className="btn btn-outline new-chat-btn" onClick={startNewChat}>
            <MessageSquarePlus size={18} />
            New Chat
          </button>
          <div className="conversation-list">
            {conversations.map((conv) => (
              <div
                key={conv.id}
                className={`conversation-item ${conv.id === conversationId ? 'active' : ''}`}
                onClick={() => loadConversation(conv.id)}
              >
                <div className="conv-info">
                  <span className="conv-title">{conv.title}</span>
                  <span className="conv-meta">
                    {conv.message_count} msgs ·{' '}
                    {new Date(conv.updated_at).toLocaleDateString()}
                  </span>
                </div>
                <button
                  className="conv-delete"
                  onClick={(e) => handleDeleteConversation(conv.id, e)}
                  title="Delete conversation"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))}
            {conversations.length === 0 && (
              <p className="empty-text">No conversations yet</p>
            )}
          </div>
        </aside>
      )}

      {/* Main Chat Area */}
      <div className="chat-main">
        {/* Chat Header */}
        <div className="chat-header">
          {isLoggedIn && (
            <button
              className="history-toggle"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              title="Chat history"
            >
              <History size={20} />
            </button>
          )}
          <div className="chat-header-info">
            <Bot size={24} />
            <div>
              <h2>University Assistant</h2>
              <span className="status-dot">Online</span>
            </div>
          </div>
          {hasMessages && (
            <button className="btn btn-ghost btn-sm" onClick={startNewChat}>
              <MessageSquarePlus size={16} />
              New Chat
            </button>
          )}
        </div>

        {/* Messages Area */}
        <div className="chat-messages">
          {!hasMessages && (
            <div className="chat-welcome">
              <div className="welcome-icon">
                <Sparkles size={48} />
              </div>
              <h2>Hi{user ? `, ${user.name}` : ''}! 👋</h2>
              <p>
                I&apos;m your university assistant. Ask me about admissions, exams,
                fees, scholarships, campus life, or anything else!
              </p>

              {suggested.length > 0 && (
                <div className="suggested-grid">
                  {suggested.slice(0, 8).map((s, i) => (
                    <button
                      key={i}
                      className="suggested-chip"
                      onClick={() => sendMessage(s.question)}
                    >
                      <span className="chip-category">{s.category}</span>
                      <span className="chip-question">{s.question}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {loadingHistory && (
            <div className="loading-center">
              <Loader2 size={32} className="spin" />
              <p>Loading conversation...</p>
            </div>
          )}

          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`message ${msg.sender === 'user' ? 'message-user' : 'message-bot'} ${msg.error ? 'message-error' : ''}`}
            >
              <div className="message-avatar">
                {msg.sender === 'user' ? (
                  <UserCircle size={28} />
                ) : (
                  <Bot size={28} />
                )}
              </div>
              <div className="message-body">
                <div className="message-content">
                  {msg.fallback && (
                    <div className="fallback-notice">
                      <AlertTriangle size={14} />
                      <span>Best-effort answer based on available knowledge</span>
                    </div>
                  )}
                  <p>{msg.content}</p>
                </div>

                {/* Sources */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="message-sources">
                    <BookOpen size={14} />
                    <span>Sources: </span>
                    {msg.sources.map((s, i) => (
                      <span key={i} className="source-tag">
                        {s.title}
                        {s.similarity != null && ` (${(s.similarity * 100).toFixed(0)}%)`}
                      </span>
                    ))}
                  </div>
                )}

                {/* Feedback buttons */}
                {msg.sender === 'bot' && !msg.error && msg.id && typeof msg.id === 'number' && (
                  <div className="message-feedback">
                    {msg.feedbackGiven ? (
                      <span className="feedback-thanks">
                        Thanks for your feedback!
                      </span>
                    ) : (
                      <>
                        <button
                          className="feedback-btn"
                          onClick={() => handleFeedback(msg.id, 'helpful')}
                          title="Helpful"
                        >
                          <ThumbsUp size={14} />
                        </button>
                        <button
                          className="feedback-btn"
                          onClick={() => handleFeedback(msg.id, 'unhelpful')}
                          title="Not helpful"
                        >
                          <ThumbsDown size={14} />
                        </button>
                      </>
                    )}
                  </div>
                )}

                {/* Follow-up suggestions */}
                {msg.followups && msg.followups.length > 0 && (
                  <div className="followup-suggestions">
                    {msg.followups.map((q, i) => (
                      <button
                        key={i}
                        className="followup-chip"
                        onClick={() => sendMessage(q)}
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {sending && (
            <div className="message message-bot">
              <div className="message-avatar">
                <Bot size={28} />
              </div>
              <div className="message-body">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="chat-input-area">
          <div className="chat-input-wrapper">
            <textarea
              ref={inputRef}
              className="chat-input"
              placeholder="Ask me anything about the university..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
              disabled={sending}
            />
            <button
              className="send-btn"
              onClick={() => sendMessage()}
              disabled={!input.trim() || sending}
              title="Send message"
            >
              {sending ? <Loader2 size={20} className="spin" /> : <Send size={20} />}
            </button>
          </div>
          <p className="chat-disclaimer">
            UniBot may produce inaccurate information. Verify important details with official university channels.
          </p>
        </div>
      </div>
    </div>
  );
}

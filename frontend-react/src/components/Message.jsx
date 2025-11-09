import React from 'react';

export default function Message({ who = 'bot', text, html = false }) {
  return (
    <div className={`row ${who}`}>
      {who === 'bot' && <div className="avatar">🤖</div>}

      {html ? (
        <div
          className="msg"
          dangerouslySetInnerHTML={{ __html: text }}
        />
      ) : (
        <div className="msg">{text}</div>
      )}

      {who === 'user' && <div className="avatar">👤</div>}
    </div>
  );
}

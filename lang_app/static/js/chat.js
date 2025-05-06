// for the emoji picker
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('emoji-picker-btn');
  const picker = document.getElementById('emoji-picker');
  const input = document.getElementById('emoji-input');

  btn.addEventListener('click', (e) => {
    // Toggle picker visibility
    picker.style.display = picker.style.display === 'none' ? 'block' : 'none';
  });

  input.addEventListener('click', (e) => {
    picker.style.display = 'none';
  })

  picker.addEventListener('emoji-click', event => {
    input.value += event.detail.unicode;
  });
});

// to display the users time not the servers
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.chat-date').forEach(el => {
      const sentTime = new Date(el.dataset.sentTime);
      const now = new Date();

      const sameDay = sentTime.toDateString() === now.toDateString();
      const yesterday = (new Date(now.setDate(now.getDate() - 1))).toDateString() === sentTime.toDateString();

      let formatted = "";

      if (sameDay) {
        formatted = sentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      } else if (yesterday) {
        formatted = "Yesterday at " + sentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      } else {
        formatted = sentTime.toLocaleDateString();
      }

      el.textContent = formatted;
    });
  });

// to scroll to the last message in the chat when i open the chat
  window.addEventListener("load", () => {
    setTimeout(() => {
      const chat = document.getElementById('chat');
      if (chat) {
        chat.scrollTop = chat.scrollHeight;
        console.log("Scrolled to:", chat.scrollTop); // debug line
      }
    }, 100); // wait a moment to ensure DOM is painted
  });
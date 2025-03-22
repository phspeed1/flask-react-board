import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [posts, setPosts] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_BASE_URL}/posts`).then((response) => {
      setPosts(response.data);
    });
  }, []);


  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post(`${process.env.REACT_APP_API_BASE_URL}/posts`, { title, content }).then(() => {
      setTitle("");
      setContent("");
      window.location.reload();
    });
  };

  return (
    <div>
      <h1>📌 게시판</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
        <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
        <button type="submit">게시글 등록</button>
      </form>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.content}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

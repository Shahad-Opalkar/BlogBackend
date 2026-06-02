import { useEffect, useState } from "react";
import api from "../api/axios";

function Posts() {
const [posts, setPosts] = useState([
  { id: 1, title: "Test", content: "Hello" }
]);
  useEffect(() => {
    api.get("/posts")
      .then((res) => {
        setPosts(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <div>
      <h2>Posts</h2>
      {posts.map((post) => (
        <div key={post.id}>
          <h4>{post.title}</h4>
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
}

export default Posts;
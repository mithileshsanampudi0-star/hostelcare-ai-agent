import React, { useState } from "react";
import { submitComplaint } from "../api/client";

const EMAIL_REGEX = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

function ComplaintForm({ onResult }) {
  const [text, setText] = useState("");
  const [email, setEmail] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0] || null;
    setImageFile(file);
    setImagePreview(file ? URL.createObjectURL(file) : null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim() && !imageFile) return;

    const trimmedEmail = email.trim();
    if (trimmedEmail && !EMAIL_REGEX.test(trimmedEmail)) {
      setError("That email address doesn't look valid. Please check it and try again.");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await submitComplaint({
        text: text.trim(),
        imageFile,
        email: trimmedEmail,
      });
      onResult(result);
      setText("");
      setImageFile(null);
      setImagePreview(null);
      setEmail("");
    } catch (err) {
      const backendMessage = err.response?.data?.error;
      setError(backendMessage || "Failed to submit complaint. Is the backend running?");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="complaint-form">
      <h2>Report an Issue</h2>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="e.g. Bathroom tap in room 204 has been leaking for 3 days"
        rows={4}
      />

      <label className="file-label">
        📷 Attach a photo (optional)
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={handleImageChange}
        />
      </label>
      {imagePreview && (
        <img src={imagePreview} alt="Complaint preview" className="image-preview" />
      )}

      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Your email (optional, for status updates)"
      />

      <button type="submit" disabled={loading}>
        {loading ? "Thinking..." : "Submit Complaint"}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}

export default ComplaintForm;

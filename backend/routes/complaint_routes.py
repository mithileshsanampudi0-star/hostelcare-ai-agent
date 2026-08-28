import re
from flask import Blueprint, request, jsonify
from agent.tool_agent import run_agent
from agent.vision import describe_image

complaint_bp = Blueprint("complaint", __name__)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_BYTES = 8 * 1024 * 1024  # 8MB

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email):
    return bool(EMAIL_REGEX.match(email))


@complaint_bp.route("/api/complaint", methods=["POST"])
def submit_complaint():
    text = ""
    student_email = None
    image_description = None

    if request.content_type and "multipart/form-data" in request.content_type:
        text = (request.form.get("text") or "").strip()
        student_email = (request.form.get("email") or "").strip() or None
        image_file = request.files.get("image")

        if image_file and image_file.filename:
            if image_file.mimetype not in ALLOWED_IMAGE_TYPES:
                return jsonify({"error": "Unsupported image type. Use JPEG, PNG, or WEBP."}), 400
            image_bytes = image_file.read()
            if len(image_bytes) > MAX_IMAGE_BYTES:
                return jsonify({"error": "Image too large (max 8MB)."}), 400
            try:
                image_description = describe_image(image_bytes, image_file.mimetype)
            except Exception as e:
                return jsonify({"error": f"Failed to analyze image: {str(e)}"}), 502
    else:
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()
        student_email = (data.get("email") or "").strip() or None

    # Validate email format up front - a typo here means the student silently
    # never gets notified, so we catch it before the agent even runs.
    if student_email and not is_valid_email(student_email):
        return jsonify({"error": "That email address doesn't look valid. Please check it and try again."}), 400

    if image_description:
        combined_text = f"{text}\n\n[Photo analysis]: {image_description}".strip()
    else:
        combined_text = text

    if not combined_text:
        return jsonify({"error": "text or image is required"}), 400

    result = run_agent(combined_text, student_email=student_email)
    result["image_analysis"] = image_description
    return jsonify(result), 201

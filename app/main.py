"""
Main Flask application for CSV Text Converter Tool
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
from .text_parser import TextParser
from .delimiter_detector import DelimiterDetector
from .ghl_converter import GHLConverter
from .json_parser import JSONContentParser
from .enhanced_json_parser import EnhancedJSONContentParser
from .ghl_api_client import GHLAPIClient
from .ghl_integration import GHLIntegrationHandler

app = Flask(__name__, template_folder="../templates")

# Initialize components
text_parser = TextParser()
delimiter_detector = DelimiterDetector()
ghl_converter = GHLConverter()
json_parser = JSONContentParser()


@app.route("/")
def index():
    """Main page"""
    return render_template("index.html")


@app.route("/ghl")
def ghl_template():
    """GoHighLevel template page"""
    return render_template("ghl_template.html")


@app.route("/json")
def json_template():
    """JSON input template page"""
    return render_template("json_template.html")


@app.route("/api/parse", methods=["POST"])
def parse_text():
    """API endpoint to parse text and convert to CSV"""
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"success": False, "error": "No text provided"}), 400

        text = data["text"]
        delimiter = data.get("delimiter")  # Optional custom delimiter

        # Parse the text
        result = text_parser.parse_text_to_csv_data(text, delimiter)

        if result["success"]:
            # Validate the data
            validation = text_parser.validate_data(result["headers"], result["data"])
            result["validation"] = validation

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route("/api/detect-delimiter", methods=["POST"])
def detect_delimiter():
    """API endpoint to detect delimiter in text"""
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"success": False, "error": "No text provided"}), 400

        text = data["text"]
        delimiter, confidence, all_scores = delimiter_detector.detect_delimiter(text)

        return jsonify(
            {
                "success": True,
                "delimiter": delimiter,
                "confidence": confidence,
                "all_scores": all_scores,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route("/api/download-csv", methods=["POST"])
def download_csv():
    """API endpoint to download CSV file"""
    try:
        data = request.get_json()

        if not data or "headers" not in data or "data" not in data:
            return jsonify({"success": False, "error": "Missing headers or data"}), 400

        headers = data["headers"]
        csv_data = data["data"]
        delimiter = data.get("delimiter", ",")
        filename = data.get("filename", "converted_data.csv")

        # Generate CSV content with UTF-8 BOM
        platform_headers = data.get("platform_headers")
        csv_content = text_parser.generate_csv_content(
            headers, csv_data, delimiter, platform_headers
        )

        # Create temporary file with UTF-8 encoding
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as temp_file:
            temp_file.write(csv_content)
            temp_file_path = temp_file.name

        return send_file(
            temp_file_path,
            as_attachment=True,
            download_name=filename,
            mimetype="text/csv",
        )

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route("/api/convert-to-ghl", methods=["POST"])
def convert_to_ghl():
    """API endpoint to convert simple format to GoHighLevel format"""
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"success": False, "error": "No text provided"}), 400

        text = data["text"]
        delimiter = data.get("delimiter", "|")  # Default to pipe delimiter

        # First parse the simple format
        parse_result = text_parser.parse_text_to_csv_data(text, delimiter)

        if not parse_result["success"]:
            return jsonify(parse_result), 400

        # Convert to GoHighLevel format
        conversion_result = ghl_converter.convert_simple_to_ghl(
            [parse_result["headers"]] + parse_result["data"]
        )

        if conversion_result["success"]:
            # Validate the converted data
            validation = text_parser.validate_data(
                conversion_result["headers"], conversion_result["data"]
            )
            conversion_result["validation"] = validation

        return jsonify(conversion_result)

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route("/api/parse-json", methods=["POST"])
def parse_json():
    """API endpoint to parse JSON content with AI enhancement"""
    try:
        data = request.get_json()

        if not data or "json_content" not in data:
            return jsonify({"success": False, "error": "No JSON content provided"}), 400

        json_content = data["json_content"]
        gemini_api_key = data.get("gemini_api_key", "")
        enable_ai = data.get("enable_ai", False)
        platform = data.get("platform", "LinkedIn")

        # Initialize enhanced parser
        if gemini_api_key and enable_ai:
            enhanced_parser = EnhancedJSONContentParser(gemini_api_key)
        else:
            enhanced_parser = EnhancedJSONContentParser()

        # Parse JSON content with AI enhancement
        parse_result = enhanced_parser.parse_json_content(
            json_content, enable_ai, platform
        )

        if not parse_result["success"]:
            return jsonify(parse_result), 400

        posts = parse_result["posts"]

        # Convert to GoHighLevel CSV format
        csv_content = enhanced_parser.convert_to_ghl_csv(posts)

        # Parse CSV content to get headers and data
        import csv
        import io

        csv_reader = csv.reader(io.StringIO(csv_content))
        rows = list(csv_reader)

        if len(rows) < 2:
            return (
                jsonify({"success": False, "error": "Invalid CSV format generated"}),
                400,
            )

        platform_headers = rows[0]
        field_headers = rows[1]
        data_rows = rows[2:]

        return jsonify(
            {
                "success": True,
                "posts": posts,
                "total_posts": len(posts),
                "headers": field_headers,
                "data": data_rows,
                "platform_headers": platform_headers,
                "csv_content": csv_content,
                "ai_enhanced": parse_result.get("ai_enhanced", False),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route("/ghl-integration")
def ghl_integration_page():
    """GoHighLevel integration page"""
    return render_template("ghl_integration.html")


@app.route("/api/ghl/test-connection", methods=["POST"])
def test_ghl_connection():
    """Test GoHighLevel API connection"""
    try:
        data = request.get_json()

        if not data or "api_key" not in data or "location_id" not in data:
            return (
                jsonify(
                    {"success": False, "error": "API key and location ID are required"}
                ),
                400,
            )

        api_key = data["api_key"]
        location_id = data["location_id"]
        is_upbiz360 = data.get("is_upbiz360", False)

        # Test connection
        ghl_client = GHLAPIClient(api_key, location_id, is_upbiz360)
        result = ghl_client.test_connection()

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route("/api/ghl/create-posts", methods=["POST"])
def create_ghl_posts():
    """Create social media posts in GoHighLevel"""
    try:
        data = request.get_json()

        if (
            not data
            or "api_key" not in data
            or "location_id" not in data
            or "csv_data" not in data
        ):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "API key, location ID, and CSV data are required",
                    }
                ),
                400,
            )

        api_key = data["api_key"]
        location_id = data["location_id"]
        csv_data = data["csv_data"]
        platform = data.get("platform", "LinkedIn")
        is_upbiz360 = data.get("is_upbiz360", False)

        # Initialize GHL integration handler
        ghl_handler = GHLIntegrationHandler(api_key, location_id, is_upbiz360)

        # Create posts in GHL
        result = ghl_handler.create_posts_in_ghl(csv_data, platform)

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route("/api/ghl/get-posts", methods=["POST"])
def get_ghl_posts():
    """Get existing social media posts from GoHighLevel"""
    try:
        data = request.get_json()

        if not data or "api_key" not in data or "location_id" not in data:
            return (
                jsonify(
                    {"success": False, "error": "API key and location ID are required"}
                ),
                400,
            )

        api_key = data["api_key"]
        location_id = data["location_id"]
        limit = data.get("limit", 50)
        is_upbiz360 = data.get("is_upbiz360", False)

        # Initialize GHL integration handler
        ghl_handler = GHLIntegrationHandler(api_key, location_id, is_upbiz360)

        # Get posts from GHL
        result = ghl_handler.get_existing_posts(limit)

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route("/api/ghl/delete-post", methods=["POST"])
def delete_ghl_post():
    """Delete a social media post from GoHighLevel"""
    try:
        data = request.get_json()

        if (
            not data
            or "api_key" not in data
            or "location_id" not in data
            or "post_id" not in data
        ):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "API key, location ID, and post ID are required",
                    }
                ),
                400,
            )

        api_key = data["api_key"]
        location_id = data["location_id"]
        post_id = data["post_id"]
        is_upbiz360 = data.get("is_upbiz360", False)

        # Initialize GHL integration handler
        ghl_handler = GHLIntegrationHandler(api_key, location_id, is_upbiz360)

        # Delete post from GHL
        result = ghl_handler.delete_post(post_id)

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

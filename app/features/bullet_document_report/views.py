import os
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.features.bullet_document_report.services import BulletDocumentReportAnalysisService

bullet_document_report_bp = Blueprint('bullet_document_report', __name__, 
                          url_prefix='/bullet-document-report',
                          template_folder='template',
                          static_folder='template')  # Serve static files from template directory

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bullet_document_report_bp.route('/')
def index():
    return render_template('index.html')

@bullet_document_report_bp.route('/upload', methods=['POST'])
async def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Make sure the upload folder exists
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Create a fresh service instance for each request
        service = BulletDocumentReportAnalysisService()
        
        try:
            document = await service.process_report(file_path)
            
            # Only remove the file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)  # Clean up the uploaded file
            
            return jsonify({
                'filename': document.filename,
                'summary': document.defect_list
            })
        except Exception as e:
            # Log the error for debugging
            print(f"Error processing PDF: {str(e)}")
            
            # Try to clean up the file even if processing failed
            if os.path.exists(file_path):
                os.remove(file_path)
                
            return jsonify({'error': f"Failed to process PDF: {str(e)}"}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from OpenSSL import crypto
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure AWS credentials
aws_access_key = 'YOUR_AWS_ACCESS_KEY'
aws_secret_key = 'YOUR_AWS_SECRET_KEY'
s3_bucket_name = 'YOUR_S3_BUCKET_NAME'

# API endpoint to handle CSR creation and private key upload
@app.route('/create_csr', methods=['POST'])
def create_csr():
    # Get CSR details from request payload
    csr_details = request.json

    # Extract CSR details
    country = csr_details['country']
    state = csr_details['state']
    locality = csr_details['locality']
    organizational_unit = csr_details['organizational_unit']
    common_names = csr_details['common_names']
    organization = csr_details['organization']
    # ... other CSR details

    # Generate private key and CSR
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    req = crypto.X509Req()
    subj = req.get_subject()
    subj.C = country
    subj.ST = state
    subj.L = locality
    subj.organizationName = organization
    subj.OU = organizational_unit
    subj.CN = common_names[0]  # Assuming the first common name is used for CN

    # ... set other CSR details

    san_list = [f'DNS:{cn}' for cn in common_names]
    san_bytes = ", ".join(san_list).encode('utf-8')
    san_extension = crypto.X509Extension(b'subjectAltName', False, san_bytes)

    req.add_extensions([san_extension])
       

    # req.add_extensions([san_extension])

    req.set_pubkey(key)
    req.sign(key, 'sha256')

    # Save private key to a temporary file
    private_key_path = 'tmp/private_key.pem'
    with open(private_key_path, 'w') as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode('utf-8'))

    # Upload private key to S3 bucket
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    s3.upload_file(private_key_path, s3_bucket_name, 'private_keys/private_key.pem')

    # Remove the temporary private key file
    os.remove(private_key_path)

    # Extract CSR details for response
    public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, key).decode('utf-8')
    csr = crypto.dump_certificate_request(crypto.FILETYPE_PEM, req).decode('utf-8')

    # Return the generated CSR as the response
    response = {
        'public_key': public_key,
        'csr': csr
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run()

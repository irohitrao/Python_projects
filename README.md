# CSR Creation Flask App

This Flask application allows you to generate a Certificate Signing Request (CSR) with subject alternative names (SAN) and upload the private key to an Amazon S3 bucket.

## Features

- Input the domain names and other details to generate a CSR with SAN.
- Upload the private key to an Amazon S3 bucket.
- Display the generated CSR and public key.

## Prerequisites

Before running the application, ensure that you have the following:

- Python 3.x installed on your system.
- Flask and the required dependencies installed. You can install them using `pip install -r requirements.txt`.
- AWS access key and secret key with permissions to access the desired S3 bucket.

## Setup

1. Clone this repository or download the files.

2. Install the required dependencies:
pip install -r requirements.txt

3. Configure AWS credentials:

- Open the `CSRgenapp.py` file.
- Replace `'YOUR_AWS_ACCESS_KEY'` and `'YOUR_AWS_SECRET_KEY'` with your AWS access key and secret key, respectively.
- Replace `'YOUR_S3_BUCKET_NAME'` with the name of your S3 bucket.

4. Run the application:
python CSRgenapp.py

5. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Fill in the domain names (comma-separated), organization, and other CSR details in the input fields.

2. Click on the "Generate CSR" button.

3. The generated CSR and public key will be displayed on the page.

## License

This project is licensed under the [MIT License](LICENSE).



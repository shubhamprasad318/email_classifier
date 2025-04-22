\# **Support Email Classification System**

This repository contains a full implementation of an email classification system for a support team, including PII masking/demasking and category prediction.

\#\# Setup

**1\. \*\*Clone the repo\*\***    
    git clone https://github.com/shubhamprasad318/email\_classifier  
   cd email\_classifier

**Install dependencies**  
pip install \-r requirements.txt

**Train the mode**l  
python train.py data/combined\_emails\_with\_natural\_pii.csv

**Run the API**  
uvicorn api:app \--reload

**API Usage**  
Endpoint: POST /classify-email

Request Body (JSON): json

{  
  "email\_body": "Hi, I am Jane Doe. My email is jane@example.com. I have a billing issue."  
}  
Response (JSON): json

{  
  "input\_email\_body": "Hi, I am Jane Doe. My email is jane@example.com. I have a billing issue.",  
  "list\_of\_masked\_entities": \[  
    {  
      "position": \[9, 18\],  
      "classification": "full\_name",  
      "entity": "Jane Doe"  
    },  
    {  
      "position": \[31, 47\],  
      "classification": "email",  
      "entity": "jane@example.com"  
    }  
  \],  
  "masked\_email": "Hi, I am \[full\_name\]. My email is \[email\]. I have a billing issue.",  
  "category\_of\_the\_email": "Billing Issues"  
}

**Folder Structure**

email\_classifier/  
├── app.py  
├── api.py  
├── models.py  
├── utils.py  
├── train.py  
├── requirements.txt  
├── README.md  
├── data/  
 │   └── combined\_emails\_with\_natural\_pii.csv  
└──  models/        \# Saved vectorizer and classifier artifacts

  
import asyncio
import threading
from flask import Flask, request, jsonify
from verify_email import verify_email

app = Flask(__name__)

async def verify_email_async(email):
    return await verify_email(email)

def verify_email_sync(email):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if not asyncio.get_event_loop().is_running():
        loop.run_until_complete(asyncio.sleep(0))
    # result = loop.run_until_complete(verify_email_async(email))
    result = (verify_email_async(email))
    loop.close()
    return result

@app.route('/verify_email/<email>', methods=['GET'])
def verify_email_route(email):
    
    verification_result = verify_email_sync(email)
    result = asyncio.run(verification_result)  # Await the result
    return jsonify({'email': email, 'verified': result})


if __name__ == '__main__':
    app.run(debug=True,port=9876)

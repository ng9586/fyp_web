import requests

def test_read_root():
    """ 
    Test the root endpoint.
    """
    response = requests.get("http://127.0.0.1:8000/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_filename_audio():
    """
    Test the filename endpoint.
    """
    test_url = "https://youtu.be/jNQXAC9IVRw?si=SdiDOQHjADpoAftR"
    response = requests.post("http://127.0.0.1:8000/filename/", json={"url": test_url})
    assert response.status_code == 200

def test_transcribe_audio_endpoint():
    """
    Test the transcribe endpoint.
    """
    test_url = "https://youtu.be/jNQXAC9IVRw?si=SdiDOQHjADpoAftR"
    response = requests.post("http://127.0.0.1:8000/transcribe/", json={"url": test_url})
    assert response.status_code == 200
    assert "transcription" in response.json()

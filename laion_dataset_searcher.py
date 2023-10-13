from clip_retrieval.clip_client import ClipClient, Modality
import requests
import os


def get_extension_from_response(response):
    content_type = response.headers.get('Content-Type')
    
    if not content_type:
        return None
    
    
    if 'image/jpeg' in content_type:
        return '.jpg'
    elif 'image/png' in content_type:
        return '.png'
    else:
        return None
    
search = "one puppy" # what to search?


client = ClipClient(url="https://knn.laion.ai/knn-service", indice_name="laion5B-H-14", num_images=5000)
results = client.query(text=search)


os.makedirs(search, exist_ok=True)

start_index = 1000


for idx, result in enumerate(results[start_index:], start=start_index + 1):  # idx starts from 1 for better clarity
   
    
    image_url = result['url']
    
    try:
        # 이미지 URL에서 이미지 내용을 가져옵니다.
        response = requests.get(image_url, timeout=15)
        
        # URL에서 파일 확장자 추출
    
        ext = get_extension_from_response(response)


        # 확장자가 .jpg, .jpeg 또는 .png가 아니면 스킵
        if ext is None or ext not in ['.jpg', '.png']:
            print(f"Skipping URL {image_url} due to unsupported file extension {ext}.")
            continue
        
        # 지정된 폴더에 저장할 파일 이름 설정
        filename = os.path.join(search, f"{search}_{idx}{ext}")

        # 이미지 내용을 로컬 파일에 저장
        with open(filename, 'wb') as file:
            file.write(response.content)

    except requests.RequestException as e:
        print(f"Error occurred for URL {image_url}: {str(e)}. Skipping.")


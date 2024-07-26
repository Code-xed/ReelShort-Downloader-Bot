#pylint:disable=W3101
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://v-mps.crazymaplestudios.com/"
# Function to download a single .ts segment
def download_segment(segment_url, output_file):
    print(f"Starting download: {segment_url}")
    try:
        response = requests.get(segment_url, stream=True)
        if response.status_code == 200:
            with open(output_file, 'ab') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Successfully downloaded {segment_url} to {output_file}")
        else:
            print(f"Failed to download {segment_url} with status code {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while downloading {segment_url}: {e}")

# Function to download and concatenate video segments
def downloadVideo(chapter, output_file):
    part = 1
    while True:
        segment_url = f"{BASE_URL}{chapter}/h265-ordinary-ld-{part:05d}.ts"
        print(f"Checking {segment_url}")
        response = requests.head(segment_url)  # Use HEAD request to check if segment exists
        if response.status_code == 200:
            download_segment(segment_url, output_file)
            part += 1
        else:
            print(f"No more segments for {chapter} (part {part})")
            return output_file

# Function to process episodes dynamically
def process_episodes(episodes, base_url):
    with ThreadPoolExecutor(max_workers=3) as executor:  # Use 3 concurrent workers
        futures = []
        for index, episode in enumerate(episodes):
            output_file = f"new_{index + 1}.ts"
            
            # Download and concatenate video segments
            future = executor.submit(downloadVideo, episode, output_file)
            futures.append(future)
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f"Finished processing: {result}")

def getEpisodeList(book_id):
	url = "https://v-api.stardustgod.com/api/video/book/getChapterList"
	headers = {
    "Host": "v-api.stardustgod.com",
    "uid": "161073425",
    "channelid": "AVG10003",
    "ts": "1721807259",
    "apiversion": "1.2.1",
    "session": "49446721c3f74fd70cf01804c094aa6f",
    "lang": "en",
    "devid": "20262bb94d17ef73",
    "clientver": "1.9.02",
    "sign": "9fd5820a848d753d5881d299c3d932ec0047466b05738b21ee3a34b1c29ddff4",
    "clienttraceid": "17218072594316743",
    "accept-encoding": "br,gzip",
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "okhttp/4.11.0"
	}
	data = f"book_id={book_id}"#668c275431237d44a301fc09 #6651191b7812e57a1e0ddb5c"
	res = requests.post(url, headers=headers, data=data)
	r = res.json()
	print(r)
	chapters = r.get("data", {}).get("chapter_lists", [])
	episodes = [chapter.get("video_id") for chapter in chapters]
	return episodes
#process_episodes(episodes, base_url)
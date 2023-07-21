import requests
import json 
import pandas as pd
import argparse



# url을 가져오되 광역지자체 대상인지, 지역지자체 대상인지 지정 필요
def get_url(target, numOfRows, startYmd, endYmd):
    if target == 'metco':
        api_name = "metcoRegnVisitrDDList"
    elif target == 'locgo':
        api_name = "locgoRegnVisitrDDList"  
    end_point = "https://apis.data.go.kr/B551011/DataLabService"
    pageNo = 1
    MobileOS = "ETC"
    MobileApp = "AppTest"
    service_key = "I%2BxJPDnE7MUOEc7%2Fz6XlywW7hcFOSfkHW6mk8wzlVr6w7sdiRYmOrp4XZrOsZ2vnt5AB%2BVgGLLVu%2BuXN8ojeZQ%3D%3D"
    d_type = 'json'
    url = f"{end_point}/{api_name}?numOfRows={numOfRows}&pageNo={pageNo}&MobileOS={MobileOS}&MobileApp={MobileApp}&serviceKey={service_key}&_type={d_type}&startYmd={startYmd}&endYmd={endYmd}"
    return url

def total_row(url):
    response = requests.get(url)
    json_text = response.text
    js = json.loads(json_text)
    return js['response']['body']['totalCount']


def get_json(numRow, startYmd, endYmd):
    url = request_url(numOfRows=numRow,startYmd=startYmd, endYmd=endYmd)
    response = requests.get(url)
    json_text = response.text
    json_result = json.loads(json_text)
    total_row = json_result['response']['body']['totalCount']
    print(f'총 열 갯수: {total_row}')
    print(f'지정된 열 갯수: {numRow}')
    return json_result

js = get_json(numRow=target_row,startYmd=start_date,endYmd=end_date)



def main():
    p = argparse.ArgumentParser()
    p.add_argument('--startDate', '-s', type=int, required=True)
    p.add_argument('--endDate', '-e', type=int, required=True)
    args = p.parse_args()
    
    start_date = args.startDate
    end_date = args.endDate

    metco_url = get_url('metgo',1,start_date,end_date)
    locgo_url = get_url('locgo',1,start_date,end_date)

    metco_total = total_row(metco_url)
    locgo_total = total_row(locgo_url)
    
    request_url()

    pass

if __name__ == "__main__": main()
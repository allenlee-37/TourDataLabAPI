import argparse
import requests
import json 
import pandas as pd
from tqdm import tqdm



def request_url(numOfRows=100, 
                pageNo=1, 
                MobileOS="ETC", 
                MobileApp="AppTest", 
                startYmd=20220101, 
                endYmd=20221231):
    end_point = "https://apis.data.go.kr/B551011/DataLabService"
    api_name = "locgoRegnVisitrDDList"
    service_key = "I%2BxJPDnE7MUOEc7%2Fz6XlywW7hcFOSfkHW6mk8wzlVr6w7sdiRYmOrp4XZrOsZ2vnt5AB%2BVgGLLVu%2BuXN8ojeZQ%3D%3D"
    d_type = "json"
    url = f"{end_point}/{api_name}?numOfRows={numOfRows}&pageNo={pageNo}&MobileOS={MobileOS}&MobileApp={MobileApp}&serviceKey={service_key}&_type={d_type}&startYmd={startYmd}&endYmd={endYmd}"
    
    return url

def get_total_row(startYmd, endYmd):
    url = request_url(numOfRows=1, pageNo= 1, startYmd=startYmd, endYmd=endYmd)
    response = requests.get(url)
    json_text = response.text
    json_result = json.loads(json_text)
    total_row = json_result['response']['body']['totalCount']
    print(f'전체 row 수: {total_row}')
    return total_row

def get_json(startYmd, endYmd, total_row):
    def page_reader(page):
        url = request_url(numOfRows=1000, pageNo=page, startYmd=startYmd, endYmd=endYmd)
        json_text = requests.get(url).text
        json_result = json.loads(json_text)
        pre_df = json_result['response']['body']['items']['item']
        df = pd.json_normalize(pre_df)
        df = df.sort_values(by=['signguCode', 'baseYmd', 'touDivCd'], ascending=True)
        df = df.reset_index(drop=True)
        df = df[['signguCode', 'touDivCd', 'touNum', 'baseYmd']]
        
        # df = df[df['signguCode']=='47190']
        return df
    
    result = page_reader(0)
    for page in tqdm(range(1, int(total_row)//1000)):
        df = page_reader(page)
        result = pd.concat([result, df])
        if page%10==0:
            result.to_excel(f'result/{startYmd}-{endYmd}-{page} - 기초 지자체 지역방문자수 집계 데이터 정보 조회.xlsx')
            print(f'저장 완료 - {startYmd}-{endYmd}-{page} - 기초 지자체 지역방문자수 집계 데이터 정보 조회')
    result.to_excel(f'result/{startYmd}-{endYmd}-{page} - 기초 지자체 지역방문자수 집계 데이터 정보 조회.xlsx')
    return result

def main():
    parser = argparse.ArgumentParser(
        prog = '한국관광공사 API',
        description = '한국관광공사 방문자 수 API 호출'
    )
    parser.add_argument('-s', '--startdate', type=int, help='시작하는 날짜')
    parser.add_argument('-e', '--enddate', type=int, help='끝나는 날짜')

    args = parser.parse_args()

    print(args.startdate)
    print(args.enddate)
    
    start_date = args.startdate
    end_date = args.enddate

    total_row = get_total_row(start_date, end_date)
    result = get_json(start_date, end_date, total_row)

if __name__ == "__main__": main()
   
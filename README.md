# presidential-2020
綠盟 2020 總統杯專案 - 農地工廠誰先拆？高污染工廠找給你 

## 地址轉換經緯度
### Usage

1. 參考[Geocoding - 批量處理地址轉換經緯度](https://medium.com/%E8%8A%B1%E5%93%A5%E7%9A%84%E5%A5%87%E5%B9%BB%E6%97%85%E7%A8%8B/geocoding-%E6%89%B9%E9%87%8F%E8%99%95%E7%90%86%E5%9C%B0%E5%9D%80%E8%BD%89%E6%8F%9B%E7%B6%93%E7%B7%AF%E5%BA%A6-721ab2564c88) 安裝selenium, beautifulsoup4, chromedriver

2. 將需要轉換的地址建立成一個檔案，一行為一個地址

3. ```
   python addr2latlng.py [the_address_file]
   ```
   遇到錯誤會retry 3次，最後會產生 `[the_address_file]\_latlng.csv` 的檔案


## 經緯度疊農委會疑似工廠地圖
### Usage

1. 將 geojson_mapping.py 裡的 GEOJSON_FILE(農委會的geojson檔), INPUT_ADDR_LATLNG(地址轉換經緯度的輸出檔案), OUTPUT_FILE(結果輸出檔名) 變數換成要處理的檔案名稱

2. ``` 
   python geojson_mapping.py
   ```
   結果只會留下有疊到的點，格式為原本的輸出加上一欄對應到的農委會地圖裡的id

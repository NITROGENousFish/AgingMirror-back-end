from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re
import os
import json
def get_xunqinweb(upload_image_path_relative):
    # upload_image_path = r'C:\Users\FISH\Desktop\测试人脸上传\bad.png'
    upload_image_path = os.path.abspath(upload_image_path_relative)
    driver = webdriver.Firefox()
    driver.get('http://xunqin.mca.gov.cn/xunqinweb/show/news.html')
    #上传图片
    upload = driver.find_element_by_id('zx_img')
    upload.send_keys(upload_image_path)
    #点击查询
    find_people = driver.find_element_by_id("start_face")
    ActionChains(driver).click(find_people).perform()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'dd2'))
    )
    ### 如果没有返回值
    if ('很遗憾未找到匹配度较高的照片' in driver.page_source):
        driver.quit()
        return "not find"
    core_people_content = driver.find_element_by_class_name('dd2')
    people_list = core_people_content.find_elements_by_tag_name('li')
    outlist = []
    for content in people_list:
        pic_href = content.find_element_by_tag_name('img').get_attribute("src")
        info = content.find_element_by_class_name('rg').text
        info_out_1 = re.split('\n| \||\|',info)
        info_dict= {
            'url':pic_href,
            'name':info_out_1[0],
            'gender':info_out_1[1],
            'age':info_out_1[2].replace(" ","").replace("岁",""),
            'height':info_out_1[3].replace(" ","").replace("cm",""),
            'region':info_out_1[5].replace("区域： ",""),
            'aid_department':info_out_1[6].replace("救助单位: ",""),
            'publish_date':info_out_1[7].replace("发布日期： ",""),
            'similarity':info_out_1[8].replace("匹配相似度： ","")
        }
        outlist.append(info_dict)
    driver.quit()
    return outlist

# if __name__ == "__main__":
#     print(get_xunqinweb('./bad.png'))
#     print(get_xunqinweb('./upload.jpg'))


# pic = "./upload.jpg"
# with open(pic, 'rb') as f:
#     image = f.read()
#     image_base64 = str(base64.b64encode(image), encoding='utf-8')
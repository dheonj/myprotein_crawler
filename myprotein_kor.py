from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import io
from selenium.webdriver.common.action_chains import ActionChains

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

##open chrome and myprotein site
path ="C:\\Users\\jeong\\Documents\\github\\chromedriver.exe"
driver=webdriver.Chrome(path)
driver.get("https://www.myprotein.co.kr/nutrition.list")


#get product categories
protein=""" //*[@id="mainContent"]/div[3]/div/div[1]/a/div/h3 """
food=""" //*[@id="mainContent"]/div[3]/div/div[2]/a/div/h3 """
vitamin=""" //*[@id="mainContent"]/div[3]/div/div[3]/a/div/h3 """
amino=""" //*[@id="mainContent"]/div[3]/div/div[4]/a/div/h3 """
prepostworkout=""" //*[@id="mainContent"]/div[3]/div/div[5]/a/div/h3 """

categories=[protein, food, vitamin, amino, prepostworkout]

#for (i:category)
#see products list on a new tab
for category_element in categories:
    category_element=categories[1]
    category=driver.find_element_by_xpath(category_element)


    ActionChains(driver).key_down(Keys.CONTROL).click(category).key_up(Keys.CONTROL).perform()
    driver.switch_to_window(driver.window_handles[1])
    #wait until page is loaded
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH , """ //*[@id="mainContent"]/div/div[1]/main/div[1]/div[1]/p """))
        )
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    #prints out number of products of certain category
    num_of_results= driver.find_element_by_xpath(""" //*[@id="mainContent"]/div/div[1]/main/div[1]/div[1]/p """)
    print(num_of_results.text)
    next=1
    while next==1:

        plist=driver.find_elements_by_class_name("athenaProductBlock_productName")

        #for product in plist[::10]:
        for product in plist:
            #print names of products
            print('PRODUCTNAME= ',product.text)
            ActionChains(driver).key_down(Keys.CONTROL).click(product).key_up(Keys.CONTROL).perform()
            driver.switch_to_window(driver.window_handles[2])
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH , """//*[@id="product-description-content-8"]/div/div"""))
                )
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            except:
                driver.close()
                driver.switch_to_window(driver.window_handles[1])
                continue
            #expand

            info = driver.find_element_by_xpath("""//*[@id="product-description-content-8"]/div/div""")
            # //*[@id="product-description-content-lg-8"]/div/div
            serving_info=info.find_elements_by_xpath(".//p")
            nutritional_info=info.find_elements_by_xpath(""".//table[not(ancestor::td)]""")

            if len(serving_info)==1:
                print("SERVINGINFO1= ",serving_info[0].get_attribute('textContent'))
            else:
                print("SERVINGINFO1= ",serving_info[0].get_attribute('textContent'))
                print("SERVINGINFO2= ",serving_info[1].get_attribute('textContent'))
            for table in nutritional_info:
                nut_info_text = table.find_elements_by_xpath(""".//td[not(child::table)]""")
                temp=[]
                for line in nut_info_text:
                    info=line.get_attribute('textContent').strip().split()
                    temp.append(info)
                    #print(line.get_attribute('textContent'))
                print("NUTINFO= ", temp)

            driver.close()
            driver.switch_to_window(driver.window_handles[1])

        pageblock= driver.find_element_by_xpath("""//*[@id="mainContent"]/div/div[1]/main/div[4]/nav""")
        tot_page=pageblock.get_attribute("data-total-pages")
        #print("total page list: "+tot_page)
        current_page_button=pageblock.find_element_by_xpath(""".//*[@aria-current="true"]""").get_attribute("aria-label")
        current_page=current_page_button[14:]
        #print("Current page num: "+current_page)

        if tot_page==current_page:
            #print("end of page list")
            next=0

            driver.close()
            driver.switch_to_window(driver.window_handles[0])
        else:
            next_xpath='''.//*[@data-page-number="'''+str(int(current_page)+1)+'''"]'''
            next_page_button=pageblock.find_element_by_xpath(next_xpath)
            #print(next_page_button.get_attribute("aria-label"))
            #print("next page")
            current_url = driver.current_url
            next_page_button.click()
            #wait after click
            WebDriverWait(driver, 5).until(EC.url_changes(driver.current_url))

    #pagenumblock=driver.find_element_by_xpath("""//*[@id="mainContent"]/div/div[1]/main/div[4]/nav""")
    #driver.find_element_by_xpath("""//*[@id="mainContent"]/div/div[1]/main/div[4]/nav/ul/li[3]/a""").click()

    break
    #driver.quit()
    #a=dir(info[0])

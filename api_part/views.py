from django.shortcuts import render
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from django.shortcuts import render
from . forms import inputsForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from . models import inputs 
from .serializers import inputsSerializers
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib import messages
from bs4 import BeautifulSoup

#from . import extract 
#url = 'https://www.airbnb.co.in/rooms/745433615303041244?check_in=2024-02-18&guests=1&adults=2&s=67&unique_share_id=9341c5d7-f9d3-4a84-8f3d-bbd95134dc07&source_impression_id=p3_1707973315_UF9r5X4xiW4DU4B7&check_out=2024-02-20'

class inputsView(viewsets.ModelViewSet):
    queryset = inputs.objects.all()
    serializer_class = inputsSerializers

#@api_view(["POST"])
def scrape_data(url):
    try:
        options = Options()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        #url = request.data
        driver.get(url)
        lst = []
        #property name
        driver.implicitly_wait(5)
        property_name_obj = driver.find_element(By.CLASS_NAME, '_1xxgv6l')
        property_name = property_name_obj.text
        if property_name == '':
            property_name = property_name_obj.get_attribute('innerHTML')
        lst.append(property_name)
        #print(property_name)

        #caters to how many people 
        catering_obj = driver.find_elements(By.XPATH, "//*[@class='l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr']") 
        catering = [] #max_ppl, bedrooms, beds, bathrooms
        for i in catering_obj:
            if i.text != '':
                catering.append(i.text)
            else:
                catering.append(i.get_attribute('innerHTML')) 
        lst.append(catering)
        #print(catering)
        #rating and num of reviews
        rating_review_obj = driver.find_elements(By.XPATH, "//*[@class='a8jt5op atm_3f_idpfg4 atm_7h_hxbz6r atm_7i_ysn8ba atm_e2_t94yts atm_ks_zryt35 atm_l8_idpfg4 atm_mk_stnw88 atm_vv_1q9ccgz atm_vy_t94yts dir dir-ltr']") 
        rating = ''
        review = ''
        for i in rating_review_obj:
            s = ''
            if i.text != '':
                s = i.text
            else:
                s = i.get_attribute('innerHTML')
            ss = s.split()
            #print(ss)
            if rating == '' and 'Rated' in ss:
                rating = s
                #print(rating)
            if review == '' and 'reviews' in ss:
                review = s
        lst.append(rating)
        lst.append(review)
        #print(rating)
        #print(review)

        #host name 
        host_name_obj = driver.find_element(By.XPATH, "//*[@class='t1pxe1a4 atm_c8_8ycq01 atm_g3_adnk3f atm_fr_rvubnj atm_cs_qo5vgd dir dir-ltr']")
        host_name = ''
        if host_name_obj.text != '':
            host_name = host_name_obj.text
        else:
            host_name = host_name_obj.get_attribute('innerHTML')
        lst.append(host_name)   

        #price
        price_obj = driver.find_element(By.CLASS_NAME, '_tyxjp1')
        price = ''
        if price_obj.text != '':
            price = price_obj.text
        else:
            price = price_obj.get_attribute('innerHTML')
        lst.append(price)
        #print(price)

        #description 
        a = driver.find_elements(By.XPATH, "//*[@class='lrl13de atm_kd_pg2kvz_1bqn0at dir dir-ltr']")
        desc = ''
        for i in a:
            desc += i.text
            if desc == '':
                for i in a:
                    desc += i.get_attribute('innerHTML')
        lst.append(desc)
        #print(desc)
        info_ab_house = ''
        
        return lst
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST) 

def cxcon(request):
    if request.method == 'POST':
        form = inputsForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link'] 
            print('LINK = ', link)
            ans = scrape_data(link)
            print('ANSWERRRRRRRRRR = ',ans)
            info_ab_house = ''
            for i in ans[1]:
                info_ab_house += i + ' '
            messages.success(request, 'Property Name : {}'.format(BeautifulSoup(ans[0], "lxml").text))
            messages.success(request, 'Info about the property : {}'.format(BeautifulSoup(info_ab_house, "lxml").text))
            messages.success(request, 'Rating : {}'.format(BeautifulSoup(ans[2], "lxml").text))
            messages.success(request, 'Reviews : {}'.format(BeautifulSoup(ans[3], "lxml").text))
            messages.success(request, 'Host Name : {}'.format(BeautifulSoup(ans[4], "lxml").text))
            messages.success(request, 'Price : {}'.format(BeautifulSoup(ans[5], "lxml").text))
            messages.success(request, 'Description : {}'.format(BeautifulSoup(ans[6], "lxml").text))
    form = inputsForm()

    return render(request, 'myform/cxform.html', {'form':form}) 
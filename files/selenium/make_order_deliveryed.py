from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, os
from time import sleep


class TestChangeShipmentStatus(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1280, 752)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_change_shipment_status(self):
        driver = self.driver
        driver.get('https://knight-stag.castlery.sg/spree/admin/orders')
        sleep(5)

        driver.find_element_by_id("spree_user_email").send_keys("alex.ac@qq.com")
        driver.find_element_by_id("spree_user_password").send_keys("7787782")
        driver.find_element_by_name("commit").click()
        sleep(3)

        driver.find_element_by_xpath("//*[@id='listing_orders']//tbody/tr[1]/td[10]/a").click()
        sleep(1)
        driver.find_element_by_xpath("//*[@value='ship']").click()
        sleep(1)
        driver.find_element_by_xpath("//input[@value='mark as delivered']").click()
        sleep(3)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()




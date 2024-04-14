import requests
from bs4 import BeautifulSoup
from helper_class import *
from proxy_interface import *


class MAIN():

    def __init__(self):
        self.helper = Helper()
        self.proxy = CWEBSHARE()
        self.proxy_filename = "proxy.json"

        self.proxy.get_proxy_list(self.proxy_filename)

        self.all_proxies = self.helper.read_json_file(self.proxy_filename)["proxies"]
        
        self.url = "https://www.medicalequipment-msl.com/htm/blood-analyzer/REAL-TIME-PCR-analyzer-MSLPCR20.html"
        self.category = []
        self.product_listing =[]
        self.all_details = []

        self.data = []

        if os.path.exists('Output.json'):
            with open('Output.json', 'r') as f:
                self.data += json.load(f)

        if isinstance(self.data, list) and all(isinstance(item, dict) for item in self.data):
            self.listing = [item['url'] for item in self.data]
            print(len(self.listing))
        else:
            print("Invalid JSON format. Expected a list of dictionaries.")
    

    def getProxy(self):
        proxy = random.choice(self.all_proxies)

        proxyHandler = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}'

        return {"https": proxyHandler, "http": proxyHandler}
    

    def run_multiThread(self,function,max_workers,args):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(function, args) 
    

    def get_category(self):
        response = requests.get(self.url)
        print(response.status_code)
        soup = BeautifulSoup(response.content, "lxml")
        self.category =["https://www.medicalequipment-msl.com"+li.find('a').get('href') for li in soup.find("div", {"id":"left_nav"}).find_all('li')]


    def scrap_listing(self, cate_url, target_length=100):
        product_response = requests.get(cate_url)

        if product_response.status_code == 200:
            product_soup = BeautifulSoup(product_response.content, "lxml")
            products = product_soup.find("div", {'class': 'row products'})
            try:
                product_links = ["https://www.medicalequipment-msl.com" + x.find('a').get('href') for x in products.find_all('div', {'class': 'col-lg-6 col-md-6 col-sm-12 col-xs-12 products_list wow flipInX'})]
                self.product_listing.extend(product_links)
            except:
                pass
        else:
            print(f"Failed to retrieve products from {cate_url}. Retrying...")
            self.scrap_listing(cate_url, target_length=target_length)
            return  # Return to avoid the rest of the function when the initial request fails

        i = 2
        while i < target_length:
            print(f"{cate_url}list_{i}.html")
            product_response = requests.get(f"{cate_url}list_{i}.html")

            if product_response.status_code == 200:
                product_soup = BeautifulSoup(product_response.content, "lxml")
                products = product_soup.find("div", {'class': 'row products'})

                if not products:
                    break

                product_links = ["https://www.medicalequipment-msl.com" + x.find('a').get('href') for x in products.find_all('div', {'class': 'col-lg-6 col-md-6 col-sm-12 col-xs-12 products_list wow flipInX'})]

                if not product_links:
                    break

                self.product_listing.extend(product_links)
                i += 1
                print(len(self.product_listing))
            else:
                print(f"Failed to retrieve products from {cate_url}list_{i}.html. Retrying...")
                break  # Exit the loop when a subsequent request fails


    def Scrap(self,link):
        if link not in self.listing:
            response_ = requests.get(link)
            soup_ = BeautifulSoup(response_.content, "lxml")
            result = soup_.find('div',{'id':'lib_product_detail ashttt'})
            pro_info = result.find('div', {'class':'pro_info'})

            obj = {}
            obj['url'] = link
            obj["product_name"] = self.helper.get_text_from_tag(pro_info.find('div', {'class':'items'})).replace('\xa0\xa0', '').replace('Product Name:','').strip()

            data = pro_info.find_all('div',{'class':'item'})
            obj['latest_price'] = self.helper.get_text_from_tag(data[0]).replace('Latest Price:','')
            obj['model_no'] = self.helper.get_text_from_tag(data[1]).replace('Model No.:\xa0\xa0','')
            obj['weight'] = self.helper.get_text_from_tag(data[2]).replace('Weight:\xa0\xa0','')
            obj['min_order_quantity'] = self.helper.get_text_from_tag(data[3]).replace('Minimum Order Quantity:\xa0\xa0','')
            obj['supply_ability'] = self.helper.get_text_from_tag(data[4]).replace('Supply Ability:\xa0\xa0','')
            obj['payment_terms'] = self.helper.get_text_from_tag(data[5]).replace('Payment Terms:\xa0\xa0','')
            obj['size_options'] = [x.text for x in data[6].find_all('option')]
            obj['Color'] = [x.text for x in data[7].find_all('option')]

            obj["image_urls"] = [img['src'] for img in result.find('div',{'class':'swiper-container'}).find_all('img')]

            obj["quick_details"] = result.find('div',{'class':'products_d'}).find('p').text.strip()
            obj["packaging_delivery"] = result.find_all('div',{'class':'products_d'})[1].find('table').find('td').text.strip()
            obj["specifications"] = result.find_all('div',{'class':'products_d'})[2].find(class_='desc_contents').text.strip()
            
            self.all_details.append(obj)
            print(len(self.all_details))
        else:
            print(f"Already scraped {link}")


    def main(self):
        
        self.get_category()
        print("Lenth of Category",len(self.category))
        
        self.run_multiThread(self.scrap_listing, 10, self.category)

        print("Product Link",len(list(set(self.product_listing))))
        self.helper.write_json_file(self.product_listing, "link.json")

        with open('link.json','r') as product:
            product_listing = json.load(product)

        self.run_multiThread(self.Scrap, 10, product_listing)
        print("len the of all details",len(self.all_details))
        
        self.helper.write_json_file(self.all_details, "Output.json")
        


if __name__ == "__main__":
    MAIN().main()
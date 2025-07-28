from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
AUTH = 'brd-customer-hl_82164ebd-zone-scraping_browser1:rzlph2yt0m7b'
# SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'


def scrape_website(website):
    print("Launching chome browser..")
    SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        
        driver.get(website)
        print('waiting captcha to solve..')


        solve_res=driver.execute('executeCdpCommand',{
            'cmd':'Captcha.waitForSolve',
            'params':{'detectTimeout':10000},
        })
        print('Captcha solve status:',solve_res['value']['status'])
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)
        return html
# the below lines of code is for the extraction of only html but not the style of the website that is css
def extract_body_content(html_content):
    soup=BeautifulSoup(html_content,"html.parser")
    body_content=soup.body
    if(body_content):
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content


# the limit to take the charater in uml is 8000 so if the url is klarge we are going to split the data into the batches
# bzc of token limit
 #first move 0 to 6000 then in 2nd batch 6000 to next 6000....  until the end of the content
def split_dom_content(dom_content,max_length=6000):
    return [
        dom_content[i: i+max_length] for i in range(0,len(dom_content),max_length)
       
    ]

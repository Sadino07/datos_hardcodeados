

import scrapy
from urllib.parse import urljoin, urlparse
import re
import argparse


class ReconSpider(scrapy.Spider):
    name = "recon_spider"

    def __init__(self, *args, **kwargs):
        super(ReconSpider, self).__init__(*args, **kwargs)

        from urllib.parse import urlparse
    
        parsed = urlparse(self.start_url)
        domain_port = parsed.netloc.replace(":", "_")  
        self.output_file = f"{domain_port}.txt"
    
        with open(self.output_file, 'w') as f:
            f.write(f"=== Resultados del escaneo: {self.start_url} ===\n\n")

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        content_type = response.headers.get('Content-Type', b'').decode('utf-8')
        if not content_type.startswith(('text/', 'application/xhtml+xml', 'application/xml')):
            self.logger.debug(f"[SKIP] Contenido no textual: {content_type} - {response.url}")
            return

        self.save_result("🔗 URL visitadas", response.url)

        text_elements = response.xpath('//body//text()[not(parent::p or parent::h1 or parent::h2 or parent::h3 or parent::h4 or parent::h5 or parent::h6)]').getall()
        text = ' '.join(t.strip() for t in text_elements if t.strip())

        emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
        if emails:
            for email in set(emails):
                self.save_result("📧 Mails encontrados", email)

        true_comments = re.findall(r'<!--(.*?)-->', response.text, re.DOTALL)
        if true_comments:
            for comment in true_comments:
                clean_comment = comment.strip()
                self.save_result("💬 Comentarios encontrados", clean_comment)

                credentials_in_comment = re.search(
                    r'(?:user|username|login|password|pass|token|key)[=:]\s*([^\s"\'<>]+)', clean_comment, re.I
                )
                if credentials_in_comment:
                    self.save_result("🔐 Posibles credenciales en comentarios", credentials_in_comment.group(0))

                api_key_in_comment = re.search(r'\b[a-fA-F0-9]{32,}|\b[A-Za-z0-9+/=]{30,}', clean_comment)
                if api_key_in_comment:
                    self.save_result("🔑 Posibles API Keys / Tokens", api_key_in_comment.group(0))

        credentials_in_text = re.findall(
            r'(?:user|username|login|password|pass|token|key)[=:]\s*([^\s"\'<>]+)', text, re.I
        )
        if credentials_in_text:
            for cred in set(credentials_in_text):
                self.save_result("🔐 Posibles credenciales en texto plano", cred)

        api_keys = re.findall(r'\b[a-fA-F0-9]{32,}|\b[A-Za-z0-9+/=]{30,}', text)
        if api_keys:
            for key in set(api_keys):
                self.save_result("🔑 Posibles API Keys / Tokens", key.strip())

        file_patterns = [".txt", ".log", ".bak", ".xml", ".json", ".pdf", ".doc", ".docx", ".xls", ".xlsx"]
        for link in response.css('a::attr(href)').getall():
            full_url = urljoin(response.url, link)
            if any(pattern in full_url.lower() for pattern in file_patterns):
                self.save_result("📄 Archivos encontrados", full_url)

        parsed_start = urlparse(self.start_url)
        base_domain = parsed_start.netloc

        for raw_link in response.css('a::attr(href)').getall():
            link = urljoin(response.url, raw_link)
            parsed = urlparse(link)

            if parsed.scheme in ['http', 'https'] and parsed.netloc == base_domain:
                yield response.follow(link, self.parse)
            else:
                self.logger.debug(f"Ignorando enlace externo: {link}")

    def save_result(self, section, content):
        """Guarda los resultados en el archivo y los muestra por consola"""
        line = f"{section}\n - {content}\n"
        
        with open(self.output_file, 'a') as f:
            f.write(line)
        
        print(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Spider de reconocimiento con Scrapy')
    parser.add_argument('-u', '--url', required=True, help='URL del objetivo')
    args = parser.parse_args()

    ReconSpider.start_url = args.url

    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36',
        'LOG_LEVEL': 'ERROR'
    })

    process.crawl(ReconSpider)
    process.start()
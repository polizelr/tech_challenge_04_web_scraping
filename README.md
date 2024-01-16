# Web Scraping - site do IPEA

O aplicativo realiza o web scraping no site do Instituto de Pesquisa Econômica Aplicada - IPEA (http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view), extraindo os dados do preço do petróleo bruto Brent presentes em uma tabela HTML. Após a extração, os dados são transformados em um DataFrame e, em seguida, são armazenados na tabela "preco_petroleo_brent" no Google BigQuery. Este processo é automatizado e agendado para ser executado diariamente às 10h, garantindo a atualização regular das informações no banco de dados.

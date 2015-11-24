import scrapy
import time
import os
import csv
import thread
import sys

CURRENT_PATH = os.getcwd()
C_WRITED_FILES = 0
print CURRENT_PATH

def is_leap_year(year):
    if(year % 4 == 0 and year % 100 != 0 or year % 400 == 0):  
        return True
    else:  
        return False

def get_urls(dia_i, mes_i, anio_i, dia_f, mes_f, anio_f):

    if(mes_i > mes_f):
        return None
    if((dia_i > dia_f) and (mes_i==mes_f)):
        return None

    isOneYear = True

    #http://www.eluniverso.com/servicios/archivo/2015/02/04
    base = "http://www.eluniverso.com/servicios/archivo/"
    lista_urls = []

    print "Starting urls generator"

    for y in range (anio_i, anio_f+1):
        #print y
        lista_dias = []

        if(is_leap_year(y)):
            lista_dias = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:           #Ene,Feb,Mar,Abr,May,Jun,Jul,Ago,Sep,Oct,Nov,Dic
            lista_dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if(y<anio_f):
            for m in range (mes_i, 12+1):
                #print m 
                for d in range (1, lista_dias[m-1]+1):
                    #print d
                    lista_urls.append(base + str(y) +'/'+ str_dia(m)+'/'+str_dia(d))
        else:
            if(isOneYear):
                for m in range( mes_i, mes_f +1):
                    if(m<mes_f):
                        for d in range (1, lista_dias[m-1]+1):
                            lista_urls.append(base + str(y) +'/'+ str_dia(m)+'/'+str_dia(d))
                    else:
                        for d in range (1, dia_f+1):
                            lista_urls.append(base + str(y) +'/'+ str_dia(m)+'/'+str_dia(d))
            else:
                for m in range (1, mes_f+1):
                    if(m<mes_f):
                        for d in range (1, lista_dias[m-1]+1):
                            lista_urls.append(base + str(y) +'/'+ str_dia(m)+'/'+str_dia(d))
                    else:
                        for d in range (1, dia_f+1):
                            lista_urls.append(base + str(y) +'/'+ str_dia(m)+'/'+str_dia(d))
    return lista_urls        

def str_dia(mes):
    if(len(str(mes))==1):
        dia = '0' + str(mes)
    else:
        dia = str(mes)
    return dia

def urls_to_file(lista):
    f = open("urls.txt", "w+")
    for l in lista:
        f.write(l+'\n')
    f.close()
    exit()
#---------------------------------------------------------------------

class UniversoSpider(scrapy.Spider):

    url_base = "http://www.eluniverso.com"
    name = "universo"
    allowed_domains = ["eluniverso.com"]
    start_urls = get_urls(1,4,2014,31,12,2014)
    
    '''
    start_urls = [
        #"http://www.eluniverso.com/politica/",
        #"http://www.eluniverso.com/ecuador/",
        #"http://www.eluniverso.com/servicios/archivo/2015/10/04",
        "http://www.eluniverso.com/servicios/archivo/2010/11/19",
        "http://www.eluniverso.com/servicios/archivo/2010/11/20",
        "http://www.eluniverso.com/servicios/archivo/2010/11/21",
    ]
    '''
    
    
    #print start_urls
    
    def parse(self, response):
        try:
            #print response.url, '====================================='
            print '====================================='
            print response.url
            group = response.xpath('//div[@class="view-grouping-content view-grouping-content-0"]')
            #allspans = group[0].xpath('//span[@class="field-content"]');
            allspans = group[0].xpath('//div/div/span[@class="field-content"]');
            count = 0    
            c = 0
            for n in allspans:
                try: 
                    title = n.xpath('a/text()').extract()[0]
                    url = n.xpath('a/@href').extract()[0]
                    tim = (n.xpath('//span[@class="time"]'))[0].xpath('text()').extract()[0]

                    if '/noticias/' in url or '/1355/' in url or '/1356/' in url or '/1447/' in url or '/1422/' in url or '/1361/' in url or '/1360/' in url or '/1445/' in url or '/1446/' in url:
                        count+=1
                        #thread.start_new_thread( print_time, ("Thread-1", 2, ) )
                        #scrapy.http.Request(url[, callback, method='GET', headers, body, cookies, meta, encoding='utf-8', priority=0, dont_filter=False, errback]
                        #thread.start_new_thread( scrapy.Request, ((self.url_base + url)[self.parse_url_content,]) )
                        yield scrapy.Request(self.url_base + url, callback=self.parse_url_content)
                    c+=1
                except Exception as e:
                    print e
            print str(count) + ' noticias de ' + str(c) +' enlaces'
            #time.sleep(30)
            
        except Exception as e:
            print e
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def parse_url_content(self, response):
        try:
            #print 'Parse_2: ',response.url

            y = response.url.split("/")[-6] 
            m = response.url.split("/")[-5] 
            d = response.url.split("/")[-4]

            topics = response.xpath('//ul/li/a[@class="active-trail"]/text()')
            topic = topics[0].extract().encode('UTF-8')

            if(topic=='Seguridad'):
                return
            #f.write(topic[0].extract().encode('UTF-8'))

            ruta = CURRENT_PATH +'/data/'+y+'/'+m+'/'+d+'/'+topic
            if not os.path.exists(ruta):
                os.makedirs(ruta)

            filename = ruta +'/'+ response.url.split("/")[-1] + '.txt'

            if(os.path.isfile(filename)):
                print 'FILE ALREADY EXISTS: '+filename
                return

            #print filename
            f = open(filename, 'a+')
            #print "==================================================="

            title = response.xpath('//header/h1[@class="node-title"]/text()')
            #print title[0].extract(), len(title)
            f.write(title[0].extract().encode('UTF-8'))

            #print "=========="
            f.write("\n==========\n")

            #topic = response.xpath('//ul/li/a[@class="active-trail"]/text()')
            #print "Topico:",topic[0].extract(), len(topic)
            #f.write(topic[0].extract().encode('UTF-8'))
            #print (topic)
            f.write(topic)

            #print "==========" #10 iguales
            f.write("\n==========\n")

            content = response.xpath('//div[@property="schema:articleBody content:encoded"]')[0]
            
            tags = response.xpath('//div[@class="tags-lea-ademas"]/div/div/div/a/text()')
            for t in tags:
                #print t.extract()
                f.write(t.extract().encode('UTF-8')+';')

            #print "=========="
            f.write("\n==========\n")

            allps = content.xpath('//p')
            paragraphs = allps[:len(allps)-1]
            for p in paragraphs:
                try:
                    ps = p.xpath('text()').extract()
                    np = len(ps)
                    aa = p.xpath('a/text()').extract()
                    na = len(aa)

                    try:
                        bp = p.xpath('strong/text()').extract()
                        #print bp[0]
                        f.write(bp[0].encode('UTF-8'))
                    except Exception as e:
                        #print e
                        pass

                    #print np, na
                    if(na>0):
                        for i in range(0,np):
                            #print ps[i],
                            f.write(ps[i].encode('UTF-8'))
                            if(i<na):
                                #print aa[i],
                                f.write(aa[i].encode('UTF-8'))
                    else:
                        #print ps[0]
                        f.write(ps[0].encode('UTF-8'))
                    f.write('\n')
                except Exception as e:
                    pass
            f.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(exc_type, fname, exc_tb.tb_lineno)
            print 'ERROR:', e, '===', response.url, '===', 'line', exc_tb.tb_lineno

# 2011  188m52s
# 2012  153m15s
# 2013  132m23s

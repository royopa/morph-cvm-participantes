# -*- coding: utf-8 -*-
import os
import time

import lxml.html
os.environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'
import scraperwiki



for pk_partic in range(99999, 999999):
    print(pk_partic)
    url = 'http://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/DemContabeis/CPublicaDemContabeisFI.aspx?PK_PARTIC={}'
    pk_partic = str(pk_partic)

    try:
        html = scraperwiki.scrape(url.format(pk_partic))
    except Exception as e:
        time.sleep(15)
        try:
            html = scraperwiki.scrape(url.format(pk_partic))
        except Exception as e:
            time.sleep(15)
            try:
                html = scraperwiki.scrape(url.format(pk_partic))
            except Exception as e:
                continue

    # Find something on the page using css selectors
    root = lxml.html.fromstring(html)

    try:
        cnpj = root.get_element_by_id("lbNrPfPj").text.replace(
            '.', '').replace('-', '').replace('/', '')
    except Exception as e:
        continue

    data = {
        "pk_partic": pk_partic,
        "cnpj": cnpj
    }

    # Write out to the sqlite database using scraperwiki library
    scraperwiki.sqlite.save(unique_keys=['pk_partic'], data=data)

# rename file
os.rename('scraperwiki.sqlite', 'data.sqlite')

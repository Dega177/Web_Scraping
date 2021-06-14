PAGINATION = {
    'selector': '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
    'callback': 'parse'
}

VACANCY = {
    'selector': '//span[@data-qa="bloko-header-3"]//a[contains(@data-qa, "vacancy-title")]/@href',
    'callback': 'vacancy_parse'
}

VACANCY_DATA = {
    'title': '//h1[@data-qa="vacancy-title"]//text()',
    'salary': '//p[contains(@class, "vacancy-salary")]/span[@data-qa="bloko-header-2"]/text()',
    'description': '//div[@class="vacancy-description"]//div[@data-qa="vacancy-description"]//text()',
    'skills': '//div[@class="bloko-tag-list"]//div[contains(@data-qa, "skills-element")]//text()',
    'company_url': '//div[@data-qa="vacancy-company"]//a[@data-qa="vacancy-company-name"]/@href'

}

COMPANY_DATA = {
    'name': '//h1[@data-qa="bloko-header-1"]/span[@data-qa="company-header-title-name"]/text()',
    'company_site': '//div[@data-qa="sidebar-text-color"]/a[@data-qa="sidebar-company-site"]/@href',
    'areas_of_work': '//div[@class="employer-sidebar-block"]/p/text()',
    'description': '//div[@data-qa="company-description-text"]//text()'
}
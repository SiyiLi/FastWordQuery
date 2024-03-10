#-*- coding:utf-8 -*-
from ..base import *

DICT_PATH = u''

@register([u'柯林斯英汉双解定制版', u'Collins COBUILD EN_CN Customized'])
class Collins(MdxService):

    def __init__(self):
        dict_path = DICT_PATH
        # if DICT_PATH is a path, stop auto detect
        if not dict_path:
            from ...service import service_manager, service_pool
            for clazz in service_manager.mdx_services:
                service = service_pool.get(clazz.__unique__)
                title = service.title if service and service.support else u''
                service_pool.put(service)
                if title.startswith(u'Collins'):
                    dict_path = service.dict_path
                    break
        super(Collins, self).__init__(dict_path)

    @property
    def title(self):
        return getattr(self, '__register_label__', self.unique)

    def _get_from_api(self):
        html = self.get_default_html()
        # Uncomment below to debug collins issues
        # print(html)
        soup = parse_html(html)
        result = {
            'stars': '',
            'explanation': '',
        }

        try:
            # Make sure 'text' & 'header' are not referenced before assignment
            text = ''
            stars = soup.find('span', {'class':'C1_word_header_star'})
            if stars:
                text = u''.join(stars.text)
            result['stars'] = text

            header = ''
            header = soup.find('div', {'class':'C1_word_header'})

            if header:
                header.replace_with('')
            result['explanation'] = u''.join(str(soup))
        except Exception as e:
            print(e)

        return self.cache_this(result)

    @export([u'柯林斯星级', u'Collins stars'])
    def fld_stars(self):
        return self._get_field('stars')

    @export([u'柯林斯解释', u'Collins explanation'])
    def fld_explanation(self):
        return self._get_field('explanation')

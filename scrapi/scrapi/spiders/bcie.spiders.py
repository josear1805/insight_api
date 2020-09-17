import scrapy
from tenders.models import Tender
from profiles.models import Profile
from webs.models import Web
from search_settings.models import SearchSettings
import datetime


# Titulos = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/text()
# Empresa = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[not(contains(@class , "para"))]/text()
# Descripcion //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[@class="para"]/text()
# Lugar = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[0]/text()
# Fecha = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[1]/text()


class BcieSpiders(scrapy.Spider):
  name = 'bcie_spiders'
  start_urls = [
      'https://adquisiciones.bcie.org/avisos-de-adquisicion'
  ]
  custom_settings = {
      'FEED_URI': 'bcie_spiders.json',
      'FEED_FORMAT': 'json'
  }

  def parse(self, response):

    codes = response.xpath(
        '//table[@id="customtables"]//tbody/tr/td[1]/text()').getall()

    titles = response.xpath(
        '//table[@id="customtables"]//tbody/tr/td[2]/a/text()').getall()

    links_webs = response.xpath(
        '//table[@id="customtables"]//tbody/tr/td[2]/a/@href').getall()

    places = response.xpath(
        '//table[@id="customtables"]//tbody/tr/td[3]/text()').getall()

    dates1 = response.xpath(
        '//table[@id="customtables"]//tbody/tr/td[4]/text()').getall()

    dates2 = response.xpath(
        '//table[@id="customtables"]//tbody/tr/td[5]/text()').getall()
  
   
    get_webs = Web.objects.all().filter(
        url='https://adquisiciones.bcie.org/avisos-de-adquisicion')

    for item_get_webs in get_webs:
      get_search_settins = SearchSettings.objects.all().filter(
          country_id=item_get_webs.country_id)

      for item_search_settings in get_search_settins:
        profiles = Profile.objects.all().filter(
            id=item_search_settings.profile_id)

        for item_profile in profiles:
          for item in titles:
            words_searchs = item_profile.search_parameters.upper().strip().split(',')
            words_not_searchs = item_profile.discard_parameters.upper().strip().split(',')

            word_key_in = any([words_search in titles[titles.index(
                item)].upper() for words_search in words_searchs])

            if word_key_in:
              word_key_not_in = any([words_not_search in titles[titles.index(
                  item)].upper() for words_not_search in words_not_searchs])

              if word_key_not_in:
                print('*************--- NOT SAVE ---*************')
              else:
                print('*************--- SAVE ---*************')
                dates_save = f"{dates1[titles.index(item)].rstrip()} - {dates2[titles.index(item)].rstrip()}"
                link = f"https://adquisiciones.bcie.org/avisos-de-adquisicion/{links_webs[titles.index(item)]}"

                tenders_save = Tender(
                    country_id=item_get_webs.country_id, profile_id=item_profile.id, description=titles[titles.index(item)], code=codes[titles.index(item)], link=link, place_of_execution=places[titles.index(item)].rstrip(), dates=dates_save)
                tenders_save.save()
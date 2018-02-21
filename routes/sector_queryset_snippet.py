    def get_queryset(self):
        self.sector_dict = {}
        country_object_list = Sector.objects.values('country').order_by('country').distinct()
        country_list=[]
        for country in country_object_list:
            country = country['country']
            country_count = Sector.objects.filter(country = country).aggregate(Count('routes'))
            country_list.append({country:[country_count['routes__count']]})

            region_object_list = (Sector.objects
                                .filter(country=country)
                                .values('region')
                                .order_by('region')
                                .distinct()
                                )

            for region in region_object_list:
                region = region[region]
                sectors = Sector.objects.filter(region = region)
                region_count = sectors.aggregate(Count('routes'))
                self.sector_dict   [country].append = {region:[count['routes__count'], sectors]}
        print(self.sector_dict)

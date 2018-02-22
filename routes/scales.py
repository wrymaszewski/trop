def convert_scale(self, new_scale):
    SCALES =[
            ['5.2','1','I','I'],
            ['5.3','2','II','II'],
            ['5.4','2+','II+','II+'],
            ['5.5','3','III','III+'],
            ['5.6','4','IV','IV'],
            ['5.7','4+','V-','IV+'],
            ['5.7','5a','V-','V-'],
            ['5.8','5a','V','V'],
            ['5.9','5b','V+','V+'],
            ['5.10a','5b+','VI-','V+/ VI-'],
            ['5.10b','5c','VI-','VI-'],
            ['5.10c','6a','VI','VI'],
            ['5.10d','6a+','VI+','VI+'],
            ['5.11a','6b','VII-','VI.1'],
            ['5.11b','6b+','VII','VI.1+'],
            ['5.11c','6c','VII+','VI.2'],
            ['5.11d','6c+','VIII-','VI.2+'],
            ['5.12a','6c+','VIII-','VI.2+/VI.3'],
            ['5.12b','7a','VIII','VI.3'],
            ['5.12c','7a+','VIII+','VI.3+'],
            ['5.12d','7b','IX–','VI.4'],
            ['5.12d','7b+','IX–','VI.4'],
            ['5.13a','7c','IX','VI.4+'],
            ['5.13b','7c+','IX+','VI.5'],
            ['5.13c','8a','IX+','VI.5+'],
            ['5.13d','8a+','X-','VI.5+/ VI.6'],
            ['5.14a','8b','X','VI.6'],
            ['5.14b','8b+','X+','VI.6+'],
            ['5.14c','8c','X+','VI.7'],
            ['5.14d','8c+','XI-','VI.7+'],
            ['5.15a','9a','XI','VI.8']
    ]

    SCALES_BLD = [
                    ['VB','1'],
                    ['VB','2'],
                    ['VB','3'],
                    ['V0','4'],
                    ['V0+','4+'],
                    ['V1','5a'],
                    ['V2','5b'],
                    ['V2','5c'],
                    ['V2+','6a'],
                    ['V3','6a+'],
                    ['V4','6b'],
                    ['V4+','6b+'],
                    ['V5','6c'],
                    ['V6','6c+'],
                    ['V6+','7a'],
                    ['V7','7a+'],
                    ['V8','7b'],
                    ['V8+','7b+'],
                    ['V9','7c'],
                    ['V10','7c+'],
                    ['V11','8a'],
                    ['V12','8a+'],
                    ['V13','8b'],
                    ['V14','8b+'],
                    ['V15','8c'],
                    ['V16','8c+'],
                    ['V17''9a']
    ]

    SCALE_INDEXES = {
        'YDS': 0,
        'FR': 1,
        'UIAA': 2,
        'POL': 3
    }

    SCALE_INDEXES_BLD = {
        'V': 0,
        'FR': 1
    }

    if self.route_type == 'BLD':
        for row in SCALES_BLD:
            if row[SCALE_INDEXES_BLD[self.scale]]==self.grade:
                return row[SCALE_INDEXES_BLD[new_scale]]
    else:
        for row in SCALES:
            if row[SCALE_INDEXES[self.scale]] == self.grade:
                return row[SCALE_INDEXES[new_scale]]

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
                    ['V1','5'],
                    ['V2','5+'],
                    ['V2+','6A'],
                    ['V3','6A+'],
                    ['V4','6B'],
                    ['V4+','6B+'],
                    ['V5','6C'],
                    ['V6','6C+'],
                    ['V6+','7A'],
                    ['V7','7A+'],
                    ['V8','7B'],
                    ['V8+','7B+'],
                    ['V9','7C'],
                    ['V10','7C+'],
                    ['V11','8A'],
                    ['V12','8A+'],
                    ['V13','8B'],
                    ['V14','8B+'],
                    ['V15','8C'],
                    ['V16','8C+'],
                    ['V17''9A']
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

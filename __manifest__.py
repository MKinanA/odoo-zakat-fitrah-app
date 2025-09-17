{
    'name': 'Zakat Fitrah',
    'summary': 'Aplikasi Pendataan Zakat Fitrah (dan fidyah) untuk Panitia.',
    'description': 'Aplikasi pendataan zakat fitrah dan fidyah untuk panitia. Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/zf_views.xml',
    ],
    'application': True,
    'installable': True,
} # pyright: ignore[reportUnusedExpression] (ignore the `Expression value is unused` warning here)
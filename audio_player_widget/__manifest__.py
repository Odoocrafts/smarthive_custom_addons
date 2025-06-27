{
    'name': "Audio Player Widget",
    'author': 'Rizwaan',
    'version': "17.0.0.0",
    'sequence': "0",
    'depends': ['base','web'],
    'data': [
    ],
    "assets": {
        "web.assets_backend": [
            'audio_player_widget/static/src/views/fields/audio_player/audio_player.scss',
            'audio_player_widget/static/src/views/fields/audio_player/audio_player.xml',
            'audio_player_widget/static/src/views/fields/audio_player/audio_player.js',

        ],
    },
    'demo': [],
    'summary': "Audio Player Widget",
    'description': "Audio Player Widget",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
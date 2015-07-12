# -*- coding: utf8 -*-
from __future__ import unicode_literals

import json

from django.conf import settings
from django.utils.encoding import force_text

from leaflet import (
    app_settings, SPATIAL_EXTENT, SRID, PLUGIN_ALL,
    PLUGIN_FORMS)

from leaflet.templatetags.leaflet_tags import (
    _get_plugin_names, _get_all_resources_for_plugins)


from django_jinja import library


@library.global_function
@library.render_with("leaflet/css.jinja")
def leaflet_css(plugins=None):
    """

    :param only_plugins:
    :param exclude_plugins:
    :return:
    """
    plugin_names = _get_plugin_names(plugins)
    return {
        "PLUGINS_CSS": _get_all_resources_for_plugins(plugin_names, 'css'),
    }


@library.global_function
@library.render_with("leaflet/js.jinja")
def leaflet_js(plugins=None):
    """

    :param only_plugins:
    :param exclude_plugins:
    :return:
    """
    plugin_names = _get_plugin_names(plugins)
    with_forms = PLUGIN_FORMS in plugin_names or PLUGIN_ALL in plugin_names
    force_image_path = app_settings.get('FORCE_IMAGE_PATH')
    return {
        "DEBUG": settings.TEMPLATE_DEBUG,
        "SRID": str(SRID) if SRID else None,
        "PLUGINS_JS": _get_all_resources_for_plugins(plugin_names, 'js'),
        "with_forms": with_forms,
        "FORCE_IMAGE_PATH": force_image_path
    }


@library.global_function
@library.render_with("leaflet/_leaflet_map.jinja")
def leaflet_map(name, callback=None, fitextent=True, creatediv=True,
                loadevent='load'):
    """

    :param name:
    :param callback:
    :param fitextent:
    :param creatediv:
    :return:
    """
    extent = None
    if SPATIAL_EXTENT is not None:
        # Leaflet uses [lat, lng]
        xmin, ymin, xmax, ymax = SPATIAL_EXTENT
        extent = (ymin, xmin, ymax, xmax)

    djoptions = dict(
        srid=SRID,
        extent=[extent[:2], extent[2:4]],
        fitextent=fitextent,
        center=app_settings['DEFAULT_CENTER'],
        zoom=app_settings['DEFAULT_ZOOM'],
        minzoom=app_settings['MIN_ZOOM'],
        maxzoom=app_settings['MAX_ZOOM'],
        layers=[
            (force_text(label), url, attrs)
            for (label, url, attrs) in app_settings.get('TILES')],
        overlays=[
            (force_text(label), url, attrs)
            for (label, url, attrs) in app_settings.get('OVERLAYS')],
        attributionprefix=force_text(
            app_settings.get('ATTRIBUTION_PREFIX'), strings_only=True),
        scale=app_settings.get('SCALE'),
        minimap=app_settings.get('MINIMAP'),
        resetview=app_settings.get('RESET_VIEW'),
        tilesextent=list(app_settings.get('TILES_EXTENT', []))
    )

    return {
        # templatetag options
        'name': name,
        'loadevents': json.dumps(loadevent.split()),
        'creatediv': creatediv,
        'callback': callback,
        # initialization options
        'djoptions': json.dumps(djoptions),
        # settings
        'NO_GLOBALS': app_settings.get('NO_GLOBALS'),
    }


@library.global_function
def leaflet_json_config():
    settings_as_json = app_settings.copy()

    if SPATIAL_EXTENT is not None:
        xmin, ymin, xmax, ymax = settings_as_json.pop('SPATIAL_EXTENT')
        settings_as_json['SPATIAL_EXTENT'] = {'xmin': xmin, 'ymin': ymin,
                                              'xmax': xmax, 'ymax': ymax}

    return json.dumps(settings_as_json)

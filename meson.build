project('reinput',
          version: '0.1.0',
    meson_version: '>= 1.0.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')

subdir('data')
#subdir('src')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)

#pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
#moduledir = pkgdatadir / 'reinput'
gnome = import('gnome')

gnome.compile_resources('reinput',
  'reinput.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'reinput.in',
  output: 'reinput',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

reinput_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

#install_data(reinput_sources, install_dir: moduledir)
install_subdir('src', install_dir: pkgdatadir, exclude_directories: './src/test')
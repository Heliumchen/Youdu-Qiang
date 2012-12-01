from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('youdu.core.views',
	url(r'^$', 'home', name='home'),
	url(r'^submit/$', 'submit_poster'),
	url(r'^posters/(?P<poster_id>\d+)/$', 'show_poster'),
	url(r'^badlink/$', 'bad_link'),
	
    # url(r'^sanren/', include('sanren.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
	url(r'^login/renren/$', 'youdu.core.renren.renren_login'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
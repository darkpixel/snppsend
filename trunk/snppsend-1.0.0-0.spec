Summary: Send text messaged to an alphanumeric pager via the SNPP protocol
Name: snppsend
Version: 1.0.0
Release: 0
Copyright: GPL
Group: Applications/Communications
Source: http://darkpixel.com/snppsend/snppsend-1.0.0.tar.gz
BuildRoot: /var/tmp/%{name}-buildroot

%description
This program allows you to send a text message to an alphanumeric
pager using the SNPP protocol.  Almost every alphanumeric paging
provider supports the SNPP protocol.

%files
%config /receivers
%config /providers
/snppsend.pl

%changelog
* Sun May 15 2005 Aaron C. de Bruyn <code@darkpixel.com>
- Initial package


# New ports collection makefile for:	pymei
# Date created:		26 November 2008
# Whom:			Ulf Lilleengen <lulf@FreeBSD.org>
#
# $FreeBSD$
#

PORTNAME=	pymei
PORTVERSION=	0.2.0
PORTREVISION=	0
CATEGORIES=	multimedia
MASTER_SITES=	http://pymei.googlecode.com/files/
PKGNAMEPREFIX=	${PYTHON_PKGNAMEPREFIX}
EXTRACT_SUFX=	.tar.gz

MAINTAINER=	lulf@FreeBSD.org
COMMENT=	Python media interface

OPTIONS=	XKCD "Enable XKCD plugin support" on
OPTIONS+=	LIRC "Enable LIRC plugin support for remote controls" on

BUILD_DEPENDS=  py*-game>=0:${PORTSDIR}/devel/py-game \
		py*-yaml>=0:${PORTSDIR}/devel/py-yaml \
		mplayer>=0:${PORTSDIR}/multimedia/mplayer
RUN_DEPENDS:=	${BUILD_DEPENDS}

.if !defined(WITHOUT_LIRC)
RUN_DEPENDS+=	${PYTHON_SITELIBDIR}/pylircmodule.so:${PORTSDIR}/comms/py-lirc
.endif

.if !defined(WITHOUT_XKCD)
RUN_DEPENDS+=	${PYTHON_SITELIBDIR}/BeautifulSoup.py:${PORTSDIR}/www/py-beautifulsoup
.endif

USE_PYTHON=		yes
USE_PYDISTUTILS=	yes
WRKSRC=			${WRKDIR}/${PORTNAME}-${PORTVERSION}
PATCH_WRKSRC=		${WRKSRC}

.include <bsd.port.mk>

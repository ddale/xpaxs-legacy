/****************************************************************************
** Form implementation generated from reading ui file 'videowidget.ui'
**
** Created: Sat Nov 6 11:37:48 2004
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.1.2   edited Dec 19 11:45 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#include "videowidget.h"

#include <qvariant.h>
#include <qlayout.h>
#include <qtooltip.h>
#include <qwhatsthis.h>
#include "../videowidget.ui.h"

/* 
 *  Constructs a VideoWidget as a child of 'parent', with the 
 *  name 'name' and widget flags set to 'f'.
 */
VideoWidget::VideoWidget( QWidget* parent, const char* name, WFlags fl )
    : QWidget( parent, name, fl )
{
    if ( !name )
	setName( "VideoWidget" );
    setSizePolicy( QSizePolicy( (QSizePolicy::SizeType)5, (QSizePolicy::SizeType)5, 0, 0, sizePolicy().hasHeightForWidth() ) );
    setPaletteBackgroundColor( QColor( 0, 0, 0 ) );
    languageChange();
    resize( QSize(763, 918).expandedTo(minimumSizeHint()) );
    clearWState( WState_Polished );
    init();
}

/*
 *  Destroys the object and frees any allocated resources
 */
VideoWidget::~VideoWidget()
{
    destroy();
    // no need to delete child widgets, Qt does it all for us
}

/*
 *  Sets the strings of the subwidgets using the current
 *  language.
 */
void VideoWidget::languageChange()
{
    setCaption( tr( "VideoWidget" ) );
}

